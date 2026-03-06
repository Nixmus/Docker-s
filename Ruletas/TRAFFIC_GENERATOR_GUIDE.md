#  Traffic Generator - Guía Completa

Este documento explica cómo funciona el sistema de generación de tráfico para **Ruleta Virtual** y qué métricas cubre el monitor de rendimiento.

##  **¿Qué es el Traffic Generator?**

El Traffic Generator es un sistema de **pruebas de carga** que simula múltiples usuarios interactuando con tu aplicación Ruleta Virtual de forma simultánea. Permite evaluar cómo se comporta tu servidor bajo diferentes niveles de estrés.

##  **Cómo Funciona**

### **1. Simulación de Usuarios Reales**

El sistema crea "usuarios virtuales" que hacen exactamente lo mismo que usuarios reales:

```python
# Lo que hace un usuario real:
1. Abre http://localhost:5000
2. Presiona "GIRAR RULETA"
3. Ve el resultado
4. Espera unos segundos
5. Repite el proceso

# Lo que hace el Traffic Generator:
1. Conecta a http://localhost:5000/api/spin
2. Hace POST request (igual que el botón)
3. Recibe el resultado JSON
4. Espera tiempo configurable
5. Repite automáticamente
```

### **2. Tipos de Tráfico Simulado**

#### ** Tráfico BAJO (Low)**
```
 Usuarios: 2-3 simulados
 Patrón: 1 acción cada 2-5 segundos
 Propósito: Verificación básica
 RPS Esperado: 1-3 requests/segundo
```

#### ** Tráfico MEDIO (Medium)**
```
 Usuarios: 8 simulados + requests continuos
 Patrón: 1 acción cada 1-3 segundos + 3 req/seg continuos
 Propósito: Simulación de uso real
 RPS Esperado: 5-15 requests/segundo
```

#### ** Tráfico ALTO (High)**
```
 Usuarios: 15 simulados + ráfagas + continuos
 Patrón: Acciones rápidas + ráfagas de 20-30 requests
 Propósito: Prueba de capacidad
 RPS Esperado: 15-30 requests/segundo
```

#### ** Tráfico EXTREMO (Extreme)**
```
 Usuarios: 30+ simulados + múltiples hilos
 Patrón: Acciones muy rápidas + ráfagas masivas
 Propósito: Stress test, encontrar límites
 RPS Esperado: 30+ requests/segundo
```

##  **Diferencias entre Generadores**

### **`simple_traffic.py`** - Generador Básico
```python
# Tecnología: Threading + requests
# Concurrencia: ~50-200 hilos simultáneos
# Instalación: Solo librerías estándar
# Uso: Pruebas normales y desarrollo

# Ejemplo de uso:
python simple_traffic.py --level medium --duration 60
```

** Ventajas:**
- Fácil de usar e instalar
- Funciona en cualquier sistema
- Ideal para empezar
- Debugging más simple

* Limitaciones:**
- Menor escalabilidad
- Más uso de memoria por hilo
- Limitado a ~200 usuarios simultáneos

### **`traffic_generator.py`** - Generador Avanzado
```python
# Tecnología: AsyncIO + aiohttp
# Concurrencia: Miles de requests simultáneos
# Instalación: Requiere pip install aiohttp
# Uso: Stress testing serio

# Ejemplo de uso:
pip install aiohttp
python traffic_generator.py --level extreme --duration 180
```

** Ventajas:**
- Altísima escalabilidad
- Uso eficiente de memoria
- Puede simular miles de usuarios
- Mejor para stress testing

** Limitaciones:**
- Más complejo de entender
- Requiere dependencias adicionales
- Debugging más difícil

##  **Métricas del Monitor de Rendimiento**

El **`performance_monitor.py`** rastrea métricas clave en tiempo real:

### ** Métricas de Rendimiento Principales**

#### **1.  Latencia/Tiempo de Respuesta**
```
Qué mide: Tiempo que tarda el servidor en procesar una request
Cómo: Mide tiempo desde envío hasta respuesta recibida
Umbrales:
 Excelente: < 100ms
 Bueno: 100-500ms
 Aceptable: 500ms-1s
 Crítico: > 1s

Incluye:
- Latencia actual en tiempo real
- Latencia promedio histórica
- Percentiles P50, P95, P99
- Tiempo mínimo y máximo registrado
```

#### **2.  Throughput (RPS - Requests Per Second)**
```
Qué mide: Número de requests procesadas por segundo
Cómo: Divide total de requests entre tiempo transcurrido
Umbrales:
 Alto: > 10 RPS
 Medio: 1-10 RPS
 Bajo: 0.1-1 RPS
 Crítico: < 0.1 RPS
```

#### **3.  Disponibilidad/Tasa de Éxito**
```
Qué mide: Porcentaje de requests exitosas vs fallidas
Cómo: (Requests exitosas / Total requests) × 100
Umbrales:
 Excelente: > 99%
 Bueno: 95-99%
 Aceptable: 90-95%
 Crítico: < 90%
```

### ** Métricas de Sistema**

#### **4.  Uso de CPU**
```
Qué mide: Porcentaje de procesador utilizado
Cómo: Usando psutil para monitorear CPU del sistema
Umbrales:
 Óptimo: < 70%
 Moderado: 70-85%
 Alto: 85-95%
 Crítico: > 95%

Incluye:
- CPU actual en tiempo real
- CPU promedio durante la sesión
```

#### **5.  Uso de Memoria RAM**
```
Qué mide: Porcentaje y cantidad de RAM utilizada
Cómo: Usando psutil para monitorear memoria del sistema
Umbrales:
 Óptimo: < 80%
 Moderado: 80-90%
 Alto: 90-95%
 Crítico: > 95%

Incluye:
- Porcentaje de RAM usado
- Cantidad en MB
- Promedio durante la sesión
```

