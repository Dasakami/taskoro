// JavaScript animations for Magic RPG Tracker

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize scroll reveal animations
    initScrollReveal();
    
    // Initialize magic particles effect
    initMagicParticles();
    
    // Add glow effects to certain elements
    initGlowEffects();
    
    // Initialize progress bars
    initProgressBars();
});

// Scroll reveal animation
function initScrollReveal() {
    const elements = document.querySelectorAll('.reveal');
    
    function checkReveal() {
        elements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (elementTop < windowHeight - 100) {
                element.classList.add('active');
            }
        });
    }
    
    // Check elements on load
    checkReveal();
    
    // Check elements on scroll
    window.addEventListener('scroll', checkReveal);
}

// Magic particles effect
function initMagicParticles() {
    const particlesContainer = document.querySelector('.magic-particles');
    if (!particlesContainer) return;
    
    // Create particles
    const particleCount = 50;
    
    for (let i = 0; i < particleCount; i++) {
        createParticle(particlesContainer);
    }
    
    // Continue creating particles at intervals
    setInterval(() => {
        createParticle(particlesContainer);
    }, 300);
}

function createParticle(container) {
    const particle = document.createElement('div');
    particle.classList.add('magic-particle');
    
    // Random position
    const posX = Math.random() * window.innerWidth;
    const posY = Math.random() * window.innerHeight;
    
    // Random size
    const size = Math.random() * 5 + 1;
    
    // Random color
    const colors = ['#6633ff', '#33ccff', '#ff3366', '#33ffcc'];
    const color = colors[Math.floor(Math.random() * colors.length)];
    
    // Set styles
    particle.style.cssText = `
        position: absolute;
        top: ${posY}px;
        left: ${posX}px;
        width: ${size}px;
        height: ${size}px;
        background-color: ${color};
        border-radius: 50%;
        pointer-events: none;
        opacity: 0;
        filter: blur(1px);
        box-shadow: 0 0 6px ${color};
        animation: magic-particle ${Math.random() * 3 + 2}s ease-out forwards;
    `;
    
    container.appendChild(particle);
    
    // Remove particle after animation completes
    setTimeout(() => {
        particle.remove();
    }, 5000);
}

// Add glow effects to elements
function initGlowEffects() {
    // Add glow to buttons on hover
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('mouseenter', (e) => {
            e.currentTarget.classList.add('glow');
        });
        
        btn.addEventListener('mouseleave', (e) => {
            e.currentTarget.classList.remove('glow');
        });
    });
    
    // Add magic aura to special elements
    document.querySelectorAll('.special-item, .legendary-item').forEach(item => {
        item.classList.add('magic-aura');
    });
}

// Initialize progress bars
function initProgressBars() {
    document.querySelectorAll('.progress-bar').forEach(bar => {
        const value = bar.getAttribute('data-value') || '0';
        const max = bar.getAttribute('data-max') || '100';
        const percent = (parseInt(value) / parseInt(max)) * 100;
        
        // Animate progress bar filling
        setTimeout(() => {
            bar.style.width = `${percent}%`;
        }, 300);
    });
}

// Task completion animation
function completeTask(taskElement) {
    if (!taskElement) return;
    
    taskElement.classList.add('task-complete');
    
    // Add magic particles effect around the completed task
    const rect = taskElement.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    
    // Create particles
    for (let i = 0; i < 10; i++) {
        createMagicParticleAt(centerX, centerY);
    }
}

function createMagicParticleAt(x, y) {
    const particle = document.createElement('div');
    const container = document.querySelector('.magic-particles');
    if (!container) return;
    
    // Random size and direction
    const size = Math.random() * 8 + 2;
    const angle = Math.random() * Math.PI * 2;
    const distance = Math.random() * 50 + 20;
    const duration = Math.random() * 1 + 0.5;
    
    // Calculate end position
    const endX = Math.cos(angle) * distance;
    const endY = Math.sin(angle) * distance;
    
    // Random color
    const colors = ['#6633ff', '#33ccff', '#ff3366', '#33ffcc'];
    const color = colors[Math.floor(Math.random() * colors.length)];
    
    // Set styles
    particle.style.cssText = `
        position: fixed;
        top: ${y}px;
        left: ${x}px;
        width: ${size}px;
        height: ${size}px;
        background-color: ${color};
        border-radius: 50%;
        pointer-events: none;
        opacity: 0;
        filter: blur(1px);
        box-shadow: 0 0 6px ${color};
        transform: translate(-50%, -50%);
        z-index: 9999;
    `;
    
    container.appendChild(particle);
    
    // Animate particle
    gsap.to(particle, {
        x: endX,
        y: endY,
        opacity: 0.8,
        duration: duration / 2,
        ease: "power1.out",
        onComplete: () => {
            gsap.to(particle, {
                opacity: 0,
                duration: duration / 2,
                ease: "power1.in",
                onComplete: () => {
                    particle.remove();
                }
            });
        }
    });
}

// Shake animation for chests and rewards
function shakeElement(element) {
    if (!element) return;
    element.classList.add('shake');
    
    // Remove class after animation completes
    setTimeout(() => {
        element.classList.remove('shake');
    }, 500);
}

// Typing effect for important messages
function typeWriter(element, text, speed = 50) {
    if (!element) return;
    
    element.classList.add('typing-effect');
    element.textContent = '';
    
    let i = 0;
    const typing = setInterval(() => {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
        } else {
            clearInterval(typing);
            element.classList.remove('typing-effect');
        }
    }, speed);
}