const coin = document.getElementById("coin");
const resultText = document.getElementById("result");

coin.addEventListener("click", async () => {
  const selected = document.querySelector('input[name="side"]:checked').value;

  coin.classList.add("flip");
  resultText.textContent = "";
  setTimeout(() => coin.classList.remove("flip"), 1000);

  const res = await fetch("/api/flip?choice=" + selected);
  const data = await res.json();
  setTimeout(() => {
    resultText.textContent = `Result: ${data.result} — You ${data.win ? "won!" : "lost."}`;
  }, 1000);
});