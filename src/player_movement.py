import pygame
from config import *

class PlayerMovementHandler:
  
  def __init__(self):
      pass

  def get_input(self, player):
    keys = pygame.key.get_pressed()
    a_pressed = keys[pygame.K_a]
    d_pressed = keys[pygame.K_d]
    l_ctrl_pressed = keys[pygame.K_LCTRL]

    no_horizontal_input = not (a_pressed or d_pressed)
    conflicting_input = a_pressed and d_pressed

    if not player.is_sliding and (no_horizontal_input or conflicting_input):
      player.velocity.x = 0 

    # Left/Right movement
    if a_pressed and not player.is_sliding:
      player.facing_right = False
      player.velocity.x -= WALKING_ACCELERATION
      player.velocity.x = max(-WALKING_MAX_SPEED, player.velocity.x)

    if d_pressed and not player.is_sliding:
      player.facing_right = True
      player.velocity.x += WALKING_ACCELERATION
      player.velocity.x = min(WALKING_MAX_SPEED, player.velocity.x)
        
    # Sliding
    if not l_ctrl_pressed or not player.on_ground:
      player.is_sliding = False

    elif not player.is_sliding:
      player.is_sliding = True
      player.apply_slide_friction = False 

    elif not player.apply_slide_friction:
      accel_dir = 1 if player.facing_right else -1
      player.velocity.x += accel_dir * SLIDE_ACCELERATION

      if abs(player.velocity.x) >= MAX_SLIDE_SPEED:
        player.velocity.x = max(-MAX_SLIDE_SPEED, min(player.velocity.x, MAX_SLIDE_SPEED))
        player.apply_slide_friction = True 

    else:
      player.velocity.x *= 0 if abs(player.velocity.x) < 1 else SLIDE_FRICTION


  def apply_gravity(self, player):
      player.velocity.y += GRAVITY
      if player.velocity.y > 20:
          player.velocity.y = 20


  def check_horizontal_collisions(self, player, platforms):
    collided_platforms = pygame.sprite.spritecollide(player, platforms, False)
    
    for platform in collided_platforms:
      if player.velocity.x > 0:
        player.rect.right = platform.rect.left
      elif player.velocity.x < 0:
        player.rect.left = platform.rect.right
    
    if player.rect.left < 0:
      player.rect.left = 0
    if player.rect.right > SCREEN_WIDTH:
      player.rect.right = SCREEN_WIDTH


  def check_vertical_collisions(self, player, platforms):
    collided_platforms = pygame.sprite.spritecollide(player, platforms, False)

    if not collided_platforms:
      player.on_ground = False
      return

    for platform in collided_platforms:

      if player.velocity.y < 0:
        player.rect.top = platform.rect.bottom
        player.velocity.y = 0

      elif player.velocity.y > 0:
        player.rect.bottom = platform.rect.top
        player.velocity.y = 0

        # Check if we *just* landed
        if not player.on_ground:
          player.on_ground = True
          
          # Check if it was a slam
          if player.is_slamming:
            player.is_slamming = False
            player.image = player.original_image
            player.slam_jump_timer = SLAM_JUMP_WINDOW
                    

  def update_state(self, player, platforms, enemies):
    # 1. Update all active timers
    self.update_timers(player)

    # 2. Check high-priority states
    if player.is_dashing:
      player.rect.x += player.velocity.x
      self.check_horizontal_collisions(player, platforms) # <-- New call
      return
    
    if player.is_slamming:
      player.velocity.x = 0
      player.velocity.y = DASH_SPEED
      player.rect.y += player.velocity.y
      self.check_vertical_collisions(player, platforms) # <-- New call
      return
        
    # 3. Normal movement (if not dashing or slamming)
    self.get_input(player)
    self.apply_gravity(player)
    
    # Move X, then check X
    player.rect.x += player.velocity.x
    self.check_horizontal_collisions(player, platforms)
    
    # Move Y, then check Y
    player.rect.y += player.velocity.y
    self.check_vertical_collisions(player, platforms)

  def update_timers(self, player):

    # Dash Duration Timer (while you are *in* the dash)
    if player.dash_timer > 0:
      player.dash_timer -= 1
      if player.dash_timer <= 0:
        player.is_dashing = False
        player.velocity.x = 0
        player.image = player.original_image
        
    # Check if we are below max charges AND the timer isn't already running
    if player.dash_charges < player.max_dash_charges and player.dash_cooldown_timer <= 0:
      player.dash_cooldown_timer = DASH_COOLDOWN

    # --- Dash Regen Timer ---
    if player.dash_cooldown_timer > 0:
      player.dash_cooldown_timer -= 1
      if player.dash_cooldown_timer == 0:
        player.dash_charges += 1

    # --- Slam Jump Timer ---
    if player.slam_jump_timer > 0:
      player.slam_jump_timer -= 1
      if player.slam_jump_timer == 0:
        player.current_jump_multiplier = 1.0