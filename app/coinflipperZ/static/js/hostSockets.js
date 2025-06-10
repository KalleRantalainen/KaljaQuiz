function loadView(viewName) {
    fetch(`/coinflip/${viewName}`)
    .then(response => response.text())
    .then(html => {
        document.getElementById('main-container').innerHTML = html;
    });
}

window.addEventListener("DOMContentLoaded", () => {
    // Heti kun host valitsee coinflipin ja host_view.html on
    // renderöity, niin täytetään main-container waiting partialilla.
    loadView("waiting_players");
});
