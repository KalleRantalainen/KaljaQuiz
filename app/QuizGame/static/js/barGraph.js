window.renderBarGraph = function() {
  const rawDataElem = document.getElementById("player-data");
  if (!rawDataElem) {
    console.warn("player-data element not found");
    return;
  }

  const standings = JSON.parse(rawDataElem.textContent);
  const graph = document.getElementById('fun-bar-graph');
  if (!graph) {
    console.warn("fun-bar-graph element not found");
    return;
  }

  graph.innerHTML = ''; // clear existing bars

  let maxPoints = 0;
  for (const id in standings) {
    const points = standings[id].quizgame.points;
    if (points > maxPoints) maxPoints = points;
  }

  const maxHeight = 200;

  for (const id in standings) {
    const player = standings[id];
    const points = player.quizgame.points;

    const bar = document.createElement('div');
    bar.className = 'bar';
    const scaledHeight = (points / (maxPoints || 1)) * maxHeight;
    bar.style.height = '0px';

    const value = document.createElement('div');
    value.className = 'bar-value';
    value.innerText = `${points}`;

    const label = document.createElement('div');
    label.className = 'bar-label';
    label.innerText = player.name;

    bar.appendChild(value);
    bar.appendChild(label);
    graph.appendChild(bar);

    setTimeout(() => {
      bar.style.height = `${scaledHeight}px`;
    }, 100);
  }
};