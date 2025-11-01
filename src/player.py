import pygame
from config import *
from src.player_movement import PlayerMovementHandler

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((40, 50))
        self.image.fill(PLAYER_COLOR)
        
        # Store the original surface
        self.original_image = self.image 

        # --- Position & Physics ---
        self.rect = self.image.get_rect(midbottom = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50))
        self.velocity = pygame.Vector2(0, 0)
        self.on_ground = False
        self.facing_right = True 

        # --- Dash State ---
        self.max_dash_charges = MAX_DASH_CHARGES
        self.dash_charges = self.max_dash_charges
        
        self.is_dashing = False
        self.dash_timer = 0
        self.dash_cooldown_timer = 0
        
        # --- Slam State ---
        self.is_slamming = False
        
        # --- Slam-Jump State ---
        self.current_jump_multiplier = 1.0
        self.slam_jump_timer = 0
        
        # --- Logic Handler ---
        self.movement_handler = PlayerMovementHandler()


    def handle_event(self, event):
        # Handles one-time button presses (KEYDOWN)
        if event.type == pygame.KEYDOWN:
            # --- JUMP ---
            if event.key == pygame.K_w:
                self.jump()
            
            # --- DASH ---
            if event.key == pygame.K_LSHIFT:
                self.dash()
                
            # --- SLAM ---
            if event.key == pygame.K_s:
                self.slam()

    # --- ACTION/ABILITY METHODS (Triggers) ---

    def jump(self):
        if not self.on_ground:
            return

        # Start with base jump power
        final_jump_power = PLAYER_JUMP_POWER

        # --- Check for slam bonus ---
        if self.slam_jump_timer > 0:
            self.current_jump_multiplier *= SLAM_JUMP_BONUS
            self.current_jump_multiplier = min(self.current_jump_multiplier, MAX_JUMP_MULTIPLIER)
            self.slam_jump_timer = 0

        # --- Apply Slam Bonus ---
        final_jump_power *= self.current_jump_multiplier

        # --- Execute Jump ---
        self.velocity.y = final_jump_power
        self.on_ground = False


    def slam(self):
        if self.on_ground or self.is_dashing or self.is_slamming:
            return
            
        self.is_slamming = True
        self.velocity.y = DASH_SPEED
        self.velocity.x = 0
        
        # Visual feedback
        self.image = pygame.Surface((40, 50))
        self.image.fill(PLAYER_SLAM_COLOR)
        
        
    def dash(self):
        if self.on_ground or self.dash_charges <= 0 or self.is_dashing or self.dash_cooldown_timer > 0:
            return
        
        self.is_dashing = True
        self.is_slamming = False 
        
        self.dash_charges -= 1
        self.dash_timer = DASH_DURATION
        self.dash_cooldown_timer = DASH_COOLDOWN
        
        # Set dash velocity
        if self.facing_right:
            self.velocity.x = DASH_SPEED
        else:
            self.velocity.x = -DASH_SPEED
            
        # Negate gravity during the dash
        self.velocity.y = 0
        
        # Visual feedback
        self.image = pygame.Surface((40, 50))
        self.image.fill(PLAYER_DASH_COLOR)


    def update(self):
        self.movement_handler.update_state(self)