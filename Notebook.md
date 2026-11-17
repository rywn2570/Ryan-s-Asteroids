## Asteroids Project Notebook

# IPO Table 
| Function | Input | Process | Output |
| :--- | :--- | :--- | :--- |
| *main() (main.py)* | System clock (dt), user inputs, audio assets | Initializes Pygame, mixer, display window, sprite groups, and runs the 60 FPS game loop | Runs the game state until the player quits or loses all lives |
| *handle_events() (main.py)* | pygame event queue | Iterates through system events to check for a window close | Returns bool (False to exit loop, True to continue) |
| *update_game() (main.py)* | dt, updatable, asteroids, shots, player, score, lives, hit_sound | Updates all sprite positions/timers and checks for collisions | Returns updated (score, lives) tuple |
| *render_game() (main.py)* | screen, drawable, font, score, lives | Clears screen to black, draws all sprites, renders HUD (score/lives), and displays Game Over screen if lives <= 0 | Updates the visible game frame with pygame.display.flip() |
| *Player.update() (player.py)* | dt, keyboard state (W, A, D, SPACE, END) | Moves/rotates ship, manages burst-fire weapon cooldowns, retains ship position within screen borders | Updates player.position, rotation, and spawns Shot objects |
| *handle_collisions() (collisions.py)* | asteroids, shots, player, score, lives, and hit_sound | Runs player-asteroid and shot-asteroid collision checks. | Returns the updated (score, lives) values. |
| *handle_player_collisions() (collisions.py)* | asteroids, player, lives, hit_sound | Checks if any asteroid overlaps with the player; plays hit sound, deducts 1 life, and resets player to screen center | Returns updated lives (int) and destroys colliding asteroid |
| *handle_shot_collisions() (collisions.py)* | asteroids, shots, score, hit_sound | Checks if any shot hits an asteroid; awards size-based points (50/100/200) and triggers asteroid splitting | Returns updated score (int) and removes shot/asteroid |
| *Asteroid.split() (asteroid.py)* | Current asteroid position, velocity, radius | Destroys current asteroid; if larger than minimum radius, spawns two smaller, faster asteroids diverging at random angles | Spawns 2 new Asteroid sprites (or None if minimum size) |
| *AsteroidField.update() (asteroidfield.py)* | Delta time (dt) and screen dimensions | Tracks the spawn timer against the spawn rate in constants.py and generates new asteroids at random screen edges. | Spawns a new Asteroid sprite into the game groups. |
| *log_state() (logger.py)* | Caller local variables (sprites, groups, screen surface) | Uses inspect to read frame variables, samples active sprite coordinates/velocities up to 16 seconds, and formats data into a JSON dictionary. | Appends a timestamped game state snapshot entry to game_state.jsonl. |

# Class Hierarchy Diagram
```text
                  ┌──────────────────────────────────┐
                  │      pygame.sprite.Sprite        │
                  └────────────────┬─────────────────┘
                                   │ (inherits)
                 ┌─────────────────┴─────────────────┐
                 ▼                                   ▼
┌─────────────────────────────────┐  ┌─────────────────────────────────┐
│           CircleShape           │  │          AsteroidField          │
│─────────────────────────────────│  │─────────────────────────────────│
│ + position: pygame.Vector2      │  │ + edges: list[Edge]             │
│ + radius: float                 │  │ + spawn_timer: float            │
│─────────────────────────────────│  │─────────────────────────────────│
│ + draw(screen)                  │  │ + spawn(radius, pos, vel)       │
│ + update(dt)                    │  │ + update(dt)                    │
│ + collides_with(other) -> bool  │  └─────────────────────────────────┘
└────────────────┬────────────────┘
                 │ (inherits)
       ┌─────────┴─────────┬─────────────────────────┐
       ▼                   ▼                         ▼
┌──────────────┐  ┌─────────────────┐  ┌─────────────────────────────┐
│    Player    │  │    Asteroid     │  │            Shot             │
│──────────────│  │─────────────────│  │─────────────────────────────│
│ + rotation   │  │ + velocity      │  │ + velocity                  │
│ + shoot_timer│  │─────────────────│  │─────────────────────────────│
│ + shoot_sound│  │ + draw(screen)  │  │ + draw(screen)              │
│──────────────│  │ + update(dt)    │  │ + update(dt)                │
│ + rotate(dt) │  │ + split()       │  └─────────────────────────────┘
│ + move(dt)   │  │ + score_for_    │
│ + shoot()    │  │   radius()      │
│ + triangle() │  └─────────────────┘
└──────────────┘
```

