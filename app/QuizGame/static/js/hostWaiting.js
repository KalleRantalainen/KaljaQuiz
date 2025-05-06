
async function fetchPlayers() {
    const res = await fetch("/players");
    if (!res.ok) return;
    const names = await res.json();
    const ul = document.getElementById("players-list");
    ul.innerHTML = "";

    if (names.length === 0) {
        ul.innerHTML = "<li><em>(no one yet)</em></li>";
    } else {
        for (const n of names) {
            const li = document.createElement("li");
            li.textContent = n;
            ul.appendChild(li);
        }
    }
}

// poll every 2s
setInterval(fetchPlayers, 2000);
fetchPlayers();
