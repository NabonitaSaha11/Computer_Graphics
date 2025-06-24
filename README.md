# Computer Graphics
This repository contains all the lab contents that I solved concerning CSE423 (Graphics Design) taught in Spring 2025. The lab assignments and project were done keeping focus on OpenGL.

The master branch has got all the files uploaded in total - ready for use. I have attached the individual files in the main branch along with the tasks that were told to be done for our assignments along with the individual files. 

# Project: 3D Snake and Ladder Adventure 
Rules of the game: 
1. The game world is a 10x10 3D grid
2. The player starts at a corner of the grid.Movement is based on dice rolls (1 to 6 steps forward depending on dice outcome).
3. Player has a limited number of lives/health points (e.g., 3-5). If the player reaches a ladder tile, the player is lifted upward (higher Z-axis).Player automatically descends when moving forward after being on a ladder tile.
4. A dynamic snake moves randomly across the grid.Snake starts moving only after the player reaches the second row.
Snake randomly chooses a direction (left, right, up, down) at each step.
Snake speed increases after certain time intervals.The snake always stays at ground level (cannot climb ladders).
5.If the snake touches the player (on the ground level), the player loses a life and resets to the starting position.
6.While on a ladder (elevated), the player is safe — snake cannot reach or harm the player.After a dice roll, if moving forward brings the player off the elevated platform, the player returns to ground level and becomes vulnerable again.
7.If the player loses all lives, the game displays a "Game Over" message.
If the player reaches the final grid (top-right corner), the player wins the game.
