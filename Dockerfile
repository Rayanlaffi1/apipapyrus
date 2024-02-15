FROM mongo:7.0

COPY mongo-init-script.js /docker-entrypoint-initdb.d/

FROM python:3.9
WORKDIR /app
RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/votre_utilisateur/votre_repo.git .
RUN pip install -r requirements.txt
RUN python fonctions/initkeycloak.py
CMD ["python", "loadmodel.py"]
CMD ["python", "api.py"]
