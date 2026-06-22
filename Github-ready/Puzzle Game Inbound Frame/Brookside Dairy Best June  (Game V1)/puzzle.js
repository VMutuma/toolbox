var rows = 4;
var columns = 4;

var currTile;
var otherTile;

var turns = 0;
var redirected = false;

window.onload = function() {
    // Pieces array with correct order
    let pieces = [];
    for (let i = 1; i <= rows * columns; i++) {
        pieces.push(i.toString());
    }

    // Shuffle the pieces array, but keep the first 8 in their correct positions
    let fixedPieces = pieces.slice(0, 8);
    let randomPieces = pieces.slice(8);

    for (let i = 0; i < randomPieces.length; i++) {
        let j = Math.floor(Math.random() * randomPieces.length);
        let tmp = randomPieces[i];
        randomPieces[i] = randomPieces[j];
        randomPieces[j] = tmp;
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
                // Make the first 8 pieces fixed
                tile.classList.add("fixed");
            } else {
                // Add drag functionality to the remaining pieces
                tile.classList.add("draggable");
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
    document.getElementById("board").addEventListener("click", hideOverlay);
}

// Function to hide the overlay
function hideOverlay() {
    document.getElementById("overlay").style.display = "none";
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
        redirected = true; // Set the flag to true to prevent further redirections
        console.log("Redirecting...");
        window.open("https://www.instagram.com/delamerekenya?igsh=NXFpaTlzdGQ3em54", "_blank");
    }

    // Check if the puzzle is solved
    if (isPuzzleSolved()) {
        transformBoardToCompleteImage();
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

// Transform the board to display the complete image with a smooth transition
function transformBoardToCompleteImage() {
    let board = document.getElementById("board");
    board.classList.add('complete');

    setTimeout(() => {
        board.innerHTML = ''; // Clear the board

        let completeImage = document.createElement("img");
        completeImage.src = "./assets/complete.png";
        completeImage.style.width = "100%";
        completeImage.style.height = "100%";

        board.appendChild(completeImage);
        board.classList.add('show-complete');
    }, 1000);
}
