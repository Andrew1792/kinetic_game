import pygame
from config import *

class PlayerMovementHandler:
    
    def __init__(self):
        pass

    def get_input(self, player):
        player.velocity.x = 0
        keys = pygame.key.get_pressed()

        # Left/Right movement
        if keys[pygame.K_a]:
            player.velocity.x = -PLAYER_SPEED
            player.facing_right = False

        if keys[pygame.K_d]:
            player.velocity.x = PLAYER_SPEED
            player.facing_right = True


    def apply_gravity(self, player):
        player.velocity.y += GRAVITY
        
        if player.velocity.y > 20: # Terminal velocity
            player.velocity.y = 20


    def check_collisions(self, player):

      # --- Floor Collision ---
      if player.rect.bottom >= SCREEN_HEIGHT - 20:
        player.rect.bottom = SCREEN_HEIGHT - 20
        player.velocity.y = 0
        
        # --- Reset logic when touching ground ---
        if not player.on_ground:
            player.dash_charges = player.max_dash_charges
            
            # Check if this was a SLAM landing
            if player.is_slamming:
                player.is_slamming = False
                player.image = player.original_image
                
                # Start the jump window
                player.slam_jump_timer = SLAM_JUMP_WINDOW
            
            # --- Handle a NORMAL landing ---
            else:
                if player.slam_jump_timer <= 0: 
                    player.current_jump_multiplier = 1.0

        player.on_ground = True

        # --- Wall Collision ---
        if player.rect.left < 0:
            player.rect.left = 0
        if player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH


    def update_timers(self, player):
        # Dash Duration Timer (while you are *in* the dash)
        if player.dash_timer > 0:
            player.dash_timer -= 1

            if player.dash_timer <= 0:
                player.is_dashing = False
                player.velocity.x = 0
                player.image = player.original_image
        
        # Dash Cooldown Timer (the "recovery" *between* dashes)
        if player.dash_cooldown_timer > 0:
            player.dash_cooldown_timer -= 1

        # --- Slam Jump Timer ---
        if player.slam_jump_timer > 0:
            player.slam_jump_timer -= 1
            
            if player.slam_jump_timer <= 0:
                player.current_jump_multiplier = 1.0

    
    def update_state(self, player):
        # 1. Update all active timers
        self.update_timers(player)

        # 2. Check high-priority states
        
        # State: Dashing
        if player.is_dashing:
            player.rect.x += player.velocity.x
            self.check_collisions(player)
            return
        
        # State: Slamming
        if player.is_slamming:
            player.velocity.x = 0
            player.velocity.y = DASH_SPEED
            
            player.rect.y += player.velocity.y
            player.rect.x += player.velocity.x
            self.check_collisions(player)
            return
            
        # 3. Normal movement (if not dashing or slamming)
        self.get_input(player)
        self.apply_gravity(player)
        player.rect.x += player.velocity.x
        player.rect.y += player.velocity.y
        
        # 4. Final collision check
        self.check_collisions(player)