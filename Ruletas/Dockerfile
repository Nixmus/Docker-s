FROM python:3.9-slim

WORKDIR /app

# Instalar Flask directamente sin requirements.txt
RUN pip install --no-cache-dir Flask==2.3.3 Flask-CORS==4.0.0

# Copiar archivos del proyecto
COPY server.py .
COPY static/ ./static/

EXPOSE 5000

CMD ["python", "server.py"]