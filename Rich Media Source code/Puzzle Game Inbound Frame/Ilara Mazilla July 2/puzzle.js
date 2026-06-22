var rows = 4;
var columns = 4;

var currTile;
var otherTile;

var turns = 0;
var redirected = !false;
var timerDuration = 20;
var timer;

// Initialize the game
window.onload = function() {
    let pieces = [];
    for (let i = 1; i <= rows * columns; i++) {
        pieces.push(i.toString());
    }

    // Shuffle the pieces array, but keep the first 8 in their correct positions
    let fixedPieces = pieces.slice(0, 8);
    let randomPieces = pieces.slice(8);

    for (let i = 0; i < randomPieces.length; i++) {
        let j = Math.floor(Math.random() * randomPieces.length);
        [randomPieces[i], randomPieces[j]] = [randomPieces[j], randomPieces[i]];
    }

    let allPieces = fixedPieces.concat(randomPieces);

    // Initialize the 4x4 board with pieces
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < columns; c++) {
            let tile = document.createElement("img");
            let pieceIndex = r * columns + c;

            tile.src = "./assets/" + allPieces[pieceIndex] + ".jpg";
            tile.dataset.index = allPieces[pieceIndex];
            if (pieceIndex < 8) {
                tile.classList.add("fixed");
            } else {
                tile.classList.add("draggable");
                tile.setAttribute("draggable", "true"); // Ensure the tile is draggable
                tile.addEventListener("dragstart", handleInteraction);
                tile.addEventListener("dragstart", dragStart);
                tile.addEventListener("dragover", dragOver);
                tile.addEventListener("dragenter", dragEnter);
                tile.addEventListener("dragleave", dragLeave);
                tile.addEventListener("drop", dragDrop);
                tile.addEventListener("dragend", dragEnd);
            }

            document.getElementById("board").append(tile);
        }
    }

    // Add event listener to hide the overlay when the user starts interacting with the puzzle
    document.getElementById("board").addEventListener("click", handleInteraction);
}

// Function to handle the initial interaction with the game
function handleInteraction() {
    document.getElementById("overlay").style.display = "none";
    document.getElementById("timer").classList.add("timer-small");
    startTimer(timerDuration);

    // Remove the event listeners to prevent them from being triggered again
    document.getElementById("board").removeEventListener("click", handleInteraction);
    let draggableTiles = document.querySelectorAll(".draggable");
    draggableTiles.forEach(tile => {
        tile.removeEventListener("dragstart", handleInteraction);
    });
}

// Function to start the timer
function startTimer(duration) {
    var timerDisplay = document.getElementById("timer");
    var time = duration;

    timer = setInterval(function() {
        let minutes = Math.floor(time / 60);
        let seconds = time % 60;
        timerDisplay.innerText = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;

        if (time <= 0) {
            clearInterval(timer);
            checkTimeUp();
        }

        time--;
    }, 1000);
}

// Function to check if time is up
function checkTimeUp() {
    if (!isPuzzleSolved()) {
        console.log("Time's up! Redirecting to the complete image...");
        showCompleteImage();
    }
}

// DRAG TILES
function dragStart() {
    if (this.classList.contains("fixed")) {
        return;
    }
    currTile = this;
    console.log("Drag Start:", currTile.src);
}

function dragOver(e) {
    e.preventDefault();
}

function dragEnter(e) {
    e.preventDefault();
}

function dragLeave() {}

function dragDrop() {
    if (this.classList.contains("fixed")) {
        return;
    }
    otherTile = this;
    console.log("Drag Drop:", otherTile.src);
}

function dragEnd() {
    if (currTile.src.includes("blank") || otherTile.classList.contains("fixed")) {
        return;
    }
    let currImg = currTile.src;
    let otherImg = otherTile.src;
    currTile.src = otherImg;
    otherTile.src = currImg;

    // Swap the data-index attributes
    let currIndex = currTile.dataset.index;
    currTile.dataset.index = otherTile.dataset.index;
    otherTile.dataset.index = currIndex;

    turns += 1;
    document.getElementById("turns").innerText = turns;
    console.log("Turns:", turns);

    if (turns >= 5 && !redirected) {
        redirected = true;
        console.log("Redirecting...");
        window.open("https://www.instagram.com/delamerekenya?igsh=NXFpaTlzdGQ3em54", "_blank");
    }

    // Check if the puzzle is solved
    if (isPuzzleSolved()) {
        clearInterval(timer);
        showCompleteImage();
    }
}

// Check if the puzzle is solved
function isPuzzleSolved() {
    let tiles = document.querySelectorAll("#board img");
    for (let i = 0; i < tiles.length; i++) {
        if (tiles[i].dataset.index != (i + 1).toString()) {
            return false;
        }
    }
    return true;
}

// Function to show the complete image
function showCompleteImage() {
    let board = document.getElementById("board");
    board.innerHTML = '';

    let completeImage = document.createElement("img");
    completeImage.src = "./assets/complete.png";
    completeImage.style.width = "100%";
    completeImage.style.height = "100%";
    completeImage.classList.add("complete"); // Add the animation class

    board.appendChild(completeImage);
}
