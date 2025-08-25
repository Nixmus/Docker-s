"""
Monitor de rendimiento en tiempo real para la Ruleta Virtual
Monitorea estadísticas del servidor mientras se ejecutan las pruebas de carga
"""

import requests
import time
import json
import threading
from datetime import datetime
import argparse
import os

class PerformanceMonitor:
    def __init__(self, base_url="http://localhost:5000", interval=2):
        self.base_url = base_url
        self.interval = interval
        self.monitoring = False
        self.stats_history = []
        self.start_time = None
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.response_times = []
        self.cpu_usage = []
        self.memory_usage = []
        
    def get_server_stats(self):
        """Obtener estadísticas del servidor"""
        try:
            import psutil
            
            # Métricas del sistema
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_used_mb = memory.used / (1024 * 1024)
            
            # Obtener estadísticas del juego
            response = requests.get(f"{self.base_url}/api/statistics", timeout=5)
            if response.status_code == 200:
                game_stats = response.json()["statistics"]
            else:
                game_stats = {}
            
            # Obtener health check
            health_start = time.time()
            response = requests.get(f"{self.base_url}/health", timeout=5)
            health_response_time = (time.time() - health_start) * 1000
            health_ok = response.status_code == 200
            
            # Medir tiempo de respuesta para spin
            spin_start = time.time()
            response = requests.post(f"{self.base_url}/api/spin", timeout=10)
            spin_response_time = (time.time() - spin_start) * 1000  # en ms
            spin_success = response.status_code == 200
            
            # Actualizar contadores
            self.total_requests += 1
            if spin_success:
                self.successful_requests += 1
            else:
                self.failed_requests += 1
            
            # Guardar métricas
            self.response_times.append(spin_response_time)
            self.cpu_usage.append(cpu_percent)
            self.memory_usage.append(memory_percent)
            
            # Mantener solo los últimos 100 registros para cálculos
            if len(self.response_times) > 100:
                self.response_times.pop(0)
                self.cpu_usage.pop(0)
                self.memory_usage.pop(0)
            
            return {
                "timestamp": datetime.now().isoformat(),
                "health_ok": health_ok,
                "health_response_time_ms": health_response_time,
                "spin_response_time_ms": spin_response_time,
                "spin_success": spin_success,
                "game_stats": game_stats,
                "system_stats": {
                    "cpu_percent": cpu_percent,
                    "memory_percent": memory_percent,
                    "memory_used_mb": memory_used_mb
                }
            }
            
        except ImportError:
            # Si psutil no está disponible, usar versión básica
            return self.get_basic_server_stats()
        except Exception as e:
            return {
                "timestamp": datetime.now().isoformat(),
                "health_ok": False,
                "error": str(e),
                "spin_response_time_ms": None,
                "spin_success": False,
                "game_stats": {},
                "system_stats": {}
            }
    
    def get_basic_server_stats(self):
        """Versión básica sin psutil"""
        try:
            # Obtener estadísticas del juego
            response = requests.get(f"{self.base_url}/api/statistics", timeout=5)
            if response.status_code == 200:
                game_stats = response.json()["statistics"]
            else:
                game_stats = {}
            
            # Obtener health check
            response = requests.get(f"{self.base_url}/health", timeout=5)
            health_ok = response.status_code == 200
            
            # Medir tiempo de respuesta para spin
            start_time = time.time()
            response = requests.post(f"{self.base_url}/api/spin", timeout=10)
            spin_response_time = (time.time() - start_time) * 1000  # en ms
            spin_success = response.status_code == 200
            
            # Actualizar contadores
            self.total_requests += 1
            if spin_success:
                self.successful_requests += 1
            else:
                self.failed_requests += 1
            
            self.response_times.append(spin_response_time)
            if len(self.response_times) > 100:
                self.response_times.pop(0)
            
            return {
                "timestamp": datetime.now().isoformat(),
                "health_ok": health_ok,
                "spin_response_time_ms": spin_response_time,
                "spin_success": spin_success,
                "game_stats": game_stats,
                "system_stats": {}
            }
            
        except Exception as e:
            return {
                "timestamp": datetime.now().isoformat(),
                "health_ok": False,
                "error": str(e),
                "spin_response_time_ms": None,
                "spin_success": False,
                "game_stats": {},
                "system_stats": {}
            }
    
    def calculate_percentiles(self, data):
        """Calcular percentiles de una lista de datos"""
        if not data:
            return {"p50": 0, "p95": 0, "p99": 0}
        
        sorted_data = sorted(data)
        n = len(sorted_data)
        
        def percentile(p):
            index = int(n * p / 100)
            if index >= n:
                index = n - 1
            return sorted_data[index]
        
        return {
            "p50": percentile(50),
            "p95": percentile(95),
            "p99": percentile(99)
        }
    
    def get_performance_metrics(self):
        """Calcular métricas de rendimiento avanzadas"""
        if not self.stats_history:
            return {}
        
        # Calcular uptime
        uptime_seconds = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
        
        # Calcular RPS (Requests Per Second)
        rps = self.total_requests / uptime_seconds if uptime_seconds > 0 else 0
        
        # Calcular tasa de éxito
        success_rate = (self.successful_requests / self.total_requests * 100) if self.total_requests > 0 else 0
        
        # Percentiles de latencia
        latency_percentiles = self.calculate_percentiles(self.response_times)
        
        # Promedios de recursos del sistema
        avg_cpu = sum(self.cpu_usage) / len(self.cpu_usage) if self.cpu_usage else 0
        avg_memory = sum(self.memory_usage) / len(self.memory_usage) if self.memory_usage else 0
        
        # Tiempo de respuesta promedio
        avg_response_time = sum(self.response_times) / len(self.response_times) if self.response_times else 0
        
        return {
            "uptime_seconds": uptime_seconds,
            "rps": rps,
            "success_rate": success_rate,
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "avg_response_time_ms": avg_response_time,
            "latency_percentiles": latency_percentiles,
            "avg_cpu_percent": avg_cpu,
            "avg_memory_percent": avg_memory,
            "min_response_time": min(self.response_times) if self.response_times else 0,
            "max_response_time": max(self.response_times) if self.response_times else 0
        }
    
    def clear_screen(self):
        """Limpiar pantalla"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def get_status_indicator(self, value, thresholds):
        """Obtener indicador de estado basado en umbrales"""
        if value <= thresholds["excellent"]:
            return "🟢 EXCELENTE"
        elif value <= thresholds["good"]:
            return "🟡 BUENO"
        elif value <= thresholds["acceptable"]:
            return "🟠 ACEPTABLE"
        else:
            return "🔴 CRÍTICO"
    
    def display_stats(self, current_stats):
        """Mostrar estadísticas en tiempo real"""
        self.clear_screen()
        
        # Calcular métricas avanzadas
        metrics = self.get_performance_metrics()
        
        print("🎰 MONITOR DE RENDIMIENTO AVANZADO - RULETA VIRTUAL")
        print("=" * 70)
        print(f"🕐 Hora actual: {datetime.now().strftime('%H:%M:%S')}")
        
        if self.start_time:
            uptime = metrics.get("uptime_seconds", 0)
            hours = int(uptime // 3600)
            minutes = int((uptime % 3600) // 60)
            seconds = int(uptime % 60)
            print(f"⏱️  Uptime: {hours:02d}h {minutes:02d}m {seconds:02d}s")
        
        print(f"🌐 URL: {self.base_url}")
        print(f"📊 Intervalo: {self.interval} segundos")
        print("-" * 70)
        
        # === ESTADO DEL SERVIDOR ===
        print("🔧 ESTADO DEL SERVIDOR:")
        if current_stats["health_ok"]:
            print("   ✅ Servidor: FUNCIONANDO")
        else:
            print("   ❌ Servidor: ERROR")
            if "error" in current_stats:
                print(f"      Error: {current_stats['error']}")
        
        # === MÉTRICAS DE RENDIMIENTO PRINCIPALES ===
        print("\n🚀 MÉTRICAS DE RENDIMIENTO:")
        
        # Latencia
        if current_stats["spin_response_time_ms"]:
            response_time = current_stats["spin_response_time_ms"]
            latency_status = self.get_status_indicator(response_time, {
                "excellent": 100, "good": 500, "acceptable": 1000
            })
            print(f"   ⚡ Latencia actual: {response_time:.2f}ms - {latency_status}")
            
            if metrics.get("avg_response_time_ms"):
                avg_time = metrics["avg_response_time_ms"]
                print(f"   📊 Latencia promedio: {avg_time:.2f}ms")
                
                # Percentiles
                percentiles = metrics.get("latency_percentiles", {})
                if percentiles:
                    print(f"   📈 P50: {percentiles.get('p50', 0):.1f}ms | P95: {percentiles.get('p95', 0):.1f}ms | P99: {percentiles.get('p99', 0):.1f}ms")
        else:
            print("   ⚡ Latencia: ERROR")
        
        # Throughput (RPS)
        rps = metrics.get("rps", 0)
        if rps == 0:
            rps_status = "🔴 CRÍTICO"
        elif rps >= 10:
            rps_status = "🟢 EXCELENTE"
        elif rps >= 1:
            rps_status = "🟡 BUENO"
        else:
            rps_status = "🟠 ACEPTABLE"
        print(f"   🚀 Throughput: {rps:.2f} RPS - {rps_status}")
        
        # Disponibilidad/Tasa de éxito
        success_rate = metrics.get("success_rate", 0)
        success_status = self.get_status_indicator(100 - success_rate, {
            "excellent": 1, "good": 5, "acceptable": 10
        })
        print(f"   ✅ Disponibilidad: {success_rate:.1f}% - {success_status}")
        
        print(f"   📤 Total requests: {metrics.get('total_requests', 0)}")
        print(f"   ✅ Exitosos: {metrics.get('successful_requests', 0)}")
        print(f"   ❌ Fallidos: {metrics.get('failed_requests', 0)}")
        
        # === RECURSOS DEL SISTEMA ===
        system_stats = current_stats.get("system_stats", {})
        if system_stats:
            print("\n💻 RECURSOS DEL SISTEMA:")
            
            cpu = system_stats.get("cpu_percent", 0)
            cpu_status = self.get_status_indicator(cpu, {
                "excellent": 70, "good": 85, "acceptable": 95
            })
            print(f"   🖥️  CPU: {cpu:.1f}% - {cpu_status}")
            
            memory = system_stats.get("memory_percent", 0)
            memory_mb = system_stats.get("memory_used_mb", 0)
            memory_status = self.get_status_indicator(memory, {
                "excellent": 80, "good": 90, "acceptable": 95
            })
            print(f"   💾 RAM: {memory:.1f}% ({memory_mb:.0f}MB) - {memory_status}")
            
            # Promedios
            avg_cpu = metrics.get("avg_cpu_percent", 0)
            avg_memory = metrics.get("avg_memory_percent", 0)
            print(f"   📊 Promedios: CPU {avg_cpu:.1f}% | RAM {avg_memory:.1f}%")
        
        # === ESTADÍSTICAS DEL JUEGO ===
        game_stats = current_stats.get("game_stats", {})
        if game_stats:
            print("\n🎮 ESTADÍSTICAS DEL JUEGO:")
            print(f"   🎯 Total giros: {game_stats.get('total_spins', 0)}")
            print(f"   📈 Resultados mostrados: {game_stats.get('results_shown', 0)}")
            
            color_counts = game_stats.get('color_counts', {})
            percentages = game_stats.get('percentages', {})
            
            # Verificar si las probabilidades están dentro del rango esperado
            azul_real = percentages.get('azul', 0)
            morado_real = percentages.get('morado', 0)
            amarillo_real = percentages.get('amarillo', 0)
            
            azul_expected = 85.4
            morado_expected = 13.0
            amarillo_expected = 1.6
            
            azul_diff = abs(azul_real - azul_expected)
            morado_diff = abs(morado_real - morado_expected)
            amarillo_diff = abs(amarillo_real - amarillo_expected)
            
            azul_status = "✅" if azul_diff < 5 else "⚠️" if azul_diff < 10 else "❌"
            morado_status = "✅" if morado_diff < 3 else "⚠️" if morado_diff < 5 else "❌"
            amarillo_status = "✅" if amarillo_diff < 2 else "⚠️" if amarillo_diff < 3 else "❌"
            
            print(f"   🔵 Azul: {color_counts.get('azul', 0)} ({azul_real:.1f}% vs {azul_expected}%) {azul_status}")
            print(f"   🟣 Morado: {color_counts.get('morado', 0)} ({morado_real:.1f}% vs {morado_expected}%) {morado_status}")
            print(f"   🟡 Amarillo: {color_counts.get('amarillo', 0)} ({amarillo_real:.1f}% vs {amarillo_expected}%) {amarillo_status}")
            
            print(f"   ⏳ Giros desde último morado: {game_stats.get('spins_since_last_purple', 0)}")
            print(f"   ⏳ Giros desde último amarillo: {game_stats.get('spins_since_last_yellow', 0)}")
        
        # === RANGOS DE RESPUESTA ===
        if len(self.response_times) > 1:
            min_time = metrics.get("min_response_time", 0)
            max_time = metrics.get("max_response_time", 0)
            print(f"\n📊 RANGO DE LATENCIA:")
            print(f"   ⚡ Mínimo: {min_time:.2f}ms | Máximo: {max_time:.2f}ms")
        
        print("\n" + "-" * 70)
        print("💡 Presiona Ctrl+C para detener el monitoreo y guardar reporte")
        print("=" * 70)
    
    def monitor_loop(self):
        """Loop principal de monitoreo"""
        self.monitoring = True
        self.start_time = datetime.now()
        
        try:
            while self.monitoring:
                # Obtener estadísticas actuales
                current_stats = self.get_server_stats()
                self.stats_history.append(current_stats)
                
                # Mantener solo los últimos 100 registros
                if len(self.stats_history) > 100:
                    self.stats_history.pop(0)
                
                # Mostrar en pantalla
                self.display_stats(current_stats)
                
                # Esperar al siguiente intervalo
                time.sleep(self.interval)
                
        except KeyboardInterrupt:
            self.stop_monitoring()
    
    def stop_monitoring(self):
        """Detener monitoreo y guardar resultados"""
        self.monitoring = False
        
        print("\n\n🛑 Deteniendo monitoreo...")
        
        # Guardar historial en archivo
        if self.stats_history:
            filename = f"performance_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            report = {
                "start_time": self.start_time.isoformat(),
                "end_time": datetime.now().isoformat(),
                "total_records": len(self.stats_history),
                "interval_seconds": self.interval,
                "base_url": self.base_url,
                "history": self.stats_history
            }
            
            # Calcular estadísticas finales
            response_times = [s["spin_response_time_ms"] for s in self.stats_history if s["spin_response_time_ms"]]
            if response_times:
                report["summary"] = {
                    "avg_response_time_ms": sum(response_times) / len(response_times),
                    "min_response_time_ms": min(response_times),
                    "max_response_time_ms": max(response_times),
                    "successful_requests": sum(1 for s in self.stats_history if s["spin_success"]),
                    "total_requests": len(self.stats_history),
                    "success_rate_percent": (sum(1 for s in self.stats_history if s["spin_success"]) / len(self.stats_history)) * 100
                }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            print(f"📁 Log guardado en: {filename}")
            
            # Mostrar resumen final
            if "summary" in report:
                summary = report["summary"]
                print("\n📊 RESUMEN FINAL:")
                print(f"   ⏱️  Duración: {(datetime.now() - self.start_time).total_seconds():.0f} segundos")
                print(f"   📊 Total requests: {summary['total_requests']}")
                print(f"   ✅ Requests exitosos: {summary['successful_requests']}")
                print(f"   📈 Tasa de éxito: {summary['success_rate_percent']:.1f}%")
                print(f"   ⚡ Tiempo promedio: {summary['avg_response_time_ms']:.2f}ms")
                print(f"   ⚡ Tiempo mínimo: {summary['min_response_time_ms']:.2f}ms")
                print(f"   ⚡ Tiempo máximo: {summary['max_response_time_ms']:.2f}ms")
        
        print("\n✅ Monitoreo finalizado")

def main():
    parser = argparse.ArgumentParser(description='Monitor de rendimiento avanzado para Ruleta Virtual')
    parser.add_argument('--url', default='http://localhost:5000', 
                       help='URL base del servidor')
    parser.add_argument('--interval', type=int, default=2,
                       help='Intervalo de monitoreo en segundos')
    
    args = parser.parse_args()
    
    monitor = PerformanceMonitor(args.url, args.interval)
    
    print("🎰 Monitor de Rendimiento Avanzado - Ruleta Virtual")
    print("=" * 60)
    print(f"🎯 Monitoreando: {args.url}")
    print(f"⏱️  Intervalo: {args.interval} segundos")
    
    # Verificar si psutil está disponible
    try:
        import psutil
        print("✅ psutil detectado - Métricas del sistema habilitadas")
    except ImportError:
        print("⚠️  psutil no detectado - Solo métricas básicas")
        print("   Instala con: pip install psutil")
    
    print("\nPresiona Ctrl+C para detener\n")
    
    # Verificar conectividad inicial
    try:
        response = requests.get(f"{args.url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Conexión inicial exitosa")
        else:
            print("⚠️  Servidor responde con errores")
    except:
        print("❌ No se puede conectar al servidor")
        print("   ¿Está ejecutándose el servidor?")
        return
    
    time.sleep(2)
    monitor.monitor_loop()

if __name__ == "__main__":
    main()
