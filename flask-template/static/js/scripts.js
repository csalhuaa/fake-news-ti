
        // Create animated particles
        function createParticles() {
            const particlesContainer = document.getElementById('particles');
            const particleCount = 50;

            for (let i = 0; i < particleCount; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.animationDelay = Math.random() * 15 + 's';
                particle.style.animationDuration = (Math.random() * 10 + 10) + 's';
                particlesContainer.appendChild(particle);
            }
        }

        // Mejorar la animación de carga
        function showLoadingAnimation() {
            const loading = document.getElementById('loading');
            loading.innerHTML = `
                <div class="loading-container">
                    <div class="loading-spinner">
                        <div class="spinner-ring"></div>
                        <div class="spinner-ring"></div>
                        <div class="spinner-ring"></div>
                    </div>
                    <p class="loading-text">Analizando con IA...</p>
                    <div class="loading-dots">
                        <span></span><span></span><span></span>
                    </div>
                </div>
            `;
            loading.style.display = 'block';
        }

        // Form submission handler
        document.getElementById('analysisForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const form = e.target;
            const formData = new FormData(form);
            const analyzeBtn = document.getElementById('analyzeBtn');
            const loading = document.getElementById('loading');
            const results = document.getElementById('results');
            
            // Validar límites de caracteres antes de enviar
            const title = formData.get('title');
            const description = formData.get('description');
            
            if (title.length > 200) {
                const errorCard = document.createElement('div');
                errorCard.className = 'error-card';
                errorCard.innerHTML = `
                    <div class="result-title">
                        <i class="fas fa-exclamation-circle"></i>
                        Error de Validación
                    </div>
                    <div class="result-content">
                        <strong>❌ Error:</strong> El título no puede exceder 200 caracteres
                    </div>
                `;
                results.innerHTML = '';
                results.appendChild(errorCard);
                results.style.display = 'block';
                return;
            }
            
            if (description.length > 8000) {
                const errorCard = document.createElement('div');
                errorCard.className = 'error-card';
                errorCard.innerHTML = `
                    <div class="result-title">
                        <i class="fas fa-exclamation-circle"></i>
                        Error de Validación
                    </div>
                    <div class="result-content">
                        <strong>❌ Error:</strong> El contenido no puede exceder 8000 caracteres
                    </div>
                `;
                results.innerHTML = '';
                results.appendChild(errorCard);
                results.style.display = 'block';
                return;
            }
            
            // Show loading state
            analyzeBtn.disabled = true;
            analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analizando...';
            showLoadingAnimation(); // Usar la nueva función
            results.style.display = 'none';
            
            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Show results
                    const resultCard = document.createElement('div');
                    resultCard.className = `result-card ${data.es_verdadera ? 'real-news' : 'fake-news'}`;
                    
                    const icon = data.es_verdadera ? 'fas fa-check-circle' : 'fas fa-exclamation-triangle';
                    const status = data.es_verdadera ? 'NOTICIA PROBABLEMENTE VERDADERA' : 'NOTICIA PROBABLEMENTE FALSA';
                    const statusIcon = data.es_verdadera ? '✅' : '⚠️';
                    
                    let detailHTML = '';
                    if (data.modelo_usado === 'both' && data.resultados_detalle.length > 1) {
                        detailHTML = `
                            <div class="result-detail">
                                <strong>Análisis detallado:</strong>
                                ${data.resultados_detalle.map(resultado => `
                                    <div class="model-result">
                                        <strong>${resultado.modelo}:</strong> ${resultado.prediccion} (${resultado.confianza}%)
                                    </div>
                                `).join('')}
                            </div>
                        `;
                    }
                    
                    resultCard.innerHTML = `
                        <div class="result-title">
                            <i class="${icon}"></i>
                            Resultado del Análisis
                        </div>
                        <div class="result-content">
                            <strong>${statusIcon} ${status}</strong><br>
                            <strong>Confianza:</strong> ${data.confianza}%<br>
                            <strong>Modelo usado:</strong> ${data.modelo_usado.toUpperCase()}<br>
                            <strong>Texto analizado:</strong> "${data.texto_analizado}"
                            ${detailHTML}
                        </div>
                    `;
                    
                    results.innerHTML = '';
                    results.appendChild(resultCard);
                    results.style.display = 'block';
                    
                } else {
                    // Show error
                    const errorCard = document.createElement('div');
                    errorCard.className = 'error-card';
                    
                    let errorMessage = data.error;
                    let actionButton = '';
                    
                    // Si es error de autenticación, mostrar botón de login
                    if (response.status === 403 && data.error.includes('iniciar sesión')) {
                        errorMessage = 'Para usar el modelo SaBERT, debes iniciar sesión.';
                        actionButton = '<a href="/login" class="auth-btn" style="display: inline-flex; margin-top: 1rem;"><i class="fas fa-sign-in-alt"></i> Iniciar Sesión</a>';
                    }
                    
                    errorCard.innerHTML = `
                        <div class="result-title">
                            <i class="fas fa-exclamation-circle"></i>
                            Error en el Análisis
                        </div>
                        <div class="result-content">
                            <strong>❌ Error:</strong> ${errorMessage}
                            ${actionButton}
                        </div>
                    `;
                    
                    results.innerHTML = '';
                    results.appendChild(errorCard);
                    results.style.display = 'block';
                }
                
            } catch (error) {
                console.error('Error:', error);
                
                const errorCard = document.createElement('div');
                errorCard.className = 'error-card';
                errorCard.innerHTML = `
                    <div class="result-title">
                        <i class="fas fa-exclamation-circle"></i>
                        Error de Conexión
                    </div>
                    <div class="result-content">
                        <strong>❌ Error:</strong> No se pudo conectar con el servidor. Por favor, inténtalo de nuevo.
                    </div>
                `;
                
                results.innerHTML = '';
                results.appendChild(errorCard);
                results.style.display = 'block';
            } finally {
                // Reset button state
                analyzeBtn.disabled = false;
                analyzeBtn.innerHTML = '<i class="fas fa-search"></i> Analizar Noticia';
                loading.style.display = 'none';
            }
        });

        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // Initialize particles when page loads
        window.addEventListener('load', function() {
            createParticles();
        });

        // Add floating animation to feature items
        const featureItems = document.querySelectorAll('.feature-item');
        featureItems.forEach((item, index) => {
            item.style.animationDelay = `${index * 0.2}s`;
        });

        // Add typing effect to hero title (optional enhancement)
        function typeWriter(element, text, speed = 100) {
            let i = 0;
            element.innerHTML = '';
            
            function type() {
                if (i < text.length) {
                    element.innerHTML += text.charAt(i);
                    i++;
                    setTimeout(type, speed);
                }
            }
            
            type();
        }

        // Optional: Add typing effect to hero title
        // Uncomment the following lines if you want a typing effect:
        /*
        window.addEventListener('load', function() {
            const heroTitle = document.querySelector('.hero-title');
            const originalText = heroTitle.textContent;
            typeWriter(heroTitle, originalText, 100);
        });
        */

        // Agregar contador de caracteres
        function addCharacterCounter() {
            const description = document.getElementById('description');
            const title = document.getElementById('title');
            
            if (description) {
                const counter = document.createElement('div');
                counter.className = 'char-counter';
                description.parentNode.appendChild(counter);
                
                function updateCounter() {
                    const count = description.value.length;
                    const max = 8000;
                    const percentage = (count / max) * 100;
                    
                    counter.textContent = `${count}/${max} caracteres`;
                    
                    // Cambiar color según el porcentaje
                    counter.classList.remove('warning', 'error');
                    if (percentage > 90) {
                        counter.classList.add('error');
                    } else if (percentage > 75) {
                        counter.classList.add('warning');
                    }
                }
                
                description.addEventListener('input', updateCounter);
                updateCounter();
            }
            
            if (title) {
                const counter = document.createElement('div');
                counter.className = 'char-counter';
                title.parentNode.appendChild(counter);
                
                function updateCounter() {
                    const count = title.value.length;
                    const max = 200;
                    const percentage = (count / max) * 100;
                    
                    counter.textContent = `${count}/${max} caracteres`;
                    
                    // Cambiar color según el porcentaje
                    counter.classList.remove('warning', 'error');
                    if (percentage > 90) {
                        counter.classList.add('error');
                    } else if (percentage > 75) {
                        counter.classList.add('warning');
                    }
                }
                
                title.addEventListener('input', updateCounter);
                updateCounter();
            }
        }

        // Llamar la función cuando se carga la página
        window.addEventListener('load', function() {
            createParticles();
            addCharacterCounter();
        });

        // Agregar funcionalidad de limpiar formulario
        document.getElementById('clearBtn').addEventListener('click', function() {
            document.getElementById('analysisForm').reset();
            document.getElementById('results').style.display = 'none';
            document.getElementById('loading').style.display = 'none';
            
            // Actualizar contadores
            const counters = document.querySelectorAll('.char-counter');
            counters.forEach(counter => {
                const input = counter.previousElementSibling;
                if (input && input.tagName === 'INPUT' || input.tagName === 'TEXTAREA') {
                    const count = input.value.length;
                    const max = input.tagName === 'TEXTAREA' ? 8000 : 200;
                    counter.textContent = `${count}/${max} caracteres`;
                    counter.classList.remove('warning', 'error');
                }
            });
        });

        // Mejorar navegación por teclado
        document.addEventListener('keydown', function(e) {
            // Ctrl+Enter para enviar formulario
            if (e.ctrlKey && e.key === 'Enter') {
                const form = document.getElementById('analysisForm');
                if (form) {
                    form.dispatchEvent(new Event('submit'));
                }
            }
            
            // Escape para limpiar formulario
            if (e.key === 'Escape') {
                const clearBtn = document.getElementById('clearBtn');
                if (clearBtn) {
                    clearBtn.click();
                }
            }
        });

        // Agregar focus visible para accesibilidad
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Tab') {
                document.body.classList.add('keyboard-navigation');
            }
        });

        document.addEventListener('mousedown', function() {
            document.body.classList.remove('keyboard-navigation');
        });