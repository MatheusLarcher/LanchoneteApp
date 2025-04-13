// app/static/js/script.js

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips do Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-dismiss para alertas
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert:not(.alert-persistent)');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Adicionar animação aos cards
    const animateCards = () => {
        const cards = document.querySelectorAll('.card');
        cards.forEach((card, index) => {
            setTimeout(() => {
                card.classList.add('fade-in');
            }, index * 100);
        });
    };

    // Aplicar animação se houver cards na página
    if (document.querySelectorAll('.card').length > 0) {
        animateCards();
    }

    // Validação personalizada para formulários
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Formatação de inputs telefone
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            
            if (value.length <= 11) {
                if (value.length > 2) {
                    value = '(' + value.substring(0, 2) + ') ' + value.substring(2);
                }
                if (value.length > 10) {
                    value = value.substring(0, 10) + '-' + value.substring(10);
                }
            }
            
            e.target.value = value;
        });
    });

    // Efeito de scroll suave para links internos
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Botão Voltar ao Topo
    const createBackToTopButton = () => {
        const body = document.querySelector('body');
        const button = document.createElement('button');
        button.innerHTML = '<i class="fas fa-arrow-up"></i>';
        button.className = 'btn btn-primary btn-back-to-top';
        button.id = 'back-to-top';
        button.style.position = 'fixed';
        button.style.bottom = '20px';
        button.style.right = '20px';
        button.style.display = 'none';
        button.style.zIndex = '1000';
        button.style.width = '40px';
        button.style.height = '40px';
        button.style.borderRadius = '50%';
        
        button.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
        
        body.appendChild(button);
        
        window.addEventListener('scroll', () => {
            if (window.scrollY > 300) {
                button.style.display = 'block';
            } else {
                button.style.display = 'none';
            }
        });
    };
    
    createBackToTopButton();
});

// Função para atualizar o carrinho via AJAX (exemplo futuro)
function updateCart(productId, quantity) {
    console.log(`Produto ${productId} atualizado para quantidade ${quantity}`);
    // Aqui poderia ter uma implementação AJAX para atualizar sem recarregar a página
}

// Função para verificar se uma imagem existe
function checkImage(imageSrc, successCallback, errorCallback) {
    const img = new Image();
    img.onload = successCallback;
    img.onerror = errorCallback;
    img.src = imageSrc;
}

// Função para formatar valores monetários 
function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}