function changeThemeAndReload(themeName) {
    localStorage.setItem('theme', themeName);
    location.reload();
}

/* Apply theme and load animation on page load only */
function applySavedTheme() {
    const themeName = localStorage.getItem('theme') || 'theme-default';

    const themeLink = document.getElementById('theme-style');
    themeLink.href = `/static/css/${themeName}/colorPalette.css`;

    loadAnimationScript(themeName);

    // Set the select dropdown to reflect current theme
    const themeSelector = document.querySelector('.dropdown');
    if (themeSelector) {
        themeSelector.value = themeName;
    }
}

/* Load theme-specific animation script */
function loadAnimationScript(themeName) {
    const existingScript = document.getElementById('animation-script');
    if (existingScript) {
        existingScript.remove();
    }

    const script = document.createElement('script');
    script.id = 'animation-script';
    script.src = `/static/js/themes/${themeName}/bgAnimation.js`;

    script.onerror = () => {
        console.warn(`Animation for theme ${themeName} not found, loading default animation.`);
        script.remove();
        if (themeName !== 'theme-default') {
            loadAnimationScript('theme-default');
        }
    };

    document.body.appendChild(script);
}

window.addEventListener('DOMContentLoaded', () => {
    applySavedTheme();
});