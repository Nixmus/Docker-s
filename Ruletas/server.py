from flask import Flask, jsonify, request, send_from_directory, send_file
from flask_cors import CORS
import random
import json
from datetime import datetime

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

class RuletaGame:
    def __init__(self):
        self.results_history = []
        self.spin_count = 0
        self.last_purple_spin = 0
        self.last_yellow_spin = 0
        self.colors = {
            1: {"name": "azul", "probability": 85.4},
            2: {"name": "morado", "probability": 13.0}, 
            3: {"name": "amarillo", "probability": 1.6}
        }
    
    def spin(self):
        self.spin_count += 1
        
        # Verificar garantías
        spins_since_purple = self.spin_count - self.last_purple_spin
        spins_since_yellow = self.spin_count - self.last_yellow_spin
        
        # Garantía: morado cada 10 tiros
        if spins_since_purple >= 10:
            result = 2  # morado
            self.last_purple_spin = self.spin_count
        # Garantía: amarillo cada 90 tiros
        elif spins_since_yellow >= 90:
            result = 3  # amarillo
            self.last_yellow_spin = self.spin_count
        else:
            # Probabilidades normales
            rand = random.uniform(0, 100)
            if rand <= 1.6:
                result = 3  # amarillo
                self.last_yellow_spin = self.spin_count
            elif rand <= 14.6:  # 1.6 + 13
                result = 2  # morado
                self.last_purple_spin = self.spin_count
            else:
                result = 1  # azul
        
        # Registrar resultado
        spin_result = {
            "spin_number": self.spin_count,
            "result": result,
            "color": self.colors[result]["name"],
            "timestamp": datetime.now().isoformat()
        }
        
        self.results_history.append(spin_result)
        
        # Mantener solo los últimos 100 resultados
        if len(self.results_history) > 100:
            self.results_history.pop(0)
            
        return spin_result
    
    def get_statistics(self):
        if not self.results_history:
            return {"total_spins": 0, "color_counts": {}}
        
        color_counts = {"azul": 0, "morado": 0, "amarillo": 0}
        for result in self.results_history:
            color_counts[result["color"]] += 1
        
        total = len(self.results_history)
        percentages = {
            color: round((count / total) * 100, 2) if total > 0 else 0
            for color, count in color_counts.items()
        }
        
        return {
            "total_spins": self.spin_count,
            "results_shown": len(self.results_history),
            "color_counts": color_counts,
            "percentages": percentages,
            "spins_since_last_purple": self.spin_count - self.last_purple_spin,
            "spins_since_last_yellow": self.spin_count - self.last_yellow_spin
        }

# Instancia global del juego
game = RuletaGame()

@app.route('/')
def serve_frontend():
    """Servir el frontend"""
    return send_file('static/index.html')

@app.route('/api/spin', methods=['POST'])
def spin_roulette():
    """Realizar un giro de la ruleta"""
    try:
        result = game.spin()
        return jsonify({
            "success": True,
            "result": result,
            "statistics": game.get_statistics()
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """Obtener historial de resultados"""
    return jsonify({
        "success": True,
        "history": game.results_history,
        "statistics": game.get_statistics()
    })

@app.route('/api/reset', methods=['POST'])
def reset_game():
    """Reiniciar el juego"""
    global game
    game = RuletaGame()
    return jsonify({
        "success": True,
        "message": "Juego reiniciado"
    })

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Obtener estadísticas del juego"""
    return jsonify({
        "success": True,
        "statistics": game.get_statistics()
    })

@app.route('/api/colors', methods=['GET'])
def get_colors():
    """Obtener información de colores y probabilidades"""
    return jsonify({
        "success": True,
        "colors": game.colors
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "OK",
        "message": "Servidor de Ruleta funcionando",
        "endpoints": {
            "POST /api/spin": "Girar la ruleta",
            "GET /api/history": "Obtener historial",
            "GET /api/statistics": "Obtener estadísticas",
            "POST /api/reset": "Reiniciar juego",
            "GET /api/colors": "Obtener información de colores"
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
