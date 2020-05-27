# Game Plot Description
The Tower is a 2D, side-scroller game is set in a fictitious post-apocalyptic, dystopian Singapore. The main character, a 21-year-old Singaporean, has to survive the infamous Tower in order to gain acceptance into the prestiguous National University of Singapore. As he climbs the Tower, he has to survive various obstacles and dangers, like falling spikes and zombie attacks. As the game progresses, we can pick up various visual hints on how Singapore had regressed to that state.


# Target Audience
This game is targetted for Singaporean young adult audiences who wish to have a quick thrill or a flight of imagination into a fantasy setting. As we might include story elements that may be disturbing, as well as several jump scares, it is not for the faint of heart (young children / elderly), or the epileptic as there may be flashing lights that could trigger seizures.


# Time Spent
Both collaborators of this project, Joshua Chew and You Ying Feng, has spent an average of 4 hours a day working on this project. We have both spent the first few weeks following online tutorials on YouTube (eg. DaFluffyPotato, TechWithTim) on programming 2D platformer games on Unity and Pygame before embarking on our project. Upon adding a new implementation, we are sure to comment our code so that the other collaborator would be able to understand the additional code and make improvements or bug fixes if needed.


# Problem
While there are many horror / fantasy video games made available online, it is rare to find a quality game that is relatable to the Singaporean narrative. We wish to create a game that strikes a chord with the Singaporean identity, invoking feelings of nostalgia, awe and suspense as they recognise several elements within the game as distinctly Singaporean.


# Development Plan
We intend to fully implement these features before the following Milestones:

## Milestone 1: Main Functionality
- Main game loop, which controls the entire game via a SceneManager
- TitleScene, GameScene and GameOverScene, classes which inherit from an abstract Scene class, all managed by a common SceneManager
- Player class, which allows movement, collisions, player damage and death
- Terrain, which is implemented via the Block and Map class
- Static, Parallax and Scrolling Backgrounds, which inherit from an abstract Background class

## Milestone 2: Gameplay Elements
- Create an Enemy class which is similar to the Player class but with automatic movement
- Implement dangerous terrain which decrements the health of the player (eg. spikes, fireballs)
- Allow player to kill enemies
- Create a PowerUp class give it special abilities. Implement methods which can only be called when the player is powered-up, making use of boolean flags.

## Milestone 3: Asset Design
- Conduct a brainstorming session to finalize our intentions for all the design elements, ensuring that they are able to tell a compelling story.
- Design the look of the player to resemble a 21-year-old Singaporean student
- Design the look of enemies to be original and menacing
- Design terrain textures to resemble walls of a tower
- Make use of photography and photoshop to design background, making it resemble a post-apocalyptic Singapore.
- Bug fixes and improvements to the efficiency of the code


# Good reading material  
http://gameprogrammingpatterns.com/game-loop.html  
http://gameprogrammingpatterns.com/state.html and pretty much the entire book lmao  
https://stackoverflow.com/questions/14354171/add-scrolling-to-a-platformer-in-pygame for camera scrolling
https://stackoverflow.com/questions/14700889/pygame-level-menu-states for state machine