# Collision Detection Strategy
All physical game entities inherit from CircleShape and use circle-based collision detection. Two entities collide when the distance between their centers is less than the sum of their radii. This method is efficient and avoids complex polygon-intersection checks, but it is an approximation: the player's circular hitbox may not match the outline of the triangular ship exactly.

Collision detection from CircleShape:     
```python
    def collides_with(self, other) -> bool:
        distance = self.position.distance_to(other.position)
        return distance <= (self.radius + other.radius)
```

# Game State Flow Diagram
```text
[ START PROGRAM (main.py) ]
        		│
        		▼
/ Initialize Pygame, Mixer, Display, & Sprite Groups /
        		│
        		▼
◆──►    [ Game Loop] ◄──────────────────────────┐
│       │                                        │
│       ├──► [ handle_events() ] ──(QUIT / END)──► [ END PROGRAM ]
│       │
│       ▼
│   [ update_game(dt) ]
│       ├──► Player.update(): Reads W/A/D/SPACE, clamps boundaries, spawns Shots
│       ├──► AsteroidField.update(): Spawns new Asteroids at screen edges
│       └──► handle_collisions():
│               ├──► Shot hits Asteroid ──► score += 50/100/200 & Asteroid.split()
│               └──► Asteroid hits Player ──► lives -= 1 & reset Player position
│       		│
│       		▼
│   / Check Extra Life (score >= next_extra_life_score -> lives += 1) /
│       		│
│       		▼
│   [ render_game() ] ──► Draw Sprites & HUD (Score / Lives)
│       		│					            │
│       		▼					            │
│   		◆── Is lives <= 0? ──(No)──────────┘
│       		│ (Yes)
│       		▼
│   / Render "GAME OVER" & Final Score, wait 3s /
│       		│
│       		▼
└──► [ END PROGRAM ]
```

# Test Cases
(See 'pytests' folder for all of the test cases. Just ensure pytest is installed beforehand and run "python -m pytest")

# Reflection
Design Justifications:
Rather than keeping all game logic inside main.py, I separated the codebase into focused modules (player.py, asteroid.py, shot.py, collisions.py, constants.py, and circleshape.py). Isolating collision logic into collisions.py and centralizing configuration values in constants.py improved readability. 
To keep gameplay challenging yet fair, I implemented a boundary so the player cannot fly off-screen, removed reverse thrust to encourage strategic manuvering, and added a burst-fire cooldown system (PLAYER_SHOOT_BURST_SECONDS) so players can use a short "laser beam" when required but cannot hold down the spacebar indefinitely. 
Visual and audio feedback—such as the orange thruster flame, HUD color changes at 10,000 points or when lives exceed four, and sound effects for shooting and collisions allowed the game to be more enjoyable and entertaining for the user, as the original bootdev lessons only provided black and white without any audio.

Challenges and Solutions:
Early on in the project I faced major difficulty following along with the bootdev Object Orientated Programming lessons as our teacher was unavailable and I felt the lessons didn't properly teach me how to use the different components well. Hence when I progressed into the assessment - building the actual Asteroids game, I was really struggling. One of the key solutions to this was to utilize bootdev's built-in educational AI, Boots. I could ask it to expand on the usage of a particular element not explained in the actual lesson section. As I completed the bootdev course on Asteroids, I began to explore different ways to make the game engaging to the user. The next challenge was one of the biggest - using ssh to access the compsci.pared account. Being unable to login to my account at home meant I was unable to efficiently save and sync my work accross different devices. Luckily, one of my classmates discovered a way to utilize the token system of github to allow us to push code to a github repository as an alternative to ssh, without signing in. 
Unlike BookBot—where functions processed standard strings and dictionaries — Pygame required things like display surfaces, audio mixers, and system event queues. This meant that writing unit tests would differ; I was unsure of how I would test units without running the game. My solution to this was to research. I came across Python's unittest.mock module that allowed me to simulate SFX, event queues and drawings so my tests could run instantly and reliably. You can view this in many of my tests under the folder "pytests".  