import kopf
import kubernetes
import logging

API_GROUP = "ally-dev-gpt.openai.azure.com"
API_VERSION = "v1alpha1"
KIND = "AzureAIService"
PLURAL = "azureaiservices"

@kopf.on.create(API_GROUP, API_VERSION, PLURAL)
@kopf.on.update(API_GROUP, API_VERSION, PLURAL)
def on_create(spec, name, namespace, logger, **kwargs):
    logger.info(f"Creating AzureAIService '{name}' in '{namespace}'")
    _apply_deployment(spec, name, namespace, logger)
    _apply_service(spec, name, namespace, logger)
    return {"message": f"Deployment and Service created for {name}"}


@kopf.on.update(API_GROUP, API_VERSION, PLURAL)
def on_update(spec, name, namespace, logger, **kwargs):
    logger.info(f"Updating AzureAIService '{name}' in '{namespace}'")
    _apply_deployment(spec, name, namespace, logger)
    _apply_service(spec, name, namespace, logger)
    return {"message": f"Deployment and Service updated for {name}"}


@kopf.on.delete(API_GROUP, API_VERSION, PLURAL)
def on_delete(spec, name, namespace, logger, **kwargs):
    logger.info(f"Deleting AzureAIService '{name}' — child resources cleaned up via ownerReferences")

def _apply_deployment(spec, name, namespace, logger):
    apps_v1 = kubernetes.client.AppsV1Api()

    image = spec.get("image")
    replicas = spec.get("replicas")
    port = spec.get("port")
    secret_name = spec.get("credentialsSecret")
    config_map_name = spec.get("configMap")

    deployment = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": name,
            "namespace": namespace,
            "labels": _generate_labels(name),
        },
        "spec": {
            "replicas": replicas,
            "selector": {"matchLabels": _generate_labels(name)},
            "template": {
                "metadata": {"labels": _generate_labels(name)},
                "spec": {
                    "containers": [
                        {
                            "name": "app",
                            "image": image,
                            "ports": [{"containerPort": port}],
                            "envFrom": [
                                {"secretRef": {"name": secret_name}},
                                {"configMapRef": {"name": config_map_name}},
                            ],
                            "resources": spec.get("resources"),
                        }
                    ]
                },
            },
        },
    }
    kopf.adopt(deployment) # Enable garbage collection when resource is deleted Yay!
    try:
        apps_v1.create_namespaced_deployment(namespace=namespace, body=deployment)
        logger.info(f"Deployment '{name}' created")
    except kubernetes.client.exceptions.ApiException as e:
        if e.status == 409:
            apps_v1.patch_namespaced_deployment(name=name, namespace=namespace, body=deployment)
            logger.info(f"Deployment '{name}' patched")
        else:
            raise


def _apply_service(spec, name, namespace, logger):
    core_v1 = kubernetes.client.CoreV1Api()

    port = spec.get("port")
    service_type = spec.get("serviceType")
    service = {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {
            "name": name,
            "namespace": namespace,
            "labels": _generate_labels(name),
        },
        "spec": {
            "type": service_type,
            "selector": _generate_labels(name),
            "ports": [
                {
                    "protocol": "TCP",
                    "port": 80,
                    "targetPort": port,
                }
            ],
        },
    }

    kopf.adopt(service)

    try:
        core_v1.create_namespaced_service(namespace=namespace, body=service)
        logger.info(f"Service '{name}' created")
    except kubernetes.client.exceptions.ApiException as e:
        if e.status == 409:
            core_v1.patch_namespaced_service(name=name, namespace=namespace, body=service)
            logger.info(f"Service '{name}' patched")
        else:
            raise


def _generate_labels(name: str) -> dict:
    return {
        "app": name,
        "managed-by": "azureaiservice-operator",
    }
