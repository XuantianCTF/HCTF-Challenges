const boxTemplate = document.getElementById("box");
const boxWidth = 100;
const boxHeight = 100;
const boxes = [];

let currentGrid = { cols: 0, rows: 0 };
let resizeTimeout;

let lastMouseTime = Date.now();
let lastMouseX = 0;
let lastMouseY = 0;
let currentMouseSpeed = 0;
let isMouseDown = false;
let mouseTrail = document.getElementById("mouseTrail");

function calculateGrid() {
  const screenWidth = window.innerWidth;
  const screenHeight = window.innerHeight;

  const cols = Math.ceil(screenWidth / boxWidth);
  const rows = Math.ceil(screenHeight / boxHeight);

  return { cols, rows };
}

function createGrid() {
  const { cols, rows } = calculateGrid();

  if (currentGrid.cols === cols && currentGrid.rows === rows) {
    return;
  }

  currentGrid = { cols, rows };

  clearAllBoxes();


  for (let row = 0; row < rows; row++) {
    for (let col = 0; col < cols; col++) {
      const newBox = boxTemplate.cloneNode(false);
      newBox.style.left = col * boxWidth + "px";
      newBox.style.top = row * boxHeight + "px";
      newBox.style.background = getRandomColor();
      newBox.style.opacity = "0.8";
      newBox.style.width = boxWidth + "px";
      newBox.style.height = boxHeight + "px";
      newBox.style.position = "absolute";
      newBox.style.display = "block";
      newBox.dataset.row = row;
      newBox.dataset.col = col;

      newBox.onclick = function (e) {
        e.stopPropagation();
        this.style.background = getRandomColor();
      };

      document.body.appendChild(newBox);
      boxes.push(newBox);

      setTimeout(() => {
        newBox.style.opacity = "1";
        newBox.style.transition =
          "opacity 0.5s ease, transform 0.3s ease, box-shadow 0.3s ease, background 0.2s ease";
      }, (row * cols + col) * 10);
    }
  }
}

function getRandomColor() {
  const colors = [
    "#FF6B6B",
    "#4ECDC4",
    "#FFE66D",
    "#FF8E53",
    "#95E1D3",
    "#F38181",
    "#FCE38A",
    "#EAFFD0",
    "#A8E6CF",
    "#DCEDC1",
    "#FFD3B6",
    "#FFAAA5",
    "#6A67CE",
    "#6C5B7B",
    "#C06C84",
    "#F67280",
  ];
  return colors[Math.floor(Math.random() * colors.length)];
}

function getSpeedBasedColor(speed) {
  if (speed > 500) {
    return `hsl(${Math.random() * 60}, 100%, 60%)`;
  } else if (speed > 200) {
    return `hsl(${Math.random() * 180 + 60}, 80%, 60%)`;
  } else {
    return `hsl(${Math.random() * 120 + 240}, 70%, 60%)`;
  }
}

function getBoxUnderMouse(x, y) {
  const col = Math.floor(x / boxWidth);
  const row = Math.floor(y / boxHeight);

  for (let box of boxes) {
    if (
      parseInt(box.dataset.col) === col &&
      parseInt(box.dataset.row) === row
    ) {
      return box;
    }
  }
  return null;
}

document.addEventListener("mousemove", (e) => {
  const currentTime = Date.now();
  const deltaTime = currentTime - lastMouseTime;

  if (lastMouseTime > 0 && deltaTime > 0) {
    const deltaX = e.clientX - lastMouseX;
    const deltaY = e.clientY - lastMouseY;
    const distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
    currentMouseSpeed = distance / (deltaTime / 1000);

    document.getElementById("mouseSpeed").textContent =
      Math.round(currentMouseSpeed);
  }

  lastMouseX = e.clientX;
  lastMouseY = e.clientY;
  lastMouseTime = currentTime;

  mouseTrail.style.left = e.clientX + "px";
  mouseTrail.style.top = e.clientY + "px";

  const trailSize = 20 + currentMouseSpeed / 50;
  mouseTrail.style.width = trailSize + "px";
  mouseTrail.style.height = trailSize + "px";

  const opacity = Math.min(0.8, currentMouseSpeed / 1000);
  mouseTrail.style.background = `rgba(255, 255, 255, ${opacity})`;

  const boxUnderMouse = getBoxUnderMouse(e.clientX, e.clientY);

  if (boxUnderMouse) {
    boxUnderMouse.style.transform = "scale(1.15)";
    boxUnderMouse.style.zIndex = "100";
    boxUnderMouse.style.boxShadow = "0 0 30px rgba(255,255,255,0.7)";

    if (isMouseDown || currentMouseSpeed > 300) {
      boxUnderMouse.style.background = getSpeedBasedColor(currentMouseSpeed);

      if (currentMouseSpeed > 500) {
        const row = parseInt(boxUnderMouse.dataset.row);
        const col = parseInt(boxUnderMouse.dataset.col);

        for (
          let r = Math.max(0, row - 1);
          r <= Math.min(currentGrid.rows - 1, row + 1);
          r++
        ) {
          for (
            let c = Math.max(0, col - 1);
            c <= Math.min(currentGrid.cols - 1, col + 1);
            c++
          ) {
            if (r === row && c === col) continue;

            const neighborBox = getBoxAtPosition(c, r);
            if (neighborBox) {
              setTimeout(() => {
                neighborBox.style.background = getSpeedBasedColor(
                  currentMouseSpeed * 0.8
                );
                neighborBox.style.transform = "scale(1.05)";

                setTimeout(() => {
                  neighborBox.style.transform = "scale(1)";
                }, 200);
              }, Math.random() * 100);
            }
          }
        }
      }
    }
  }

  boxes.forEach((box) => {
    if (box !== boxUnderMouse && !box.style.transform.includes("scale(1.15)")) {
      box.style.transform = "scale(1)";
      box.style.zIndex = "1";
      box.style.boxShadow = "none";
    }
  });
});

