# 📊 Métricas de Rendimiento - Monitor Avanzado

Este documento detalla todas las métricas que cubre el **Monitor de Rendimiento Avanzado** de Ruleta Virtual y cómo interpretarlas.

## 🎯 **Vista General del Monitor**

El `performance_monitor.py` rastrea **8 categorías principales** de métricas en tiempo real:

1. **⚡ Métricas de Latencia**
2. **🚀 Métricas de Throughput**
3. **✅ Métricas de Disponibilidad**
4. **💻 Métricas de Recursos del Sistema**
5. **🎮 Métricas de Negocio (Ruleta)**
6. **📈 Métricas Estadísticas Avanzadas**
7. **⏱️ Métricas de Tiempo/Uptime**
8. **🔍 Métricas de Diagnóstico**

## ⚡ **1. Métricas de Latencia**

### **Latencia Actual**
```
Descripción: Tiempo de respuesta de la última request
Medición: Desde envío POST /api/spin hasta respuesta recibida
Actualización: Cada intervalo (2 segundos por defecto)
Formato: XXX.XXms

Umbrales de Estado:
🟢 EXCELENTE: < 100ms
🟡 BUENO: 100-500ms
🟠 ACEPTABLE: 500ms-1s
🔴 CRÍTICO: > 1s
```

### **Latencia Promedio**
```
Descripción: Promedio de todas las latencias en la sesión
Cálculo: Suma de latencias / Número de mediciones
Utilidad: Evaluar rendimiento general durante la prueba
```

### **Percentiles de Latencia**
```
P50 (Mediana): 50% de requests son más rápidas que este valor
P95: Solo 5% de requests son más lentas que este valor
P99: Solo 1% de requests son más lentas que este valor

Ejemplo de interpretación:
P50: 120ms → La experiencia típica del usuario
P95: 800ms → El 95% de usuarios tienen buena experiencia
P99: 2000ms → Solo casos extremos (1%) son muy lentos
```

### **Rango de Latencia**
```
Mínimo: La request más rápida registrada
Máximo: La request más lenta registrada
Utilidad: Detectar variabilidad extrema en rendimiento
```

## 🚀 **2. Métricas de Throughput**

### **RPS (Requests Per Second)**
```
Descripción: Número de requests procesadas por segundo
Cálculo: Total requests / Tiempo transcurrido
Actualización: Continua durante la sesión

Interpretación por Nivel:
🟢 ALTO: > 10 RPS (Servidor maneja bien la carga)
🟡 MEDIO: 1-10 RPS (Rendimiento moderado)
🟠 BAJO: 0.1-1 RPS (Posibles cuellos de botella)
🔴 CRÍTICO: < 0.1 RPS (Servidor saturado/con problemas)
```

### **Total de Requests**
```
Descripción: Número absoluto de requests enviadas al servidor
Incluye: Tanto exitosas como fallidas
Utilidad: Evaluar volumen total de la prueba
```

## ✅ **3. Métricas de Disponibilidad**

### **Tasa de Éxito (Success Rate)**
```
Descripción: Porcentaje de requests exitosas
Cálculo: (Requests exitosas / Total requests) × 100
Formato: XX.X%

Umbrales de Calidad:
🟢 EXCELENTE: > 99% (Solo 1 de cada 100 falla)
🟡 BUENO: 95-99% (2-5 de cada 100 fallan)
🟠 ACEPTABLE: 90-95% (5-10 de cada 100 fallan)
🔴 CRÍTICO: < 90% (Más de 10 de cada 100 fallan)
```

### **Requests Exitosos vs Fallidos**
```
Exitosos: HTTP 200 + respuesta JSON válida
Fallidos: HTTP 5XX, timeouts, errores de conexión

Causas comunes de fallos:
- Servidor sobrecargado (HTTP 503)
- Timeouts por lentitud
- Errores en código Python (HTTP 500)
- Problemas de memoria/CPU
```

## 💻 **4. Métricas de Recursos del Sistema**

