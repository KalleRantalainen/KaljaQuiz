const canvas = document.getElementById('beerCanvas');
const ctx = canvas.getContext('2d');
const rootStyles = getComputedStyle(document.documentElement);

let bubbleColor = rootStyles.getPropertyValue('--color-text-highlight').trim();
let bgColor = rootStyles.getPropertyValue('--color-background-2').trim();

let width, height;
function resize() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
}

window.addEventListener('resize', resize);
resize();

const bubbles = [];
const bubbleColCount = 20;
const bubblesPerCol = 30;

const colCoords = [];

for (let i = 0; i < bubbleColCount; i++) {
  const num = Math.random() * width;
  colCoords.push(num);
  console.log("ColNum:", i);
  console.log("xCoord:", num);
  console.log("----");
}

for (const xCoord of colCoords) {
    for (let i = 0; i < bubblesPerCol; i++) {
        bubbles.push({
            initialX: xCoord,
            x: ((Math.random() * 5) - 10) + xCoord,
            y: Math.random() * height,
            size: Math.random() * 5 + 2.5,
            speed: Math.random() * 0.5 + 0.3,
            wobbleAmplitude: Math.random() * 5 + 2.5,
            wobbleFrequency: Math.random() * 0.02 + 0.005,
        });
    }
}

function drawBubble(x, y, size) {
    ctx.save();
    ctx.translate(x, y);

    ctx.strokeStyle = bubbleColor;   // Outline color
    ctx.lineWidth = 1;           // Outline thickness

    ctx.beginPath();
    ctx.arc(x, y, size, 0, Math.PI * 2);  // x, y, radius, startAngle, endAngle
    ctx.stroke();  // Actually draws the outline

    //ctx.fillStyle = `rgba(255, 204, 0, ${alpha})`;
    ctx.restore();
}

function draw() {
    //dropColor = rootStyles.getPropertyValue('--color-drop').trim();
    //bgColor = rootStyles.getPropertyValue('--color-background').trim();
    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = bgColor;
    ctx.fillRect(0, 0, width, height);

    for (let bubble of bubbles) {
        drawBubble(bubble.x, bubble.y, bubble.size);

        bubble.y -= bubble.speed;
        // Lasketaan x koordinaatti siniaallon perusteella niin tulee oikkeen smooth
        bubble.x = bubble.initialX + Math.sin(bubble.y * bubble.wobbleFrequency) * bubble.wobbleAmplitude;

        if (bubble.y < -20) {
            bubble.x = bubble.initialX;
            bubble.y = height + 20;
            bubble.size = Math.random() * 5 + 2.5;
        }
    }

    requestAnimationFrame(draw);
}

draw();