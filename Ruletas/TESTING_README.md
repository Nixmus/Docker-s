#  Generación de Tráfico y Pruebas de Carga

Este directorio contiene herramientas para generar diferentes niveles de tráfico y probar el rendimiento de la aplicación Ruleta Virtual.

##  Herramientas Disponibles

### 1. **simple_traffic.py** - Generador Principal
Generador de tráfico usando threading y requests. Compatible con cualquier instalación de Python.

```bash
# Uso básico
python simple_traffic.py --level medium --duration 60

# Todos los parámetros
python simple_traffic.py --level high --duration 120 --url http://localhost:5000
```

### 2. **traffic_generator.py** - Versión Async (Avanzada)
Versión con asyncio para pruebas más intensivas. Requiere `aiohttp`.

```bash
# Instalar dependencia
pip install aiohttp

# Ejecutar
python traffic_generator.py --level extreme --duration 180
```

### 3. **performance_monitor.py** - Monitor en Tiempo Real
Monitorea el rendimiento del servidor durante las pruebas.

```bash
# Monitoreo básico
python performance_monitor.py

# Con intervalo personalizado
python performance_monitor.py --interval 1 --url http://localhost:5000
```

### 4. **test_traffic.ps1** - Script PowerShell
Script interactivo para Windows PowerShell con verificaciones automáticas.

```powershell
# Ejecutar con permisos
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

# Usar
.\test_traffic.ps1 medium 60
.\test_traffic.ps1 high 120
```

### 5. **test_traffic.bat** - Script Batch
Interfaz gráfica simple en línea de comandos para Windows.

```batch
# Doble clic o ejecutar desde cmd
test_traffic.bat
```

##  Niveles de Tráfico

###  **BAJO (Low)**
- **Usuarios**: 2-3 simulados
- **Patrón**: Acciones espaciadas (2-5 seg entre acciones)
- **Duración recomendada**: 30-60 segundos
- **Uso**: Pruebas básicas, verificar funcionalidad

###  **MEDIO (Medium)**
- **Usuarios**: 8 simulados + requests continuos
- **Patrón**: 3 req/sec continuos + usuarios normales
- **Duración recomendada**: 60-90 segundos
- **Uso**: Simulación de uso real moderado

###  **ALTO (High)**
- **Usuarios**: 15 simulados + ráfagas + continuos
- **Patrón**: 8 req/sec + ráfagas periódicas de 20-30 requests
- **Duración recomendada**: 90-120 segundos
- **Uso**: Prueba de capacidad bajo carga

###  **EXTREMO (Extreme)**
- **Usuarios**: 30+ simulados + múltiples hilos continuos
- **Patrón**: 45+ req/sec + ráfagas masivas de 50-100 requests
- **Duración recomendada**: 120+ segundos
- **Uso**: Stress test, encontrar límites del sistema

##  Configuración y Preparación

### Requisitos Previos
```bash
# Python 3.7+
python --version

# Instalar dependencias básicas
pip install requests

# Para versión async (opcional)
pip install aiohttp
```

### Preparar el Servidor
```bash
# Asegúrate de que el servidor esté ejecutándose
python server.py

# Verificar que responde
curl http://localhost:5000/health
```

##  Interpretación de Resultados

### Métricas Clave
- **RPS (Requests/Second)**: Número de requests procesados por segundo
- **Tasa de Éxito**: Porcentaje de requests exitosos vs fallidos
- **Tiempo de Respuesta**: Latencia promedio de las requests
- **Throughput**: Capacidad total de procesamiento

### Valores de Referencia
| Nivel | RPS Esperado | Tiempo Respuesta | Tasa Éxito |
|-------|-------------|------------------|------------|
| Bajo | 1-3 RPS | < 100ms | > 98% |
| Medio | 5-15 RPS | < 200ms | > 95% |
| Alto | 15-30 RPS | < 500ms | > 90% |
| Extremo | 30+ RPS | < 1000ms | > 80% |

### Archivos de Resultados
Los tests generan archivos JSON con estadísticas detalladas:

```json
{
  "timestamp": "2025-08-24T10:30:00",
  "duration": 60.5,
  "total_requests": 1250,
  "successful_requests": 1190,
  "failed_requests": 60,
  "requests_per_second": 20.66,
  "success_rate": 95.2
}
```

##  Casos de Uso Específicos

### 1. **Verificación de Despliegue**
```bash
# Test rápido después de despliegue
python simple_traffic.py --level low --duration 30
```

### 2. **Prueba de Capacidad**
```bash
# Encontrar límite de usuarios concurrentes
python simple_traffic.py --level high --duration 120
```

### 3. **Monitoreo Continuo**
```bash
# En una terminal: monitoreo
python performance_monitor.py --interval 1

# En otra terminal: generar carga
python simple_traffic.py --level medium --duration 300
```

### 4. **Stress Test Completo**
```bash
# Test extremo con monitoreo
python performance_monitor.py --interval 2 &
python simple_traffic.py --level extreme --duration 180
```

## ⚠️ Consideraciones Importantes

### Limitaciones del Sistema
- **CPU**: Los tests intensivos pueden saturar el procesador
- **Memoria**: Monitorear uso de RAM durante tests extremos
- **Red**: En localhost no hay limitaciones de red reales
- **Base de Datos**: Si usas BD, considerar límites de conexiones

### Buenas Prácticas
1. **Empezar gradual**: Comenzar con tráfico bajo e ir subiendo
2. **Monitorear sistema**: Usar `htop` o Task Manager durante tests
3. **Guardar resultados**: Los archivos JSON son útiles para comparaciones
4. **Probar en producción**: Los resultados en localhost pueden diferir
5. **Cleanup**: Reiniciar el juego entre tests para resultados consistentes

### Solución de Problemas

#### "No se puede conectar al servidor"
```bash
# Verificar que el servidor esté corriendo
python server.py

# Verificar puerto
netstat -an | findstr :5000
```

#### "Requests fallidos"
- Verificar límites de timeout
- Reducir intensidad del test
- Verificar recursos del sistema

#### "Rendimiento degradado"
- Revisar uso de CPU/RAM
- Verificar logs del servidor
- Reducir concurrencia

##  Logs y Debugging

### Archivos Generados
- `traffic_test_YYYYMMDD_HHMMSS.json`: Resultados de tests de tráfico
- `performance_log_YYYYMMDD_HHMMSS.json`: Logs de monitoreo de rendimiento

### Debugging
```bash
# Ver logs en tiempo real (si usas logging en server.py)
tail -f server.log

# Monitorear recursos del sistema (Linux/Mac)
htop

# Monitorear recursos (Windows)
# Task Manager o:
wmic cpu get loadpercentage /value
```

##  Objetivos de Rendimiento

Para la aplicación Ruleta Virtual, objetivos sugeridos:

| Métrica | Objetivo | Crítico |
|---------|----------|---------|
| Tiempo respuesta | < 200ms | < 500ms |
| Disponibilidad | > 99% | > 95% |
| Throughput | > 10 RPS | > 5 RPS |
| Concurrencia | > 20 usuarios | > 10 usuarios |

¡Úsalos como referencia para evaluar el rendimiento de tu aplicación!
