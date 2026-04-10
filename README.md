🎮 Catch the Ball – OpenGL Python Game



📌 Overview

Catch the Ball is a two-player OpenGL game built using Python, where both players choose a preferred color and try to catch falling balls of that color using their baskets.

The game includes:

Real-time falling balls

Basket movement for both players

Scoring, penalty, pause, restart & exit

Randomized ball colors & movement

🧩 Game Rules

Both players choose their preferred ball color at the start.

Players move their baskets to catch balls of their chosen color.

First player to catch 5 correct-colored balls wins.

If a player misses 15 balls of their own color, the other player wins by default.

Catching a wrong-colored ball resets your score to 0.

Use the Pause button to freeze/unfreeze the game.

Use Restart to reset game state.

The Cross icon closes the game.

🎮 Controls

Player 1 (Left Basket) – Keyboard
Key	Action

A	Move Left

D	Move Right

W	Move Up

S	Move Down

Player 2 (Right Basket) – Arrow Keys

Key	Action

←	Move Left

→	Move Right

↑	Move Up

↓	Move Down

Mouse Controls

Click	Action

Click Pause Button	Toggle pause/resume

Click Restart Button	Restart game

Click Cross Button	Close game

🚀 How to Run

Install dependencies:

pip install PyOpenGL PyOpenGL_accelerate

Run the game:

python catch_the_ball.py

🎨 Player Setup

At the start, the game shows:

Preferred color for Player 1:

Preferred color for Player 2:

Available colors:

yellow, red, blue, green, aqua, purple, orange

Player 2 cannot choose Player 1's selected color.

⚙️ Features Implemented

✔ Real-time falling balls with variable speeds

✔ Ball–basket collision detection

✔ Wrong catch resets score

✔ Miss counter for each player

✔ Win conditions

✔ Pause, restart, exit buttons

✔ Eight-way symmetry line drawing

✔ Midpoint line & circle algorithms

✔ Random horizontal ball wiggle

📁 File Structure (Suggested)

project/

│── catch_the_ball.py

│── README.md

│── assets/ (optional future use)



🏆 Win Conditions


Player catches 5 correct balls	That player wins

Player misses 15 of their color	Opponent wins

Wrong catch resets score	No winner, continue
