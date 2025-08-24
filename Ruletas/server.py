from flask import Flask, jsonify, request, send_from_directory, send_file
from flask_cors import CORS
import random
import json
from datetime import datetime
import sqlite3
import os

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)


# --- SQLite integration ---
DB_PATH = os.path.join(os.path.dirname(__file__), 'giros.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS giros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        spin_number INTEGER,
        result INTEGER,
        color TEXT,
        timestamp TEXT
    )''')
    conn.commit()
    conn.close()

def insert_giro(spin_number, result, color, timestamp):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO giros (spin_number, result, color, timestamp) VALUES (?, ?, ?, ?)',
              (spin_number, result, color, timestamp))
    conn.commit()
    conn.close()

def get_giros(limit=100):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT spin_number, result, color, timestamp FROM giros ORDER BY id DESC LIMIT ?', (limit,))
    rows = c.fetchall()
    conn.close()
    # Return in ascending order
    return [
        {"spin_number": row[0], "result": row[1], "color": row[2], "timestamp": row[3]}
        for row in reversed(rows)
    ]

def get_total_spins():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM giros')
    total = c.fetchone()[0]
    conn.close()
    return total

def get_last_spin_number():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT MAX(spin_number) FROM giros')
    last = c.fetchone()[0]
    conn.close()
    return last or 0

def get_last_spin_by_color(color):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT spin_number FROM giros WHERE color = ? ORDER BY spin_number DESC LIMIT 1', (color,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else 0

class RuletaGame:
    def __init__(self):
        self.colors = {
            1: {"name": "azul", "probability": 85.4},
            2: {"name": "morado", "probability": 13.0},
            3: {"name": "amarillo", "probability": 1.6}
        }
        init_db()
        self.spin_count = get_last_spin_number()
        self.last_purple_spin = get_last_spin_by_color("morado")
        self.last_yellow_spin = get_last_spin_by_color("amarillo")

    def spin(self):
        self.spin_count += 1
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
            rand = random.uniform(0, 100)
            if rand <= 1.6:
                result = 3  # amarillo
                self.last_yellow_spin = self.spin_count
            elif rand <= 14.6:
                result = 2  # morado
                self.last_purple_spin = self.spin_count
            else:
                result = 1  # azul

        color = self.colors[result]["name"]
        timestamp = datetime.now().isoformat()
        spin_result = {
            "spin_number": self.spin_count,
            "result": result,
            "color": color,
            "timestamp": timestamp
        }
        insert_giro(self.spin_count, result, color, timestamp)
        return spin_result

    def get_statistics(self):
        history = get_giros(100)
        if not history:
            return {"total_spins": 0, "color_counts": {}}
        color_counts = {"azul": 0, "morado": 0, "amarillo": 0}
        for result in history:
            color_counts[result["color"]] += 1
        total = len(history)
        percentages = {
            color: round((count / total) * 100, 2) if total > 0 else 0
            for color, count in color_counts.items()
        }
        return {
            "total_spins": get_total_spins(),
            "results_shown": len(history),
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
    history = get_giros(100)
    return jsonify({
        "success": True,
        "history": history,
        "statistics": game.get_statistics()
    })

@app.route('/api/reset', methods=['POST'])
def reset_game():
    """Reiniciar el juego"""
    # Borrar la base de datos
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
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
