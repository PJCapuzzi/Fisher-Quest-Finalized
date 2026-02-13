# Two Player Platformer (Python + Pygame)

## Controls
- Player 1: W = Jump, S = Left, D = Right
- Player 2: I = Jump, J = Left, K = Right

## Win Condition
Both players must reach the goal zone (a rectangle) to win.

## Customize
- Edit physics/display: `config/game_config.json`
- Edit end-screen text/image path: `config/end_screen.json`
- Edit level rectangles/spawns/goal: `level/level1.json`
- Optional end image: `assets/ui/end_image.png`

## Run
```bash
pip install -r requirements.txt
python run_game.py
