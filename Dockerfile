FROM mongo:7.0

COPY mongo-init-script.js /docker-entrypoint-initdb.d/

FROM python:3.11.1
WORKDIR /app
RUN git clone https://github.com/Rayanlaffi1/apipapyrus.git .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "api.py"]
