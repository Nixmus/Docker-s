# 🎰 Ruleta Virtual

Un simulador de ruleta web desarrollado en Python con Flask que implementa un sistema de probabilidades personalizado con garantías.

## 📋 Descripción

Este proyecto es una aplicación web que simula una ruleta con tres colores (azul, morado y amarillo) con probabilidades específicas y un sistema de garantías que asegura ciertos resultados después de determinados números de giros.

### 🎨 Características del Juego

- **Tres colores disponibles:**
  - 🔵 **Azul**: 85.4% de probabilidad
  - 🟣 **Morado**: 13.0% de probabilidad  
  - 🟡 **Amarillo**: 1.6% de probabilidad

- **Sistema de garantías:**
  - Morado garantizado cada 10 giros máximo
  - Amarillo garantizado cada 90 giros máximo

## 🚀 Tecnologías Utilizadas

- **Backend**: Python 3.9 + Flask
- **Frontend**: HTML5, CSS3, JavaScript vanilla
- **Containerización**: Docker
- **CORS**: Flask-CORS para comunicación entre frontend y backend

## 📁 Estructura del Proyecto

```
Ruletas/
├── Dockerfile              # Configuración de Docker
├── server.py               # Servidor Flask con lógica del juego
├── requirements.txt        # Dependencias Python (deprecado)
├── static/
│   ├── index.html         # Interfaz web principal
│   ├── script.js          # Lógica del frontend
│   └── style.css          # Estilos CSS
└── README.md              # Este archivo
```

## 🛠️ Instalación y Ejecución

### Opción 1: Con Docker (Recomendado)

1. **Construir la imagen:**
   ```bash
   docker build -t ruleta-virtual .
   ```

2. **Ejecutar el contenedor:**
   ```bash
   docker run -p 5000:5000 ruleta-virtual
   ```

3. **Acceder a la aplicación:**
   Abre tu navegador en `http://localhost:5000`

### Opción 2: Ejecución Local

1. **Instalar dependencias:**
   ```bash
   pip install Flask==2.3.3 Flask-CORS==4.0.0
   ```

2. **Ejecutar el servidor:**
   ```bash
   python server.py
   ```

3. **Acceder a la aplicación:**
   Abre tu navegador en `http://localhost:5000`

## 🎮 Uso de la Aplicación

### Interfaz Web
- **Botón "GIRAR RULETA"**: Realiza un giro individual
- **Botón "TIRAR 10"**: Realiza 10 giros automáticamente
- **Botón "REINICIAR"**: Reinicia todas las estadísticas

### Estadísticas en Tiempo Real
- Contador total de giros
- Distribución por colores con porcentajes
- Visualización del último resultado
- Información sobre las garantías activas

## 🔌 API Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/spin` | Realiza un giro de la ruleta |
| `GET` | `/api/history` | Obtiene el historial de resultados |
| `GET` | `/api/statistics` | Obtiene estadísticas del juego |
| `POST` | `/api/reset` | Reinicia el juego |
| `GET` | `/api/colors` | Obtiene información de colores y probabilidades |
| `GET` | `/health` | Health check del servidor |

### Ejemplo de Respuesta API

```json
{
  "success": true,
  "result": {
    "spin_number": 1,
    "result": 1,
    "color": "azul",
    "timestamp": "2025-08-24T10:30:00.123456"
  },
  "statistics": {
    "total_spins": 1,
    "results_shown": 1,
    "color_counts": {"azul": 1, "morado": 0, "amarillo": 0},
    "percentages": {"azul": 100.0, "morado": 0.0, "amarillo": 0.0},
    "spins_since_last_purple": 1,
    "spins_since_last_yellow": 1
  }
}
```

## ⚙️ Configuración

### Probabilidades
Las probabilidades están definidas en la clase `RuletaGame` en `server.py`:

```python
self.colors = {
    1: {"name": "azul", "probability": 85.4},
    2: {"name": "morado", "probability": 13.0}, 
    3: {"name": "amarillo", "probability": 1.6}
}
```

### Sistema de Garantías
- **Morado**: Forzado después de 10 giros sin morado
- **Amarillo**: Forzado después de 90 giros sin amarillo

## 🐳 Docker

El proyecto incluye un `Dockerfile` optimizado que:
- Usa Python 3.9-slim como base
- Instala dependencias directamente sin requirements.txt
- Expone el puerto 5000
- Configura el directorio de trabajo en `/app`

## 📊 Funcionalidades Avanzadas

- **Historial limitado**: Mantiene solo los últimos 100 resultados en memoria
- **Estadísticas en tiempo real**: Actualización automática de porcentajes
- **Animaciones CSS**: Efecto visual de giro de ruleta
- **Responsive Design**: Interfaz adaptable a diferentes dispositivos

## 🔧 Desarrollo

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Realiza tus cambios
4. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
5. Push a la rama (`git push origin feature/nueva-funcionalidad`)
6. Crea un Pull Request

## 📝 Notas

- El archivo `requirements.txt` está marcado como deprecado; las dependencias se instalan directamente en el Dockerfile
- El servidor se ejecuta en modo debug por defecto para desarrollo
- La aplicación guarda el estado en memoria (se reinicia al reiniciar el servidor)

## 🚀 Próximas Mejoras

- Persistencia de datos en base de datos
- Sistema de usuarios y sesiones
- Más tipos de apuestas
- Sonidos y efectos visuales mejorados
- Modo multijugador

---

**Desarrollado con ❤️ usando Flask y Docker**
