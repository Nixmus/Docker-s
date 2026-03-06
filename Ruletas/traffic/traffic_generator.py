"""
Generador de tráfico para la aplicación de Ruleta Virtual
Simula diferentes niveles de carga: bajo, medio y alto
"""

import asyncio
import aiohttp
import time
import random
from datetime import datetime
import argparse
import json

class TrafficGenerator:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "start_time": None,
            "end_time": None
        }
    
    async def single_spin(self, session, delay=0):
        """Realizar un giro individual"""
        if delay > 0:
            await asyncio.sleep(delay)
        
        try:
            async with session.post(f"{self.base_url}/api/spin") as response:
                self.stats["total_requests"] += 1
                if response.status == 200:
                    self.stats["successful_requests"] += 1
                    data = await response.json()
                    return data
                else:
                    self.stats["failed_requests"] += 1
                    return None
        except Exception as e:
            self.stats["failed_requests"] += 1
            print(f"Error en request: {e}")
            return None
    
    async def burst_spins(self, session, count=10):
        """Realizar múltiples giros en ráfaga"""
        tasks = []
        for i in range(count):
            # Pequeño delay aleatorio entre requests
            delay = random.uniform(0.1, 0.5)
            tasks.append(self.single_spin(session, delay))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results
    
    async def continuous_traffic(self, session, duration_seconds, requests_per_second):
        """Generar tráfico continuo por un tiempo determinado"""
        interval = 1.0 / requests_per_second if requests_per_second > 0 else 1.0
        end_time = time.time() + duration_seconds
        
        while time.time() < end_time:
            start = time.time()
            await self.single_spin(session)
            
            # Calcular tiempo de espera para mantener la frecuencia
            elapsed = time.time() - start
            sleep_time = max(0, interval - elapsed)
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
    
    async def simulate_users(self, session, num_users, actions_per_user, delay_between_actions):
        """Simular múltiples usuarios concurrentes"""
        async def user_session():
            for _ in range(actions_per_user):
                # Mezclar diferentes tipos de acciones
                action = random.choice(['spin', 'history', 'stats'])
                
                if action == 'spin':
                    await self.single_spin(session)
                elif action == 'history':
                    try:
                        async with session.get(f"{self.base_url}/api/history") as response:
                            self.stats["total_requests"] += 1
                            if response.status == 200:
                                self.stats["successful_requests"] += 1
                            else:
                                self.stats["failed_requests"] += 1
                    except:
                        self.stats["failed_requests"] += 1
                elif action == 'stats':
                    try:
                        async with session.get(f"{self.base_url}/api/statistics") as response:
                            self.stats["total_requests"] += 1
                            if response.status == 200:
                                self.stats["successful_requests"] += 1
                            else:
                                self.stats["failed_requests"] += 1
                    except:
                        self.stats["failed_requests"] += 1
                
                # Delay entre acciones del usuario
                await asyncio.sleep(random.uniform(0.5, delay_between_actions))
        
        # Crear tareas para todos los usuarios
        tasks = [user_session() for _ in range(num_users)]
        await asyncio.gather(*tasks, return_exceptions=True)
    
    async def run_traffic_test(self, traffic_level="medium", duration=60):
        """Ejecutar prueba de tráfico según el nivel especificado"""
        print(f"🚀 Iniciando prueba de tráfico: {traffic_level.upper()}")
        print(f"⏱️  Duración: {duration} segundos")
        print(f"🎯 URL objetivo: {self.base_url}")
        print("-" * 50)
        
        self.stats["start_time"] = datetime.now()
        
        connector = aiohttp.TCPConnector(limit=100, limit_per_host=50)
        timeout = aiohttp.ClientTimeout(total=30)
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            if traffic_level == "low":
                # Tráfico bajo: 1-2 requests por segundo
                await self.continuous_traffic(session, duration, 1.5)
                
            elif traffic_level == "medium":
                # Tráfico medio: 5-10 usuarios concurrentes
                await self.simulate_users(session, 8, 20, 2.0)
                
            elif traffic_level == "high":
                # Tráfico alto: 20-50 usuarios concurrentes con ráfagas
                tasks = [
                    self.simulate_users(session, 25, 15, 1.0),
                    self.continuous_traffic(session, duration//2, 10),
                    self.burst_spins(session, 50)
                ]
                await asyncio.gather(*tasks, return_exceptions=True)
                
            elif traffic_level == "extreme":
                # Tráfico extremo: stress test
                tasks = [
                    self.simulate_users(session, 50, 20, 0.5),
                    self.continuous_traffic(session, duration//3, 20),
                    self.burst_spins(session, 100),
                    self.burst_spins(session, 100),
                ]
                await asyncio.gather(*tasks, return_exceptions=True)
        
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
        print(f"🚀 Requests por segundo: {rps:.2f}")
        print(f"📈 Tasa de éxito: {success_rate:.2f}%")
        print("="*60)

async def main():
    parser = argparse.ArgumentParser(description='Generador de tráfico para Ruleta Virtual')
    parser.add_argument('--level', choices=['low', 'medium', 'high', 'extreme'], 
                       default='medium', help='Nivel de tráfico')
    parser.add_argument('--duration', type=int, default=60, 
                       help='Duración en segundos')
    parser.add_argument('--url', default='http://localhost:5000', 
                       help='URL base del servidor')
    
    args = parser.parse_args()
    
    generator = TrafficGenerator(args.url)
    await generator.run_traffic_test(args.level, args.duration)

if __name__ == "__main__":
    print("🎰 Generador de Tráfico - Ruleta Virtual")
    print("=" * 50)
    asyncio.run(main())
