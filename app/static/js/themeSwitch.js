function switchTheme(themeName) {
    const themeLink = document.getElementById('theme-style');
    themeLink.href = `/static/css/${themeName}/colorPalette.css`;
    localStorage.setItem('theme', themeName);
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