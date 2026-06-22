document.addEventListener('DOMContentLoaded', () => {
    const scenes = document.getElementById('scenes');
    let isReversed = false;

    function startAnimation() {
      setTimeout(() => {
        // Start trembling
        scenes.classList.add('trembling');
        
        setTimeout(() => {
          if (isReversed) {
            scenes.classList.remove('reverse');
            scenes.classList.add('active');
          } else {
            scenes.classList.remove('active');
            scenes.classList.add('reverse');
          }

          isReversed = !isReversed;

          // Stop trembling once the transition ends
          setTimeout(() => {
            scenes.classList.remove('trembling');
          }, 2000); // Same duration as the transition (2s)
          
          startAnimation(); // Repeat the animation
        }, 2000); // Wait for the transition duration (2s)
      }, 5000); // 7 seconds between transitions
    }

    // Initial delay before starting the animation
    setTimeout(() => {
      scenes.classList.add('active');
      startAnimation();
    }, 7000);  // Wait 7 seconds before the first animation
});
