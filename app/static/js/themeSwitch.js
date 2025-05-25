function switchTheme(themeName) {
    const themeLink = document.getElementById('theme-style');
    themeLink.href = `/static/css/${themeName}/colorPalette.css`;
    localStorage.setItem('theme', themeName);
}

window.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme') || 'theme-default';
    switchTheme(savedTheme);
});