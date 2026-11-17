# Ryan-s-Asteroids


Extreme Asteroids Arcade Game
Author: Ryan Lin
Date: November 2026
Course: Building Asteroids using Python and Pygame - Bootdev

# Description:
    Asteroids is a 1979 multidirectional shooter video game originally developed and published by Atari, Inc. 
    for arcades. This fast-paced version of the game features a single-player 2D arcade game built with Pygame. 
    The player controls a spaceship using physics-based momentum to navigate space, avoid asteroids, 
    and shoot targets.

# Requirements

- Windows
- Python 3.13
- Pygame 2.6.1 (installed in the steps below)

# Download and run on Windows

1. Go to the [Ryan's Asteroids GitHub repository](https://github.com/rywn2570/Ryan-s-Asteroids).
2. Click the green **Code** button, then choose **Download ZIP**.
3. When the ZIP file finishes downloading, right-click it and choose **Extract All...**.
4. Open the extracted `Ryan-s-Asteroids` folder in File Explorer.
5. Click the folder's address bar, type `powershell`, and press Enter.
6. In the PowerShell window, create a virtual environment:

   ```powershell
   py -3.13 -m venv .venv
   ```

7. Install Pygame:

   ```powershell
   .\.venv\Scripts\python.exe -m pip install pygame==2.6.1
   ```

8. Start the game:

   ```powershell
   .\.venv\Scripts\python.exe main.py
   ```    
    
# Controls:
    - A / D: Rotate the spaceship
    - W: Activate thrusters
    - SPACEBAR (Quick): Fires weapon once.
    - SPACEBAR (Held): Fires a beam, then cools down.
    - END: Quit
