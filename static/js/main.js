// ── Banner slider automático ──────────────────────────────────────
document.addEventListener('DOMContentLoaded', function() {
    const slider = document.getElementById('heroSlider');
    if (!slider) return;

    const slides = slider.querySelectorAll('.hero-slide');
    if (slides.length <= 1) return;

    let current = 0;

    setInterval(function() {
        slides[current].classList.remove('active');
        current = (current + 1) % slides.length;
        slides[current].classList.add('active');
    }, 5000);
});


// ── Cartazes laterais: prender dentro da área branca ──────────────
// Os cartazes ficam fixos, mas nunca podem invadir a faixa azul do topo
// (cabeçalho + banner + texto da home) nem o rodapé azul. Este código
// mede, a cada rolagem, onde começa e termina a área branca visível e
// posiciona os cartazes exatamente nesse intervalo.
(function() {
    const colunas = document.querySelectorAll('.cartazes-lateral');
    if (!colunas.length) return;

    const header = document.querySelector('.header');
    const footer = document.querySelector('.footer');
    // Último bloco azul antes do conteúdo branco (texto da home ou banner)
    const azulFinal = document.querySelector('.home-intro') ||
                      document.querySelector('.hero');
    const GAP = 12;

    function ajustar() {
        // Em telas <=1400px os cartazes usam o botão flutuante; deixa o CSS cuidar
        if (window.innerWidth <= 1400) {
            colunas.forEach(function(c) {
                c.style.top = '';
                c.style.bottom = '';
                c.style.maxHeight = '';
                c.style.display = '';
            });
            return;
        }

        const headerBottom = header ? header.getBoundingClientRect().bottom : 0;
        const azulBottom = azulFinal ? azulFinal.getBoundingClientRect().bottom : 0;
        const footerTop = footer ? footer.getBoundingClientRect().top : window.innerHeight;

        const topo = Math.max(headerBottom, azulBottom) + GAP;
        const base = Math.min(window.innerHeight, footerTop) - GAP;
        const altura = Math.max(0, base - topo);

        colunas.forEach(function(c) {
            c.style.top = topo + 'px';
            c.style.bottom = 'auto';
            c.style.maxHeight = altura + 'px';
            // Se a área branca visível ficou pequena demais, esconde
            c.style.display = altura < 90 ? 'none' : 'flex';
        });
    }

    window.addEventListener('scroll', ajustar, { passive: true });
    window.addEventListener('resize', ajustar);
    document.addEventListener('DOMContentLoaded', ajustar);
    window.addEventListener('load', ajustar);
    ajustar();
})();
