const createScratchCard = (canvasId, color) => {
  let canvas = document.getElementById(canvasId);
  let context = canvas.getContext("2d");

  const init = () => {
    context.fillStyle = color;
    context.fillRect(0, 0, 300, 100);
  };

  let isDragging = false;

  const scratch = (x, y) => {
    context.globalCompositeOperation = "destination-out";
    context.beginPath();
    context.arc(x, y, 24, 0, 2 * Math.PI);
    context.fill();
  };

  canvas.addEventListener("mousedown", (event) => {
    isDragging = true;
    scratch(event.offsetX, event.offsetY);
  });

  canvas.addEventListener("mousemove", (event) => {
    if (isDragging) {
      scratch(event.offsetX, event.offsetY);
    }
  });

  canvas.addEventListener("mouseup", () => {
    isDragging = false;
  });

  canvas.addEventListener("mouseleave", () => {
    isDragging = false;
  });

  init();
};

createScratchCard("scratch-card1", "#006d77");
