# Battleship Game

This Python script offers players a customized version of Battleship where they can strategically position their own ships on the game board. The game then uses a density probability algorithm to determine the best possible moves, aiming to sink the player's ships as efficiently as possible.

## Features

- **Custom Ship Placement**: Players can strategically position their ships on the 10x10 game board. Available ship types and sizes include:
  - Aircraft Carrier (size: 5)
  - Battleship (size: 4)
  - Submarine (size: 3)
  - Cruiser (size: 3)
  - Destroyer (size: 2)

- **Game Modes**:
  - **Hunt Mode**: The algorithm systematically hunts for the player's ships using density probability calculations.
  - **Sink Mode**: After hitting a ship, the game switches to this mode to systematically sink the rest of the ship.
    
- **Statistics Tracking**: Players can track their turns, hits, misses, and remaining targets, providing valuable insights into their gameplay strategy.

## Notes

- The game ends when all opponent ships are sunk or when the player runs out of shots.
- Ships cannot overlap on the board. If there's an overlap, an error message will be displayed.

## Work in Progress

Please note that this code and model are still under active development.
