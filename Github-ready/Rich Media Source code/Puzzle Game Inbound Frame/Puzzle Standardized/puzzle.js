var currTile, otherTile, timer, rows = 4, columns = 4, turns = 0, redirected = !0, timerDuration = 20;

window.onload = function() {
    let a = [];
    for (let b = 1; b <= rows * columns; b++) a.push(b.toString());
    let b = a.slice(0, 8), c = a.slice(8);
    for (let a, b = 0; b < c.length; b++) a = Math.floor(Math.random() * c.length), [c[b], c[a]] = [c[a], c[b]];
    let d = b.concat(c);
    for (let a = 0; a < rows; a++) {
        for (let b = 0; b < columns; b++) {
            let c = document.createElement("img"), e = a * columns + b;
            c.src = "./assets/" + d[e] + ".jpg";
            c.dataset.index = d[e];
            if (e < 8) {
                c.classList.add("fixed");
            } else {
                c.classList.add("draggable");
                c.setAttribute("draggable", "true");
                c.addEventListener("dragstart", handleInteraction);
                c.addEventListener("dragstart", dragStart);
                c.addEventListener("dragover", dragOver);
                c.addEventListener("dragenter", dragEnter);
                c.addEventListener("dragleave", dragLeave);
                c.addEventListener("drop", dragDrop);
                c.addEventListener("dragend", dragEnd);
            }
            document.getElementById("board").append(c);
        }
    }
    document.getElementById("board").addEventListener("click", handleInteraction);
};

function handleInteraction() {
    document.getElementById("overlay").style.display = "none";
    document.getElementById("timer").classList.add("timer-small");
    startTimer(timerDuration);
    document.getElementById("board").removeEventListener("click", handleInteraction);
    let a = document.querySelectorAll(".draggable");
    a.forEach(a => {
        a.removeEventListener("dragstart", handleInteraction);
    });
}

function startTimer(a) {
    var b = document.getElementById("timer"), c = a;
    timer = setInterval(function() {
        let a = Math.floor(c / 60), d = c % 60;
        b.innerText = `${a}:${10 > d ? "0" : ""}${d}`;
        if (c <= 0) {
            clearInterval(timer);
            checkTimeUp();
        }
        c--;
    }, 1000);
}

function checkTimeUp() {
    if (!isPuzzleSolved()) {
        console.log("Time's up! Redirecting to the complete image...");
        showCompleteImage();
    }
}

function dragStart() {
    if (this.classList.contains("fixed")) return;
    currTile = this;
    console.log("Drag Start:", currTile.src);
}

function dragOver(a) {
    a.preventDefault();
}

function dragEnter(a) {
    a.preventDefault();
}

function dragLeave() {}

function dragDrop() {
    if (this.classList.contains("fixed")) return;
    otherTile = this;
    console.log("Drag Drop:", otherTile.src);
}

function dragEnd() {
    if (currTile.src.includes("blank") || otherTile.classList.contains("fixed")) return;
    let a = currTile.src, b = otherTile.src;
    currTile.src = b, otherTile.src = a;
    let c = currTile.dataset.index;
    currTile.dataset.index = otherTile.dataset.index, otherTile.dataset.index = c;
    turns += 1;
    document.getElementById("turns").innerText = turns;
    console.log("Turns:", turns);
    if (turns >= 5 && !redirected) {
        redirected = !0;
        console.log("Redirecting...");
        window.open("https://www.instagram.com/delamerekenya?igsh=NXFpaTlzdGQ3em54", "_blank");
    }
    if (isPuzzleSolved()) {
        clearInterval(timer);
        showCompleteImage();
    }
}

function isPuzzleSolved() {
    let a = document.querySelectorAll("#board img");
    for (let b = 0; b < a.length; b++) {
        if (a[b].dataset.index != (b + 1).toString()) return !1;
    }
    return !0;
}

function showCompleteImage() {
    let a = document.getElementById("board");
    a.innerHTML = "";
    let b = document.createElement("img");
    b.src = "./assets/complete.png";
    b.style.width = "100%";
    b.style.height = "100%";
    b.classList.add("complete");

    // Add event listener for click
    b.addEventListener("click", function() {
        window.open("https://www.carrefour.ke/mafken/en/plain-laban/ilara-maziwa-lala-bottle-500ml/p/43357?list_name=search%7Cillara_mazilla&offer=offer_carrefour_&utm_source=suss_ads_display_video&utm_medium=display&utm_campaign=dairy_best&utm_id=suss_ads&utm_term=display_video", "_blank");
    });

    a.appendChild(b);
}