### ** Métricas del Negocio (Específicas de Ruleta)**

#### **6.  Estadísticas del Juego**
```
Total de giros: Número absoluto de giros procesados
Resultados mostrados: Giros en el historial visible

Distribución de colores con verificación automática:
 Azul: Real vs Esperado (85.4%)
 Morado: Real vs Esperado (13.0%)
 Amarillo: Real vs Esperado (1.6%)

Indicadores de estado:
 Diferencia < 5% del esperado
  Diferencia 5-10% del esperado
 Diferencia > 10% del esperado

Garantías del sistema:
- Giros desde último morado (máx: 10)
- Giros desde último amarillo (máx: 90)
```

### ** Métricas Avanzadas**

#### **7.  Percentiles de Latencia**
```
P50 (Mediana): 50% de requests son más rápidas
P95: 95% de requests son más rápidas
P99: 99% de requests son más rápidas

Ejemplo:
P50: 120ms (la mitad de requests < 120ms)
P95: 800ms (solo 5% de requests > 800ms)
P99: 2000ms (solo 1% de requests > 2000ms)
```

#### **8.  Uptime y Estadísticas de Sesión**
```
Uptime: Tiempo total de monitoreo (HH:MM:SS)
Total requests: Número absoluto de requests monitoreadas
Requests exitosos/fallidos: Conteo detallado
Rango de latencia: Tiempo mínimo y máximo registrado
```

##  **Ejemplo de Monitoreo Completo**

### **Pantalla del Performance Monitor:**
```
 MONITOR DE RENDIMIENTO AVANZADO - RULETA VIRTUAL
======================================================================
 Hora actual: 14:30:25
 Uptime: 02h 15m 30s
 URL: http://localhost:5000
 Intervalo: 2 segundos
----------------------------------------------------------------------

🔧 ESTADO DEL SERVIDOR:
    Servidor: FUNCIONANDO

🚀 MÉTRICAS DE RENDIMIENTO:
    Latencia actual: 145.67ms -  BUENO
    Latencia promedio: 167.23ms
    P50: 135.2ms | P95: 456.8ms | P99: 1205.5ms
    Throughput: 18.5 RPS -  EXCELENTE
    Disponibilidad: 96.8% -  BUENO
    Total requests: 2,847
    Exitosos: 2,756
    Fallidos: 91

💻 RECURSOS DEL SISTEMA:
     CPU: 67.3% -  EXCELENTE
    RAM: 78.9% (3,156MB) -  EXCELENTE
    Promedios: CPU 71.2% | RAM 82.4%

🎮 ESTADÍSTICAS DEL JUEGO:
    Total giros: 2,847
    Resultados mostrados: 100
    Azul: 2,431 (85.4% vs 85.4%) 
    Morado: 369 (13.0% vs 13.0%) 
    Amarillo: 47 (1.7% vs 1.6%) 
    Giros desde último morado: 3
    Giros desde último amarillo: 47

📊 RANGO DE LATENCIA:
    Mínimo: 89.23ms | Máximo: 1,456.78ms

----------------------------------------------------------------------
 Presiona Ctrl+C para detener el monitoreo y guardar reporte
======================================================================
```

##  **Cómo Ejecutar una Prueba Completa**

### **Paso 1: Preparar el Entorno**
```bash
# Terminal 1: Iniciar servidor
cd "C:\Documentos\docker's\Ruletas"
python server.py
```

### **Paso 2: Iniciar Monitoreo**
```bash
# Terminal 2: Monitor de rendimiento
cd "C:\Documentos\docker's\Ruletas"
# Instalar métricas avanzadas (opcional)
pip install psutil
# Ejecutar monitor
python performance_monitor.py --interval 1
```

### **Paso 3: Generar Tráfico**
```bash
# Terminal 3: Generador de tráfico
cd "C:\Documentos\docker's\Ruletas"

# Prueba básica
python simple_traffic.py --level medium --duration 60

# O prueba avanzada
pip install aiohttp
python traffic_generator.py --level high --duration 120
```

### **Paso 4: Analizar Resultados**
- **Monitor en tiempo real:** Observa métricas en Terminal 2
- **Archivo de resultados:** `traffic_test_YYYYMMDD_HHMMSS.json`
- **Log de rendimiento:** `performance_log_YYYYMMDD_HHMMSS.json`

##  **Consideraciones Importantes**

### **Limitaciones del Servidor de Desarrollo**
```
Flask development server (python server.py):
- Diseñado para desarrollo, no producción
- Single-threaded por defecto
- Límites naturales de concurrencia
- Rendimiento menor que servidores de producción
```

### **Interpretación de Resultados**
```
Resultados esperados para Flask dev server:
 RPS: 5-30 (dependiendo del hardware)
 Latencia: 50-500ms (bajo carga normal)
 Concurrencia: 10-50 usuarios simultáneos
  > 50 usuarios: Posibles degradaciones

Para producción, considera:
- Gunicorn con workers
- nginx como reverse proxy
- Load balancers
- Bases de datos optimizadas
```

##  **Objetivos de Rendimiento Sugeridos**

| Métrica | Desarrollo | Producción |
|---------|------------|------------|
| **Latencia P95** | < 500ms | < 200ms |
| **RPS** | > 10 | > 100 |
| **Disponibilidad** | > 95% | > 99.9% |
| **CPU** | < 80% | < 70% |
| **RAM** | < 90% | < 80% |
| **Concurrencia** | 20 usuarios | 500+ usuarios |

¡Usa estas métricas para evaluar y optimizar tu aplicación Ruleta Virtual! 🎰🚀
