# AI Project 1: Search - Pac-Man Ghosts

## 📌 Introduction

This project focuses on implementing search algorithms for ghosts in the classic **Pac-Man** game.
The goal is to develop intelligent ghost behaviors using **BFS, DFS, UCS, and A* Search** and evaluate their performance.

## 🚀 Features

✅ **Blue Ghost (BFS)** - Explores all possible paths evenly.

✅ **Pink Ghost (DFS)** - Searches deeply before backtracking.

✅ **Orange Ghost (UCS)** - Finds the lowest-cost path.

✅ **Red Ghost (A\*)** - Uses heuristics for optimal pathfinding.

✅ **Parallel Execution** - All ghosts move simultaneously.

✅ **User-Controlled Pac-Man** - Players can interact in real-time.

## 🛠 Technologies Used

- **Python** 🐍
- **Pygame** (for visualization) 🎮
- **Matplotlib** (for performance analysis) 📊

## 📂 Project Structure

```plaintext
📦 AI-Project-Search
 ┣ 📂 assets
 ┃ ┣ 📜 game_over.png      # Game over screen
 ┃ ┣ 📂 ghost_images       # Ghost sprites
 ┃ ┃ ┣ 📜 blue.png
 ┃ ┃ ┣ 📜 dead.png
 ┃ ┃ ┣ 📜 orange.png
 ┃ ┃ ┣ 📜 pink.png
 ┃ ┃ ┣ 📜 powerup.png
 ┃ ┃ ┗ 📜 red.png
 ┃ ┣ 📂 player_images      # Player sprites
 ┃ ┃ ┣ 📜 1.png
 ┃ ┃ ┣ 📜 2.png
 ┃ ┃ ┣ 📜 3.png
 ┃ ┃ ┗ 📜 4.png
 ┣ 📜 README.md            # Project documentation
 ┣ 📜 requirements.txt      # Dependencies
 ┣ 📂 src
 ┃ ┣ 📜 main.py            # Entry point
 ┃ ┣ 📜 board.py           # Game board logic
 ┃ ┣ 📜 ghost.py           # Ghost behavior
 ┃ ┣ 📜 player.py          # Player mechanics
 ┃ ┣ 📜 search.py          # Search algorithms (BFS, DFS, A*, UCS)
 ┃ ┗ 📜 performance.py     # Performance evaluation
 ┣ 📜 Report.pdf
 ┗ 📜 Demo.mp4
```

## 🎮 How to Run

1️⃣ **Install dependencies:**

```bash
conda install --file requirements.txt
# or
pip install -r requirements.txt
```

2️⃣ **Run the main script:**

```bash
python src/main.py
```

3️⃣ **Control Pac-Man (if implemented):**

- Arrow keys to move

## 🎥 Demo

📺 [Watch the demo here](#)
