

docker build -t azureaiservice-operator:latest .
kind load docker-image azureaiservice-operator:latest

kubectl apply -f crd.yaml
kubectl apply -f rbac.yaml
kubectl create secret generic azure-openai-credentials --from-env-file="../.env"
