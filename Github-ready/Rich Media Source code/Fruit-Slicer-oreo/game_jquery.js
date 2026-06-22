var playing = false;
var score;
var trialsleft;
var step = 3; // Increase initial speed
var action; // for setInterval
var fruits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']; // for fruits
var intervalTime = 50; // Initial interval time
var speedIncreaseInterval = 1; // Increase speed every fruit slice
var maxFruits = 3; // Maximum number of fruits dropping at the same time
var originalBackground = 'url("./Assets/OREO\ Background.jpg")'; // Change to your original background image

$(function() {
    // Show the front screen initially
    $('#front').show();

    // Click on start or reset button
    $("#startReset").click(function() {
        if (playing == true) {
            // If we are playing, reload page
            location.reload();
        } else {
            // If we are not playing from before
            playing = true;

            // Hide the front screen and show the score
            $('#front').hide();
            $('#score').show();

            // Set score to 0
            score = 0;
            $("#scoreValue").html(score);

            // Show trials left box
            $('#trialsleft').show();
            trialsleft = 3;
            addHearts();

            // Hide game over box
            $('#gameOver').hide();

            // Hide startReset button
            $('#startReset').hide();

            // Set the original background
            $('#fruitcontainer').css('background-image', originalBackground);

            // Start action
            startAction();
        }
    });

    // Functions
    function addHearts() {
        $('#trialsleft').empty();
        for (var i = 0; i < trialsleft; i++) {
            $('#trialsleft').append('<img src="Assets/wrong.png" class="life">');
        }
    }

    function startAction() {
        // Generate random fruits
        for (var i = 0; i < maxFruits; i++) {
            generateFruit(i);
        }

        // Move fruits down
        action = setInterval(function() {
            $('.fruit').each(function() {
                var fruit = $(this);
                fruit.css('top', fruit.position().top + step);

                // Check if the fruit is too low
                if (fruit.position().top > $('#fruitcontainer').height() - 50) {
                    if (trialsleft > 1) {
                        // Generate a fruit again
                        resetFruit(fruit);
                        trialsleft--;
                        addHearts();
                    } else {
                        // Game over
                        playing = false;

                        // Change background image of #fruitcontainer
                        $('#fruitcontainer').css('background-image', 'url("Assets/OREO_End Frame Background.jpg")');

                        // Show game over
                        // $('#gameOver').show().html('<p>Your score is ' + score + '</p>');

                        // Hide trials left
                        $('#trialsleft').hide();

                        // Stop fruit moving
                        stopAction();

                        // Show startReset button
                        $('#startReset').html('Start Again').show();

                        // Play confetti effect after 500ms
                        setTimeout(function() {
                            confettiEffect();
                            $('#congrats')[0].play();
                        }, 500);

                        // Redirect to Instagram after 3 seconds
                        setTimeout(function() {
                            window.open("https://www.instagram.com/oreo/?hl=en", "_blank");
                        }, 2500);
                    }
                }
            });
        }, intervalTime);
    }

    // Generate a random fruit
    function generateFruit(index) {
        var fruit = $('<img src="" class="fruit">').attr('id', 'fruit' + index);
        $('#fruitcontainer').append(fruit);
        resetFruit(fruit);
    }

    // Reset a fruit's position and image
    function resetFruit(fruit) {
        var randomFruit = Math.round(9 * Math.random());
        fruit.attr('src', 'Assets/' + fruits[randomFruit] + '.png');
        fruit.css({
            'left': Math.round(550 * Math.random()),
            'top': -50
        }).show();
    }

    // Stop dropping fruits
    function stopAction() {
        clearInterval(action);
        $('.fruit').remove();
    }

    // Slice a fruit
    $(document).on('mouseover', '.fruit', function() {
        var fruit = $(this);
        score++; // Increase score
        $("#scoreValue").html(score);

        // Increase speed as score increases
        if (score % speedIncreaseInterval == 0) {
            step++; // Increase the step to make fruits fall faster
        }

        // Play sound
        var sliceSound = $("#slicesound")[0];
        sliceSound.currentTime = 0; // Reset playback position to the start
        sliceSound.play();

        // Show flash effect
        $('#flash').css({
            'top': fruit.position().top - 20,
            'left': fruit.position().left - 20
        }).show().fadeOut(100);

        // Get the fruit's current position
        var fruitTop = fruit.position().top;
        var fruitLeft = fruit.position().left;

        // Hide whole fruit
        fruit.hide();

        // Create and position the sliced halves
        var half1 = $('<img src="' + fruit.attr('src') + '" class="fruit-half">').css({
            'top': fruitTop,
            'left': fruitLeft,
            'transform': 'rotate(-20deg)',
            'display': 'block'
        });
        var half2 = $('<img src="' + fruit.attr('src') + '" class="fruit-half">').css({
            'top': fruitTop,
            'left': fruitLeft + 30,
            'transform': 'rotate(20deg)',
            'display': 'block'
        });

        // Append the halves to the container
        $('#fruitcontainer').append(half1).append(half2);

        // Animate the sliced halves
        half1.animate({
            top: fruitTop + 100,
            left: fruitLeft - 100,
            opacity: 0
        }, 1000, 'linear', function() {
            $(this).remove(); // Remove the element after animation completes
        });

        half2.animate({
            top: fruitTop + 100,
            left: fruitLeft + 100,
            opacity: 0
        }, 1000, 'linear', function() {
            $(this).remove(); // Remove the element after animation completes
        });

        // Generate a new fruit
        resetFruit(fruit);
    });

    function confettiEffect() {
        var duration = 5 * 1000;
        var animationEnd = Date.now() + duration;
        var defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 0 };

        function randomInRange(min, max) {
            return Math.random() * (max - min) + min;
        }

        var interval = setInterval(function() {
            var timeLeft = animationEnd - Date.now();

            if (timeLeft <= 0) {
                return clearInterval(interval);
            }

            var particleCount = 50 * (timeLeft / duration);
            confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 } }));
            confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 } }));
        }, 250);
    }
});
