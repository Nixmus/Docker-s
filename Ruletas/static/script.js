// Rutas de las canciones (archivos locales en static/)
const AUDIO_TRACKS = [
    '/static/thank-you-for-your-generous-purchase-dori-theme.mp3',
    '/static/whirling-of-vairambhaka.mp3'
];

class AudioManager {
    constructor() {
        this.audio1 = document.getElementById('audio1');
        this.audio2 = document.getElementById('audio2');
        this.playBtn = document.getElementById('playBtn');
        this.muteBtn = document.getElementById('muteBtn');
        this.volumeSlider = document.getElementById('volumeSlider');
        this.volumeLabel = document.getElementById('volumeLabel');
        
        this.currentTrackIndex = 0;
        this.isMuted = false;
        this.isPlaying = false;
        this.volume = 0.5;
        
        this.setupAudio();
        this.bindEvents();
    }
    
    setupAudio() {
        console.log('=== Iniciando AudioManager ===');
        
        // Configurar etiquetas de audio con rutas
        this.audio1.src = AUDIO_TRACKS[0];
        this.audio2.src = AUDIO_TRACKS[1];
        
        console.log('Track 1:', AUDIO_TRACKS[0]);
        console.log('Track 2:', AUDIO_TRACKS[1]);
        
        // Volumen inicial
        this.audio1.volume = this.volume;
        this.audio2.volume = this.volume;
        
        // Event: cuando termina audio 1
        this.audio1.addEventListener('ended', () => {
            console.log('✓ Canción 1 terminada, iniciando canción 2');
            this.playTrack(1);
        });
        
        // Event: cuando termina audio 2
        this.audio2.addEventListener('ended', () => {
            console.log('✓ Canción 2 terminada, iniciando canción 1');
            this.playTrack(0);
        });
        
        // Event: error en audio 1
        this.audio1.addEventListener('error', (e) => {
            console.error('❌ Error en canción 1:', e);
            console.log('Código de error:', this.audio1.error?.code);
        });
        
        // Event: error en audio 2
        this.audio2.addEventListener('error', (e) => {
            console.error('❌ Error en canción 2:', e);
            console.log('Código de error:', this.audio2.error?.code);
        });
        
        // Event: cuando está cargada
        this.audio1.addEventListener('canplay', () => {
            console.log('✓ Canción 1 lista para reproducir');
        });
        
        this.audio2.addEventListener('canplay', () => {
            console.log('✓ Canción 2 lista para reproducir');
        });
        
        console.log('AudioManager configurado');
    }
    
    bindEvents() {
        this.playBtn.addEventListener('click', () => this.togglePlay());
        this.muteBtn.addEventListener('click', () => this.toggleMute());
        this.volumeSlider.addEventListener('input', (e) => this.setVolume(e.target.value));
    }
    
    togglePlay() {
        if (this.isPlaying) {
            this.stopMusic();
        } else {
            this.playTrack(0);
        }
    }
    
    playTrack(index) {
        this.currentTrackIndex = index;
        const audioElement = index === 0 ? this.audio1 : this.audio2;
        const otherAudio = index === 0 ? this.audio2 : this.audio1;
        const trackName = AUDIO_TRACKS[index].split('/').pop();
        
        console.log(`▶️ Reproduciendo: ${trackName}`);
        
        // Pausar la otra
        otherAudio.pause();
        otherAudio.currentTime = 0;
        
        // Reproducir la actual
        audioElement.currentTime = 0;
        
        const playPromise = audioElement.play();
        
        if (playPromise !== undefined) {
            playPromise
                .then(() => {
                    console.log('✓ Reproducción iniciada');
                    this.isPlaying = true;
                    this.updatePlayBtn();
                })
                .catch(error => {
                    console.error('❌ Error al reproducir:', error.name, error.message);
                });
        }
    }
    
    stopMusic() {
        console.log('⏹️ Deteniendo música');
        this.audio1.pause();
        this.audio2.pause();
        this.isPlaying = false;
        this.updatePlayBtn();
    }
    
    updatePlayBtn() {
        const icon = this.playBtn.querySelector('.play-icon');
        if (this.isPlaying) {
            icon.textContent = '⏸️';
            this.playBtn.title = 'Pausar música';
        } else {
            icon.textContent = '▶️';
            this.playBtn.title = 'Reproducir música';
        }
    }
    
    toggleMute() {
        this.isMuted = !this.isMuted;
        
        if (this.isMuted) {
            this.audio1.muted = true;
            this.audio2.muted = true;
            this.muteBtn.classList.add('muted');
            this.muteBtn.querySelector('.speaker-icon').textContent = '🔇';
            console.log('🔇 Muteado');
        } else {
            this.audio1.muted = false;
            this.audio2.muted = false;
            this.muteBtn.classList.remove('muted');
            this.muteBtn.querySelector('.speaker-icon').textContent = '🔊';
            console.log('🔊 Desmuted');
        }
    }
    
