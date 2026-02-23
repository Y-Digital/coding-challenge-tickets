FROM python:3.14
ADD . /src
RUN pip install kopf kubernetes
CMD kopf run /src/handlers.py --verbose
