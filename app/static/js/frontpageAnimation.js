const canvas = document.getElementById('beerCanvas');
const ctx = canvas.getContext('2d');
const rootStyles = getComputedStyle(document.documentElement);
let dropColor = rootStyles.getPropertyValue('--color-drop').trim();
let bgColor = rootStyles.getPropertyValue('--color-background').trim();

let width, height;
function resize() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
}
window.addEventListener('resize', resize);
resize();

const drops = [];

for (let i = 0; i < 70; i++) {
    drops.push({
        x: Math.random() * width,
        y: Math.random() * height,
        size: Math.random() * 20 + 10,
        speed: Math.random() * 0.5 + 0.3,
        wobble: Math.random() * 2 * Math.PI,
        alpha: Math.random() * 0.4 + 0.4
    });
}

function drawDrop(x, y, size, alpha, wobble) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(Math.sin(wobble) * 0.1);
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.bezierCurveTo(size * 0.5, size * 0.2, size * 0.5, size * 0.8, 0, size);
    ctx.bezierCurveTo(-size * 0.5, size * 0.8, -size * 0.5, size * 0.2, 0, 0);
    ctx.closePath();

    ctx.fillStyle = bgColor;
    ctx.fillStyle = dropColor.replace(/[\d\.]+\)$/, `${alpha})`);

    //ctx.fillStyle = `rgba(255, 204, 0, ${alpha})`;
    ctx.fill();
    ctx.restore();
}

function draw() {
    dropColor = rootStyles.getPropertyValue('--color-drop').trim();
    bgColor = rootStyles.getPropertyValue('--color-background').trim();
    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = bgColor;
    ctx.fillRect(0, 0, width, height);

    for (let drop of drops) {
        drawDrop(drop.x, drop.y, drop.size, drop.alpha, drop.wobble);
        drop.y += drop.speed;
        drop.wobble += 0.05;

        if (drop.y > height + 20) {
            drop.y = -20;
            drop.x = Math.random() * width;
            drop.size = Math.random() * 20 + 10;
            drop.alpha = Math.random() * 0.4 + 0.4;
            drop.wobble = Math.random() * 2 * Math.PI;
        }
    }

    requestAnimationFrame(draw);
}

draw();