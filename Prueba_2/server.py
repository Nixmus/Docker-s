from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
from datetime import datetime
from urllib.parse import urlparse, parse_qs

class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        
        # Servir archivos HTML estáticos
        if path == "/" or path == "/index.html":
            self.serve_file("index.html", "text/html")
        elif path == "/style.css":
            self.serve_file("style.css", "text/css")
        # API endpoints
        elif path == "/api/saludo":
            self.send_json({"mensaje": "¡Hola desde Python Backend!", "hora": datetime.now().strftime("%H:%M:%S")})
        elif path == "/api/contador":
            count = getattr(APIHandler, "contador", 0) + 1
            APIHandler.contador = count
            self.send_json({"contador": count})
        else:
            self.send_error(404)
    
    def serve_file(self, filename, content_type):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-type", content_type)
            self.end_headers()
            self.wfile.write(content.encode())
        except FileNotFoundError:
            self.send_error(404)
    
    def send_json(self, data):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), APIHandler)
    print("Servidor ejecutándose en puerto 8000...")
    server.serve_forever()