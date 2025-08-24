class RuletaApp {
    constructor() {
        this.spinBtn = document.getElementById('spinBtn');
        this.spin10Btn = document.getElementById('spin10Btn');
        this.resetBtn = document.getElementById('resetBtn');
        this.roulette = document.getElementById('roulette');
        this.lastResult = document.getElementById('lastResult');
        this.historyBody = document.getElementById('historyBody');
        
        this.isSpinning = false;
        this.currentRotation = 0;
        
        this.bindEvents();
        this.loadHistory();
    }
    
    bindEvents() {
        this.spinBtn.addEventListener('click', () => this.spin());
        this.spin10Btn.addEventListener('click', () => this.spin10());
        this.resetBtn.addEventListener('click', () => this.reset());
    }
    
    async spin() {
        if (this.isSpinning) return;
        
        this.isSpinning = true;
        this.spinBtn.disabled = true;
        this.spin10Btn.disabled = true;
        this.spinBtn.textContent = 'GIRANDO...';
        
        try {
            const response = await fetch('/api/spin', {
                method: 'POST'
            });
            
            const data = await response.json();
            
            if (data.success) {
                await this.animateSpin(data.result.result);
                this.updateResult(data.result);
                this.updateStats(data.statistics);
                this.addToHistory(data.result);
            }
        } catch (error) {
            console.error('Error al girar:', error);
            alert('Error al conectar con el servidor');
        }
        
        this.isSpinning = false;
        this.spinBtn.disabled = false;
        this.spin10Btn.disabled = false;
        this.spinBtn.textContent = 'GIRAR RULETA';
    }
    
    async spin10() {
        if (this.isSpinning) return;
        
        this.isSpinning = true;
        this.spinBtn.disabled = true;
        this.spin10Btn.disabled = true;
        this.spin10Btn.textContent = 'GIRANDO 10...';
        
        try {
            for (let i = 0; i < 10; i++) {
                const response = await fetch('/api/spin', {
                    method: 'POST'
                });
                
                const data = await response.json();
                
                if (data.success) {
                    if (i === 9) { // Solo animar el último giro
                        await this.animateSpin(data.result.result);
                    }
                    this.updateResult(data.result);
                    this.updateStats(data.statistics);
                    this.addToHistory(data.result);
                    
                    // Pequeña pausa entre giros
                    if (i < 9) await new Promise(resolve => setTimeout(resolve, 100));
                }
            }
        } catch (error) {
            console.error('Error al girar 10:', error);
            alert('Error al conectar con el servidor');
        }
        
        this.isSpinning = false;
        this.spinBtn.disabled = false;
        this.spin10Btn.disabled = false;
        this.spin10Btn.textContent = 'TIRAR 10';
    }
    
    animateSpin(result) {
        return new Promise((resolve) => {
            // Ángulos corregidos para que coincidan con el diseño de la ruleta
            const angles = {
                3: 2.88,    // amarillo: 0° - 5.76°
                2: 29.16,   // morado: 5.76° - 52.56°
                1: 180      // azul: 52.56° - 360° (centro aproximado)
            };
            
            const targetAngle = angles[result] + (Math.random() * 10 - 5);
            const spins = 3 + Math.random() * 2; // 3-5 vueltas
            const totalRotation = this.currentRotation + (360 * spins) + (360 - targetAngle);
            
            this.roulette.style.transform = `rotate(${totalRotation}deg)`;
            this.currentRotation = totalRotation % 360;
            
            setTimeout(resolve, 2500);
        });
    }
    
    updateResult(result) {
        this.lastResult.textContent = `${result.result} - ${result.color.toUpperCase()}`;
        this.lastResult.className = `result-box ${result.color}`;
    }
    
    updateStats(stats) {
        document.getElementById('totalSpins').textContent = stats.total_spins;
        document.getElementById('blueCount').textContent = stats.color_counts.azul;
        document.getElementById('purpleCount').textContent = stats.color_counts.morado;
        document.getElementById('yellowCount').textContent = stats.color_counts.amarillo;
        document.getElementById('bluePercent').textContent = `${stats.percentages.azul}%`;
        document.getElementById('purplePercent').textContent = `${stats.percentages.morado}%`;
        document.getElementById('yellowPercent').textContent = `${stats.percentages.amarillo}%`;
    }
    
    addToHistory(result) {
        const row = document.createElement('tr');
        // Corregir zona horaria (restar 5 horas)
        const date = new Date(result.timestamp);
        const localDate = new Date(date.getTime() - (5 * 60 * 60 * 1000));
        const time = localDate.toLocaleTimeString();
        
        row.innerHTML = `
            <td>${result.spin_number}</td>
            <td><span class="color-${result.color}">${result.result} - ${result.color}</span></td>
            <td>${time}</td>
        `;
        
        this.historyBody.insertBefore(row, this.historyBody.firstChild);
        
        // Mantener solo los últimos 20 en la vista
        while (this.historyBody.children.length > 20) {
            this.historyBody.removeChild(this.historyBody.lastChild);
        }
    }
    
    async loadHistory() {
        try {
            const response = await fetch('/api/history');
            const data = await response.json();
            
            if (data.success) {
                this.updateStats(data.statistics);
                
                // Mostrar últimos 20 resultados
                const recentHistory = data.history.slice(-20).reverse();
                recentHistory.forEach(result => {
                    this.addToHistory(result);
                });
            }
        } catch (error) {
            console.error('Error al cargar historial:', error);
        }
    }
    
    async reset() {
        if (confirm('¿Estás seguro de que quieres reiniciar el juego?')) {
            try {
                const response = await fetch('/api/reset', {
                    method: 'POST'
                });
                
                const data = await response.json();
                
                if (data.success) {
                    location.reload();
                }
            } catch (error) {
                console.error('Error al reiniciar:', error);
                alert('Error al reiniciar el juego');
            }
        }
    }
}

// Inicializar la aplicación cuando se carga la página
document.addEventListener('DOMContentLoaded', () => {
    new RuletaApp();
});