### **Uso de CPU**
```
Descripción: Porcentaje del procesador utilizado
Medición: Via psutil.cpu_percent()
Actualización: Cada intervalo
Incluye: CPU actual + promedio de la sesión

Umbrales de Rendimiento:
🟢 ÓPTIMO: < 70% (Sistema cómodo)
🟡 MODERADO: 70-85% (Carga media)
🟠 ALTO: 85-95% (Cerca del límite)
🔴 CRÍTICO: > 95% (Saturación, posibles timeouts)
```

### **Uso de Memoria RAM**
```
Descripción: Porcentaje y cantidad absoluta de RAM utilizada
Medición: Via psutil.virtual_memory()
Formato: XX.X% (XXXXmb)

Umbrales de Memoria:
🟢 ÓPTIMO: < 80% (Mucha memoria disponible)
🟡 MODERADO: 80-90% (Memoria controlada)
🟠 ALTO: 90-95% (Cerca del límite)
🔴 CRÍTICO: > 95% (Riesgo de swap/crash)
```

### **Promedios de Recursos**
```
CPU Promedio: Media de uso de CPU durante toda la sesión
RAM Promedio: Media de uso de RAM durante toda la sesión
Utilidad: Evaluar consumo sostenido vs picos temporales
```

## 🎮 **5. Métricas de Negocio (Específicas de Ruleta)**

### **Estadísticas de Giros**
```
Total de giros: Número absoluto procesado por el servidor
Resultados mostrados: Giros visibles en historial (últimos 100)
Utilidad: Verificar que el servidor procesa requests correctamente
```

### **Distribución de Colores con Verificación**
```
🔵 Azul: XXX (XX.X% vs 85.4%) ✅/⚠️/❌
🟣 Morado: XXX (XX.X% vs 13.0%) ✅/⚠️/❌  
🟡 Amarillo: XXX (XX.X% vs 1.6%) ✅/⚠️/❌

Indicadores de Estado:
✅ Diferencia < 5% del esperado (Probabilidades correctas)
⚠️  Diferencia 5-10% del esperado (Ligera desviación)
❌ Diferencia > 10% del esperado (Posible problema en lógica)

Nota: Con pocos giros es normal tener desviaciones
```

### **Sistema de Garantías**
```
Giros desde último morado: X (máximo: 10)
Giros desde último amarillo: X (máximo: 90)

Verificaciones:
- Si morado > 10 → Sistema de garantías fallando
- Si amarillo > 90 → Sistema de garantías fallando
- Valores normales indican funcionamiento correcto
```

## 📈 **6. Métricas Estadísticas Avanzadas**

### **Percentiles Explicados**
```
¿Qué son? Valores que dividen las mediciones en porcentajes

P50 (Mediana): 
- El valor que está justo en el medio
- 50% de mediciones están por debajo
- 50% de mediciones están por encima
- Representa la "experiencia típica"

P95:
- 95% de mediciones están por debajo
- Solo 5% son peores que este valor
- Importante para SLAs y calidad de servicio

P99:
- 99% de mediciones están por debajo
- Solo 1% son peores (casos extremos)
- Crítico para detectar outliers
```

### **Ejemplo Práctico de Percentiles**
```
100 mediciones de latencia ordenadas:
[50ms, 52ms, 55ms, ..., 180ms, 220ms, 1500ms]

P50: 120ms → Usuario típico espera ~120ms
P95: 400ms → 95% de usuarios esperan < 400ms
P99: 1200ms → Solo 1% experimenta > 1200ms

Conclusión: Buen rendimiento general con algunos casos lentos
```

## ⏱️ **7. Métricas de Tiempo/Uptime**

### **Uptime de Monitoreo**
```
Formato: HH:MM:SS
Descripción: Tiempo total que ha estado ejecutándose el monitor
Utilidad: Contextualizar todas las demás métricas
```

### **Timestamp**
```
Hora actual: Timestamp de la medición más reciente
Utilidad: Correlacionar con logs externos o eventos
```

## 🔍 **8. Métricas de Diagnóstico**

### **Estado del Servidor**
```
✅ FUNCIONANDO: /health endpoint responde HTTP 200
❌ ERROR: Servidor no responde o devuelve errores
Incluye: Mensaje de error específico si hay problemas
```

