FROM python:3.11-alpine
COPY server.py /app/server.py
COPY index.html /app/index.html
WORKDIR /app
EXPOSE 8000
CMD ["python", "server.py"]
