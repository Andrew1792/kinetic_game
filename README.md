# Pygame Platformer Engine

This is a 2D platformer game engine built with Python and Pygame.

## Core Engine Features

* **Class-Based Structure:** The game is organized into classes (`Game`, `Player`, `Platform`, `LevelLoader`)

* **Sprite Group Management:** Efficiently handles all game objects using `pygame.sprite.Group` for drawing, updating, and collisions.

* **JSON Level Loader:** Levels are loaded from `.json` files, allowing for easy creation and modification of levels without touching the game's code.

  * Loads platform positions and sizes.

  * Loads the player's starting coordinates.

  * Loads a custom background color for each level.

* **Persistent Player:** The `Player` object is persistent, meaning stats like health or score (when added) will carry over between levels.

* **Dynamic Level Reset:** A `player.reset()` method ensures the player's position and level-specific stats (like dash charges) are reset when a new level loads.

* **Automatic Level Boundaries:** The `LevelLoader` automatically generates a floor and a ceiling for every level.

## Player Movement Mechanics

The player has physics-based moveset inspired by other games (ultrakill)

* **Acceleration Movement:** Player movement is based on acceleration, not constant speed

* **Jumping:** A standard, velocity-based jump.

* **Dash:**

  * Can be performed on the ground or in the air.

  * Uses a multi-charge system (`MAX_DASH_CHARGES`).

  * Charges regenerate one by one after a cooldown. (capped at 3)

* **Slam:** A fast-fall move that cancels horizontal velocity and sends the player straight down.

* **Slam Jump (Stacking Bonus):**

  * Slamming and landing on a platform opens a brief `SLAM_JTUMP_WINDOW`.

  * Jumping within this window grants a `SLAM_JUMP_BONUS` (e.g., 1.5x jump height).

  * This bonus *stacks* with each successful slam jump (e.g., 1.5x -> 2.25x).

  * The bonus is capped at a `MAX_JUMP_MULTIPLIER` to prevent it from getting too high.

  * The bonus stack is reset to 1.0x after a single *normal* jump.

* **Slide:**

  * Holding 'Ctrl' on the ground initiates a slide.

  * The slide has its own acceleration phase up to a `MAX_SLIDE_SPEED`.

  * After reaching max speed, friction is applied to slow the slide down.