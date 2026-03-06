"""
Generador de tráfico simple usando requests (sin dependencias async)
Para generar diferentes niveles de carga en la Ruleta Virtual
"""

import requests
import time
import threading
import random
from datetime import datetime
import argparse
import json

class SimpleTrafficGenerator:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "start_time": None,
            "end_time": None
        }
        self.stats_lock = threading.Lock()
    
    def update_stats(self, success=True):
        """Actualizar estadísticas de forma thread-safe"""
        with self.stats_lock:
            self.stats["total_requests"] += 1
            if success:
                self.stats["successful_requests"] += 1
            else:
                self.stats["failed_requests"] += 1
    
    def single_spin(self):
        """Realizar un giro individual"""
        try:
            response = requests.post(f"{self.base_url}/api/spin", timeout=10)
            if response.status_code == 200:
                self.update_stats(True)
                return response.json()
            else:
                self.update_stats(False)
                return None
        except Exception as e:
            self.update_stats(False)
            print(f"Error en request: {e}")
            return None
    
    def get_history(self):
        """Obtener historial"""
        try:
            response = requests.get(f"{self.base_url}/api/history", timeout=10)
            if response.status_code == 200:
                self.update_stats(True)
                return response.json()
            else:
                self.update_stats(False)
                return None
        except Exception as e:
            self.update_stats(False)
            return None
    
    def get_stats(self):
        """Obtener estadísticas"""
        try:
            response = requests.get(f"{self.base_url}/api/statistics", timeout=10)
            if response.status_code == 200:
                self.update_stats(True)
                return response.json()
            else:
                self.update_stats(False)
                return None
        except Exception as e:
            self.update_stats(False)
            return None
    
    def user_simulation(self, user_id, actions_count, delay_range):
        """Simular un usuario individual"""
        print(f"👤 Usuario {user_id} iniciado")
        
        for i in range(actions_count):
            # Elegir acción aleatoria
            action = random.choice(['spin', 'spin', 'spin', 'history', 'stats'])  # Más probabilidad de spin
            
            if action == 'spin':
                self.single_spin()
            elif action == 'history':
                self.get_history()
            elif action == 'stats':
                self.get_stats()
            
            # Delay aleatorio entre acciones
            delay = random.uniform(delay_range[0], delay_range[1])
            time.sleep(delay)
        
        print(f"👤 Usuario {user_id} terminado")
    
    def continuous_requests(self, duration, requests_per_second):
        """Generar requests continuos"""
        interval = 1.0 / requests_per_second
        end_time = time.time() + duration
        
        while time.time() < end_time:
            start = time.time()
            self.single_spin()
            
            elapsed = time.time() - start
            sleep_time = max(0, interval - elapsed)
            if sleep_time > 0:
                time.sleep(sleep_time)
    
    def burst_requests(self, count, delay_between_bursts=0.1):
        """Generar ráfaga de requests"""
        print(f"💥 Generando ráfaga de {count} requests...")
        threads = []
        
        for i in range(count):
            thread = threading.Thread(target=self.single_spin)
            threads.append(thread)
            thread.start()
            time.sleep(delay_between_bursts)
        
        # Esperar a que terminen todos
        for thread in threads:
            thread.join()
        
        print(f"💥 Ráfaga completada")
    
    def run_traffic_test(self, level="medium", duration=60):
        """Ejecutar prueba según el nivel de tráfico"""
        print(f"🚀 Iniciando prueba de tráfico: {level.upper()}")
        print(f"⏱️  Duración: {duration} segundos")
        print(f"🎯 URL objetivo: {self.base_url}")
        print("-" * 50)
        
        self.stats["start_time"] = datetime.now()
        threads = []
        
        if level == "low":
            # Tráfico bajo: 2-3 usuarios, pocas acciones
            print("📊 Configuración BAJA: 2-3 usuarios simulados")
            for i in range(3):
                thread = threading.Thread(
                    target=self.user_simulation, 
                    args=(i+1, 10, (2.0, 5.0))  # 10 acciones, delay 2-5 seg
                )
                threads.append(thread)
                thread.start()
        
        elif level == "medium":
            # Tráfico medio: 5-8 usuarios + requests continuos
            print("📊 Configuración MEDIA: 8 usuarios + requests continuos")
            
            # Usuarios simulados
            for i in range(8):
                thread = threading.Thread(
                    target=self.user_simulation,
                    args=(i+1, 15, (1.0, 3.0))  # 15 acciones, delay 1-3 seg
                )
                threads.append(thread)
                thread.start()
            
            # Requests continuos en paralelo
            thread = threading.Thread(
                target=self.continuous_requests,
                args=(duration//2, 3)  # 3 req/sec por la mitad del tiempo
            )
            threads.append(thread)
            thread.start()
        
        elif level == "high":
            # Tráfico alto: muchos usuarios + ráfagas + continuos
            print("📊 Configuración ALTA: 15 usuarios + ráfagas + continuos")
            
            # Muchos usuarios
            for i in range(15):
                thread = threading.Thread(
                    target=self.user_simulation,
                    args=(i+1, 20, (0.5, 2.0))  # 20 acciones, delay 0.5-2 seg
                )
                threads.append(thread)
                thread.start()
            
            # Requests continuos agresivos
            thread = threading.Thread(
                target=self.continuous_requests,
                args=(duration//3, 8)  # 8 req/sec
            )
            threads.append(thread)
            thread.start()
            
            # Ráfagas periódicas
            def periodic_bursts():
                time.sleep(5)  # Esperar 5 segundos
                self.burst_requests(20)
                time.sleep(10)
                self.burst_requests(30)
                time.sleep(10)
                self.burst_requests(25)
            
            thread = threading.Thread(target=periodic_bursts)
            threads.append(thread)
            thread.start()
        
        elif level == "extreme":
            # Stress test extremo
            print("📊 Configuración EXTREMA: ¡Stress test máximo!")
            
            # Muchísimos usuarios
            for i in range(30):
                thread = threading.Thread(
                    target=self.user_simulation,
                    args=(i+1, 25, (0.2, 1.0))
                )
                threads.append(thread)
                thread.start()
            
            # Requests continuos muy agresivos
            for i in range(3):  # 3 hilos de requests continuos
                thread = threading.Thread(
                    target=self.continuous_requests,
                    args=(duration//2, 15)  # 15 req/sec cada hilo
                )
                threads.append(thread)
                thread.start()
            
            # Ráfagas masivas
            def massive_bursts():
                time.sleep(2)
                self.burst_requests(50, 0.05)
                time.sleep(8)
                self.burst_requests(75, 0.03)
                time.sleep(8)
                self.burst_requests(100, 0.02)
            
            thread = threading.Thread(target=massive_bursts)
            threads.append(thread)
            thread.start()
        
        # Esperar a que terminen todos los hilos
        for thread in threads:
            thread.join()
        
        self.stats["end_time"] = datetime.now()
        self.print_results()
    
    def print_results(self):
        """Imprimir estadísticas del test"""
        duration = (self.stats["end_time"] - self.stats["start_time"]).total_seconds()
        rps = self.stats["total_requests"] / duration if duration > 0 else 0
        success_rate = (self.stats["successful_requests"] / self.stats["total_requests"] * 100) if self.stats["total_requests"] > 0 else 0
        
        print("\n" + "="*60)
        print("📊 RESULTADOS DE LA PRUEBA DE TRÁFICO")
        print("="*60)
        print(f"⏱️  Duración total: {duration:.2f} segundos")
        print(f"📤 Total de requests: {self.stats['total_requests']}")
        print(f"✅ Requests exitosos: {self.stats['successful_requests']}")
        print(f"❌ Requests fallidos: {self.stats['failed_requests']}")
        print(f"🚀 Requests por segundo promedio: {rps:.2f}")
        print(f"📈 Tasa de éxito: {success_rate:.2f}%")
        print("="*60)
        
        # Guardar resultados en archivo
        results = {
            "timestamp": self.stats["start_time"].isoformat(),
            "duration": duration,
            "total_requests": self.stats["total_requests"],
            "successful_requests": self.stats["successful_requests"],
            "failed_requests": self.stats["failed_requests"],
            "requests_per_second": rps,
            "success_rate": success_rate
        }
        
        filename = f"traffic_test_{self.stats['start_time'].strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"📁 Resultados guardados en: {filename}")

def main():
    parser = argparse.ArgumentParser(description='Generador de tráfico simple para Ruleta Virtual')
    parser.add_argument('--level', choices=['low', 'medium', 'high', 'extreme'], 
                       default='medium', help='Nivel de tráfico')
    parser.add_argument('--duration', type=int, default=60, 
                       help='Duración en segundos')
    parser.add_argument('--url', default='http://localhost:5000', 
                       help='URL base del servidor')
    
    args = parser.parse_args()
    
    generator = SimpleTrafficGenerator(args.url)
    
    # Verificar que el servidor esté disponible
    try:
        response = requests.get(f"{args.url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor detectado y funcionando")
        else:
            print("⚠️  Servidor responde pero con errores")
    except:
        print("❌ No se puede conectar al servidor. ¿Está ejecutándose?")
        print(f"   Verifica que el servidor esté corriendo en {args.url}")
        return
    
    # Ejecutar test
    generator.run_traffic_test(args.level, args.duration)

if __name__ == "__main__":
    print("🎰 Generador de Tráfico Simple - Ruleta Virtual")
    print("=" * 60)
    main()