    setVolume(value) {
        this.volume = value / 100;
        this.audio1.volume = this.volume;
        this.audio2.volume = this.volume;
        this.volumeLabel.textContent = `${value}%`;
        
        console.log(`🔊 Volumen: ${value}%`);
        
        // Cambiar icono
        if (value == 0) {
            this.muteBtn.querySelector('.speaker-icon').textContent = '🔇';
        } else if (value < 33) {
            this.muteBtn.querySelector('.speaker-icon').textContent = '🔈';
        } else if (value < 66) {
            this.muteBtn.querySelector('.speaker-icon').textContent = '🔉';
        } else {
            this.muteBtn.querySelector('.speaker-icon').textContent = '🔊';
        }
    }
}

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
        
        // Ángulos de cada resultado (coinciden con el conic-gradient en CSS)
        this.ANGLES = {
            3: { center: 2.88, range: 5.76 },      // amarillo: 0° - 5.76°
            2: { center: 29.16, range: 46.80 },    // morado: 5.76° - 52.56°
            1: { center: 206.28, range: 307.44 }   // azul: 52.56° - 360°
        };
        
        this.ANIMATION_DURATION = 2500; // ms
        this.FAST_SPIN_DURATION = 400;  // ms para spins rápidos en spin10
        this.FULL_SPINS = 3; // Vueltas completas por giro
        
        this.bindEvents();
        this.loadHistory();
    }
    
    bindEvents() {
        this.spinBtn.addEventListener('click', () => this.spinMultiple(1));
        this.spin10Btn.addEventListener('click', () => this.spinMultiple(10));
        this.resetBtn.addEventListener('click', () => this.reset());
    }
    
    async spinMultiple(count) {
        if (this.isSpinning) return;
        
        this.isSpinning = true;
        this.spinBtn.disabled = true;
        this.spin10Btn.disabled = true;
        
        const isBulkSpin = count > 1;
        const btnToUpdate = isBulkSpin ? this.spin10Btn : this.spinBtn;
        const originalText = btnToUpdate.textContent;
        
        try {
            for (let i = 0; i < count; i++) {
                const isLastSpin = i === count - 1;
                
                if (isBulkSpin) {
                    btnToUpdate.textContent = `GIRANDO ${i + 1}/10...`;
                } else {
                    btnToUpdate.textContent = 'GIRANDO...';
                }
                
                const response = await fetch('/api/spin', {
                    method: 'POST'
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Animar con duración diferente según si es último giro
                    const duration = isLastSpin ? this.ANIMATION_DURATION : this.FAST_SPIN_DURATION;
                    await this.animateSpin(data.result.result, duration, isLastSpin);
                    
                    this.updateResult(data.result);
                    this.updateStats(data.statistics);
                    this.addToHistory(data.result);
                }
            }
        } catch (error) {
            console.error('Error al girar:', error);
            alert('Error al conectar con el servidor');
        }
        
        this.isSpinning = false;
        this.spinBtn.disabled = false;
        this.spin10Btn.disabled = false;
        btnToUpdate.textContent = originalText;
    }
    
    animateSpin(result, duration = this.ANIMATION_DURATION, isMainSpin = true) {
        return new Promise((resolve) => {
            const resultData = this.ANGLES[result];
            
            // Calcular ángulo objetivo con variación
            const angleVariation = isMainSpin ? (Math.random() * 10 - 5) : 0;
            const targetAngle = resultData.center + angleVariation;
            
            // Número de vueltas completas
            const fullSpins = isMainSpin ? (this.FULL_SPINS + Math.random() * 2) : 1;
            
            // Rotación total = rotación actual + vueltas + ajuste para llegar al ángulo
            const totalRotation = this.currentRotation + (360 * fullSpins) + (360 - targetAngle);
            
            // Agregar clase de animación
            this.roulette.classList.add('spinning');
            
            // Aplicar transición con duración dinámica
            this.roulette.style.transition = `transform ${duration}ms cubic-bezier(0.17, 0.67, 0.12, 0.99)`;
            this.roulette.style.transform = `rotate(${totalRotation}deg)`;
            
            // Guardar rotación actual para el próximo giro
            this.currentRotation = totalRotation % 360;
            
            setTimeout(() => {
                this.roulette.classList.remove('spinning');
                resolve();
            }, duration);
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
    // Inicializar gestión de audio
    const audioManager = new AudioManager();
    
    // Inicializar ruleta
    new RuletaApp();
});
