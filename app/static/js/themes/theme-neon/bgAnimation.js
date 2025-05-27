(function () {
    // Voin tulla sen verran vastaan että tässäkin animaatiossa on hiomista jos meinaa
    // saada sellatteen jota viittii kattella.

    // x coord: ruudun sisään
    // y coord: ylös/alas
    // z coord: vasen/oikea

    const canvas = document.getElementById('beerCanvas');
    if (!canvas) return;

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const rootStyles = getComputedStyle(document.documentElement);
    let activeCellColor = rootStyles.getPropertyValue('--color-drop').trim();
    let bgColor = rootStyles.getPropertyValue('--color-background').trim();
    let ceilingColor = rootStyles.getPropertyValue('--color-background-button').trim();
    let highlightColor = rootStyles.getPropertyValue('--color-drop').trim();

    const floorMaterial = new THREE.MeshBasicMaterial({
        color: new THREE.Color(bgColor), 
        side: THREE.DoubleSide
    });

    const ceilingMaterial = new THREE.MeshBasicMaterial({
        color: new THREE.Color(ceilingColor), 
        side: THREE.DoubleSide
    });

    const scene = new THREE.Scene();

    // const loader = new THREE.TextureLoader();
    // loader.load('/static/data/environment.jpg', function(texture) {
    //     texture.mapping = THREE.EquirectangularReflectionMapping;
    //     scene.background = texture;
    //     scene.environment = texture;
    // });

    function getRandomFloat(min, max) {
        return Math.random() * (max - min) + min;
    }


    function getRandomInt(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    function getCubePos(initial = false) {
        // Generoidaan aloituskoko ja paikka cubeille
        let xPos;
        if (initial) {
            xPos = getRandomInt(-50, -5);
        } else {
            xPos = getRandomInt(-50, -30);
        }
        let zPos = getRandomInt(-9, 9);
        let yRot = getRandomFloat(0, Math.PI); // Rotaatio on radiaaneissa
        let speed = getRandomFloat(0.01, 0.03);
        return [xPos, zPos, yRot, speed];
    }

    // Init random cubes
    const numOfCubes = 10;
    const cubes = []
    for (let i = 0; i < numOfCubes; i++) {
        let cubeSize = getRandomInt(1, 3);
        
        // Lisätään cubet listaan
        const boxGeometry = new THREE.BoxGeometry(cubeSize);
        const edges = new THREE.EdgesGeometry(boxGeometry);
        const lineMaterial = new THREE.LineBasicMaterial({ color: highlightColor });
        const wireframeCube = new THREE.LineSegments(edges, lineMaterial);

        const [xPos, zPos, yRot, speed] = getCubePos(true); // Initial pos attrubutes

        wireframeCube.position.set(xPos, 0, zPos);
        wireframeCube.rotation.y = yRot;
        wireframeCube.speed = speed; // Mun oma property, ei tee defaulttina mitään, ei ois varmaan tätäkään pitänyt tehdä kun näyttää perseeltä

        cubes.push(wireframeCube);

        // Lisätään cubet sceneen oikealle paikalle tasolle
        scene.add(wireframeCube);
    }

    // const boxGeometry = new THREE.BoxGeometry(1, 1, 1);
    // const edges = new THREE.EdgesGeometry(boxGeometry);
    // const lineMaterial = new THREE.LineBasicMaterial({ color: 0xffffff }); // white lines
    // const wireframeCube = new THREE.LineSegments(edges, lineMaterial);
    // scene.add(wireframeCube);

    // Parametrit: fov, aspect ratio, lyhin etäisyys kamerasta, pisin etäisyys kamerasta
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({canvas: canvas});
    renderer.setSize(window.innerWidth, window.innerHeight);

    // const geometry = new THREE.BoxGeometry();
    // const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
    // const cube = new THREE.Mesh(geometry, material);
    // scene.add(cube);

    const wallGeometry = new THREE.BoxGeometry(50, 2, 2); //x ,y, z
    const wallMaterial = new THREE.MeshBasicMaterial({ color: 0x00ffff });

    const leftWall = new THREE.Mesh(wallGeometry, wallMaterial);
    leftWall.position.set(0, 1, 10);
    scene.add(leftWall);

    const rightWall = new THREE.Mesh(wallGeometry, wallMaterial);
    rightWall.position.set(0, 1, -10);
    scene.add(rightWall);

    // Grid helper (visual grid lines)
    //const gridHelper = new THREE.GridHelper(10, 10);
    //scene.add(gridHelper);
    const gridSize = 50;      // total size of the grid (units)
    const gridDivisions = 50; // number of divisions
    const gridColor = 0x00ffff;
    const centerLineColor = 0x00ffff;

    const gridBottom = new THREE.GridHelper(gridSize, gridDivisions, centerLineColor, gridColor);
    const gridTop = new THREE.GridHelper(gridSize, gridDivisions, centerLineColor, gridColor);

    gridBottom.position.set(0, 0, 0);
    gridTop.position.set(0, 2, 0);

    scene.add(gridBottom);
    scene.add(gridTop);

    /*const planeGeometry = new THREE.PlaneGeometry(50, 50);
    //const planeMaterial = new THREE.MeshBasicMaterial({ color: bgColor, side: THREE.DoubleSide });
    const planeBottom = new THREE.Mesh(planeGeometry, floorMaterial);
    planeBottom.position.set(0, -0.01, 0);
    planeBottom.rotation.x = -Math.PI / 2;
    scene.add(planeBottom);

    const planeTop = new THREE.Mesh(planeGeometry, ceilingMaterial);
    planeTop.position.set(0, 2.01, 0);
    planeTop.rotation.x = -Math.PI / 2;
    scene.add(planeTop);*/

    camera.position.set(3, 1, 0);
    camera.lookAt(scene.position);
    console.log("Plane 1 pos:", gridBottom.position);

    function animate() {
        requestAnimationFrame(animate);
        // cube.rotation.x += 0.01;
        // cube.rotation.y += 0.01;

        gridBottom.position.x += 0.01;
        //gridBottom.rotation.x += 0.005;

        gridTop.position.x += 0.01;
        //gridTop.rotation.x += 0.005;

        if (gridBottom.position.x >= 2) {
          gridBottom.position.x = 0;
        }

        if (gridTop.position.x >= 2) {
          gridTop.position.x = 0;
        }

        // Move cubes:
        for (let i = 0; i < cubes.length; i++) {
            const cube = cubes[i];
            cube.position.x += cube.speed;

            if (cube.position.x > 5) {
                const [xPos, zPos, yRot, speed] = getCubePos();
                cube.position.x = xPos;
                cube.position.z = zPos;
                cube.rotation.y = yRot;
                cube.speed = speed;
            }
        }

        renderer.render(scene, camera);
    }
    animate();
})();


// Vanha bubble animaatio säilössä täällä jos three.js alkaa harmittaan liikaa

/*(function () {
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
})();*/