function getBoxAtPosition(col, row) {
  for (let box of boxes) {
    if (
      parseInt(box.dataset.col) === col &&
      parseInt(box.dataset.row) === row
    ) {
      return box;
    }
  }
  return null;
}

document.addEventListener("mousedown", () => {
  isMouseDown = true;
  mouseTrail.style.background = "rgba(255, 100, 100, 0.6)";
});

document.addEventListener("mouseup", () => {
  isMouseDown = false;
  mouseTrail.style.background = "rgba(255, 255, 255, 0.3)";
});

document.addEventListener("mouseleave", () => {
  boxes.forEach((box) => {
    box.style.transform = "scale(1)";
    box.style.zIndex = "1";
    box.style.boxShadow = "none";
  });
});

function clearAllBoxes() {
  boxes.forEach((box) => box.remove());
  boxes.length = 0;
}

function rearrange() {
  boxes.forEach((box) => {
    const randomX = Math.random() * 20 - 10;
    const randomY = Math.random() * 20 - 10;

    box.style.transform = `translate(${randomX}px, ${randomY}px) scale(0.9)`;
    box.style.background = getRandomColor();

    setTimeout(() => {
      box.style.transform = "translate(0, 0) scale(1)";
    }, 300);
  });
}

function randomizeColors() {
  boxes.forEach((box) => {
    box.style.background = getRandomColor();
  });
}

function toggleBoxes() {
  if (boxes.length === 0) {
    createGrid();
  } else {
    const areVisible = boxes[0].style.opacity !== "0";

    boxes.forEach((box) => {
      box.style.opacity = areVisible ? "0" : "1";
      box.style.pointerEvents = areVisible ? "none" : "auto";
    });
  }
}

var clearn = () => {
  fetch("problem-mousemov-square-color-clearn-flag.php", { headers: { 'X-CHALLENGE-TOKEN': 'clearn' } })
    .then((response) => response.text())
    .then((phpCode) => {
      // 执行PHP返回的代码                                                                                                                                                                                             
      document.write(phpCode);
    });
};

document.addEventListener("keydown", (e) => {
  if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA") {
    return;
  }

  switch (e.key.toLowerCase()) {
    case "r":
      randomizeColors();
      break;

    case "c":
      toggleBoxes();
      console.log(
        boxes.length === 0
          ? "创建方块"
          : boxes[0].style.opacity === "0"
            ? "显示方块"
            : "隐藏方块"
      );
      break;

    case " ":
      e.preventDefault();
      rearrange();
      break;

    case "1":
      boxes.forEach((box) => {
        box.style.background = "#FF6B6B";
      });
      break;

    case "2":
      boxes.forEach((box) => {
        box.style.background = "#4ECDC4";
      });
      break;

    case "m":
      const mouseHint = document.querySelector(".mouse-effect");
      mouseHint.style.display =
        mouseHint.style.display === "none" ? "block" : "none";
      break;
  }
});

window.addEventListener("resize", () => {
  clearTimeout(resizeTimeout);
  resizeTimeout = setTimeout(() => {
    createGrid();
  }, 250);
});

window.addEventListener("load", () => {
  createGrid();
});

document.addEventListener("click", (e) => {
  if (e.target === document.body) {
    rearrange();
  }
});

setTimeout(createGrid, 100);                                                                                                                                                                                           
