FROM mongo:7.0

COPY mongo-init-script.js /docker-entrypoint-initdb.d/