function switchTheme(themeName) {
    const themeLink = document.getElementById('theme-style');
    themeLink.href = `/static/css/${themeName}/colorPalette.css`;
    localStorage.setItem('theme', themeName);
    // Ladataan animaatio dynaamisesti
    loadAnimationScript(themeName);
}

/*Ladataan animaation scripti dynaamisesti, ei pelkästää kun page päivitetään*/
function loadAnimationScript(themeName) {
    // Poistetaan olemassa oleva animaation script jos on
    const existingScript = document.getElementById('animation-script');
    if (existingScript) {
        existingScript.remove();
    }

    // Luodaan uusi scripti elementti uudella animaatio polulla
    const script = document.createElement('script');
    script.id = 'animation-script';
    script.src = `/static/js/themes/${themeName}/bgAnimation.js`;

    // Jos teemalle ei ole omaa animaatiota, käytetään default
    script.onerror = () => {
        console.warn(`Animation for theme ${themeName} not found, loading default animation.`);
        script.remove();
        loadAnimationScript('theme-default');
    };

    // Tykitetään bodyyn scripti tägi
    document.body.appendChild(script);
}

window.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme') || 'theme-default';
    switchTheme(savedTheme);

    // Set the select element's value to match the saved theme
    const themeSelector = document.querySelector('.dropdown');
    if (themeSelector) {
        themeSelector.value = savedTheme;
    }
});