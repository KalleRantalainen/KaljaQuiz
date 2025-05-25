const canvas = document.getElementById('beerCanvas');
const ctx = canvas.getContext('2d');

const rootStyles = getComputedStyle(document.documentElement);

let activeCellColor = rootStyles.getPropertyValue('--color-drop').trim();
let bgColor = rootStyles.getPropertyValue('--color-background').trim();


const cellSize = 10;
const cols = canvas.width / cellSize;
const rows = canvas.height / cellSize;

let grid = [];

// Initialize grid with dead cells
function initGrid() {
  grid = new Array(rows);
  for (let y = 0; y < rows; y++) {
    grid[y] = new Array(cols).fill(0);
  }
}

// Randomize grid with some live cells
function randomizeGrid() {
  for (let y = 0; y < rows; y++) {
    for (let x = 0; x < cols; x++) {
      grid[y][x] = Math.random() > 0.8 ? 1 : 0;
    }
  }
}

// Count live neighbors of a cell
function countNeighbors(x, y) {
  let count = 0;
  for (let i = -1; i <= 1; i++) {
    for (let j = -1; j <= 1; j++) {
      if (i === 0 && j === 0) continue;
      let col = (x + j + cols) % cols;
      let row = (y + i + rows) % rows;
      count += grid[row][col];
    }
  }
  return count;
}

// Update grid for next generation
function updateGrid() {
  const nextGrid = new Array(rows);
  for (let y = 0; y < rows; y++) {
    nextGrid[y] = new Array(cols).fill(0);
    for (let x = 0; x < cols; x++) {
      const neighbors = countNeighbors(x, y);
      if (grid[y][x] === 1) {
        nextGrid[y][x] = neighbors === 2 || neighbors === 3 ? 1 : 0;
      } else {
        nextGrid[y][x] = neighbors === 3 ? 1 : 0;
      }
    }
  }
  grid = nextGrid;
}

// Draw the grid with neon green cells
function drawGrid() {
  ctx.fillStyle = bgColor;
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.fillStyle = activeCellColor;
  for (let y = 0; y < rows; y++) {
    for (let x = 0; x < cols; x++) {
      if (grid[y][x] === 1) {
        ctx.fillRect(x * cellSize, y * cellSize, cellSize - 1, cellSize - 1);
      }
    }
  }
}

// Main loop
let lastUpdateTime = 0;
const updateInterval = 200; // milliseconds

function loop(timestamp) {
  if (!lastUpdateTime) lastUpdateTime = timestamp;
  
  if (timestamp - lastUpdateTime > updateInterval) {
    updateGrid();
    lastUpdateTime = timestamp;
  }
  
  drawGrid();
  requestAnimationFrame(loop);
}

initGrid();
randomizeGrid();
requestAnimationFrame(loop);