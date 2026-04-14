# Aero Blaster: Horse of Doom
1. INTRODUCTION
     hi teacher! this is our group project for the class. we really like space shooting games like chicken invaders, so we tried to make one together using python. the game is about a pilot trying to survive in space and reach the iss station. we hope you enjoy playing it!
   - technologies we use: 
      + language: python 3.x
      + library: pygame (for game logic and rendering)
      + math and random: for enemy movement and boss patterns
      + os and sys: for managing file paths and system exit
2. SUMMARY (what is this code about?)
  - the code is a complete game. here is what we put inside:
      + player & movement: you can move your ship using w, a, s, d keys
      + combat system: your ship shoots automatically. the more points you get, the stronger your bullets become (from 1 bullet per shot to 3 bullets per shot)
      + enemies: there are enemy planes and flying rocks (asteroids). they move at different speed
      + boss fight: when you reach 400 points, a big boss will appear with a lot of hp and special bullet patterns
      + victory: if you kill the boss, you win and reach the international space station
      + sound & visuals: we added background music, shooting sounds, and explosion effects to make it feel "real"
  3. BODY
  - how to run the game?
      + you need to install python and pygame library
      + make sure you have all the image and sound files in the right folder (we put the paths in the code)
      + just run the main file and press space to start
  * This is the states diagram for our game, it will help you understand more about how the code work
-
-
-
-

  - how we made this code?
  - we used pygame library to made this project. here is our process:
      + first step: we created the "game loop" so the screen can refresh 60 times per second (60 fps)
      + second step: we wrote "classes" for everything. one class for player, one for enemy, and one for the boss. this makes the code easier for us to fix.
      + third step: we used some math (like sin and cos) to make the boss move smoothly and shoot bullets in a circle.
      + final step: we added "collision detection." this is the part where the code checks if a bullet hits an enemy or if the player hits a rock. if the hp goes to 0, we trigger the explosion effect.
      *note: it was a bit hard for us to fix the sound bugs at first, but now it works fine!
  - things we want to add in the future:
      + if we had more time, our group would like to add:
      + more levels: not just one boss, maybe 3 or 5 levels with different backgrounds
      + item drops: like health kits or shield when you kill enemies
      + shop system: use score to buy new ships or better guns
      + high score table: to save the best players' names
  * This is the video of running our video game:
  -
  -
  -
  -


  
3. CONCLUSION
making this game was a great experience for our group. we learned how to work together, solve difficult bugs, and use python in a fun way. it was challenging to make the boss fight and the sounds work perfectly, but we are very happy with the result. thank you teacher for helping us during the semester and we hope you ẹnoy our project!
  - some small notes:
      + the game gets harder every 100 points because the enemy spawns faster
      + we used "try-except" for the images, so if the computer doesn't have the folders, the game still runs with basic shapes