### **Tiempo de Respuesta del Health Check**
```
Descripción: Latencia del endpoint /health
Utilidad: Separar problemas de red vs problemas de procesamiento
Comparación: Si /health es rápido pero /spin es lento → problema en lógica de spin
```

## 📊 **Instalación de Métricas Avanzadas**

### **Con psutil (Recomendado)**
```bash
pip install psutil
python performance_monitor.py
# Obtiene: CPU, RAM, y todas las métricas del sistema
```

### **Sin psutil (Básico)**
```bash
python performance_monitor.py
# Obtiene: Solo métricas de red/aplicación, sin sistema
```

## 🎪 **Interpretación de Resultados Típicos**

### **Escenario: Sistema Saludable**
```
⚡ Latencia: 80-200ms → 🟢 EXCELENTE/BUENO
🚀 RPS: 15-25 → 🟢 ALTO
✅ Disponibilidad: 98-100% → 🟢 EXCELENTE
💻 CPU: 40-70% → 🟢 ÓPTIMO
💾 RAM: 60-80% → 🟢 ÓPTIMO
🎮 Colores: Todos ✅ → Lógica correcta
```

### **Escenario: Sistema Sobrecargado**
```
⚡ Latencia: 500-2000ms → 🟠/🔴 CRÍTICO
🚀 RPS: 2-5 → 🟡 MEDIO/BAJO
✅ Disponibilidad: 85-95% → 🟠 ACEPTABLE
💻 CPU: 85-95% → 🟠/🔴 ALTO/CRÍTICO
💾 RAM: 90-95% → 🟠/🔴 ALTO/CRÍTICO
🎮 Colores: Posibles ⚠️ → Menos precisión bajo carga
```

### **Escenario: Problemas de Red**
```
⚡ Latencia: Variable/Timeouts → 🔴 CRÍTICO
🚀 RPS: Muy bajo → 🔴 CRÍTICO
✅ Disponibilidad: < 90% → 🔴 CRÍTICO
💻 CPU: Normal 20-40% → 🟢 (No es problema de servidor)
💾 RAM: Normal 50-70% → 🟢 (No es problema de servidor)
🎮 Diagnóstico: Problema de conectividad, no de aplicación
```

## 🚀 **Comandos de Monitoreo**

### **Básico**
```bash
python performance_monitor.py
```

### **Con Intervalo Personalizado**
```bash
python performance_monitor.py --interval 1  # Cada segundo
python performance_monitor.py --interval 5  # Cada 5 segundos
```

### **URL Personalizada**
```bash
python performance_monitor.py --url http://192.168.1.100:5000
```

### **Monitoreo + Generación de Tráfico**
```bash
# Terminal 1: Monitor
python performance_monitor.py --interval 1

# Terminal 2: Tráfico (después de 5 segundos)
python simple_traffic.py --level medium --duration 120
```

## 📁 **Archivos de Resultados**

### **performance_log_YYYYMMDD_HHMMSS.json**
```json
{
  "start_time": "2025-08-24T14:30:15",
  "end_time": "2025-08-24T14:32:45",
  "total_records": 75,
  "interval_seconds": 2,
  "base_url": "http://localhost:5000",
  "summary": {
    "avg_response_time_ms": 167.23,
    "min_response_time_ms": 89.45,
    "max_response_time_ms": 1456.78,
    "successful_requests": 72,
    "total_requests": 75,
    "success_rate_percent": 96.0
  },
  "history": [...]
}
```

## 🏆 **Objetivos de Rendimiento por Entorno**

### **Desarrollo Local**
```
⚡ Latencia P95: < 500ms
🚀 RPS: > 5
✅ Disponibilidad: > 95%
💻 CPU: < 80%
💾 RAM: < 85%
```

### **Staging/Testing**
```
⚡ Latencia P95: < 300ms
🚀 RPS: > 20
✅ Disponibilidad: > 98%
💻 CPU: < 70%
💾 RAM: < 80%
```

### **Producción**
```
⚡ Latencia P95: < 200ms
🚀 RPS: > 100
✅ Disponibilidad: > 99.9%
💻 CPU: < 60%
💾 RAM: < 75%
```

¡Usa estas métricas para optimizar y monitorear tu aplicación Ruleta Virtual! 🎰📊
