// Adapted from the Academic Project Page Template
// (https://github.com/eliahuhorwitz/Academic-project-page-template, CC BY-SA 4.0).
// This page has no carousel, slider or "More Works" menu, so only the BibTeX
// copy button and the scroll-to-top button are kept.

function copyBibTeX() {
    const bibtexElement = document.getElementById('bibtex-code');
    const button = document.querySelector('.copy-bibtex-btn');
    const copyText = button.querySelector('.copy-text');
    const done = function () {
        button.classList.add('copied');
        copyText.textContent = 'Cop';
        setTimeout(function () {
            button.classList.remove('copied');
            copyText.textContent = 'Copy';
        }, 2000);
    };
    const fallback = function () {
        const textArea = document.createElement('textarea');
        textArea.value = bibtexElement.textContent;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        done();
    };
    if (!bibtexElement) return;
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(bibtexElement.textContent).then(done, fallback);
    } else {
        fallback();
    }
}

function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

window.addEventListener('scroll', function () {
    const scrollButton = document.querySelector('.scroll-to-top');
    if (!scrollButton) return;
    if (window.pageYOffset > 300) {
        scrollButton.classList.add('visible');
    } else {
        scrollButton.classList.remove('visible');
    }
});
