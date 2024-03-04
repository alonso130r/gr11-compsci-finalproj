import random

class Player:
    def __init__(self, x, y, block_pos, img, minim, bg):
        #######################################################################
        # Function Name: __init__
        # Function Purpose: initialize all user passed variables to the object
        # Parameters: self, x, y, block_pos, img, minim, bg
        # Variables (Locally defined): self.initial_x, self.initial_y, self.initial_block_pos, self.initial_img, self.minim, self.jump_sound, self.bg_img
        # Return: none
        #######################################################################

        self.initial_x = x
        self.initial_y = y
        self.initial_block_pos = block_pos
        self.initial_img = img
        self.reset()
        self.minim = minim
        self.jump_sound = self.minim.loadSample('jump.mp3', 128)
        self.bg_img = bg

    def reset(self):
        #######################################################################
        # Function Name: reset
        # Function Purpose: set all non-user defined variables to their original state (used to initialize game, and reset after 0 lives)
        # Parameters: self
        # Variables (Locally defined): self.pos, self.vel, self.acc, self.gravity, self.jump_strength, self.block_pos, self.player, self.current_jump_frame, self.jump_frames = 0, self.on_ground, self.jumps_made, self.width, self.height
        # Variables (cont.) : self.enemy_img, self.enemies, self.lives, self.collision cooldown, self.heart_img, self.missiles, self.missile_img, self.is_invincible, self.invincibility_timer, self.invincibility_duration, self.powerups
        # Return: none
        #######################################################################

        self.pos = PVector(self.initial_x, self.initial_y)
        self.vel = PVector(0, 0)
        self.acc = PVector(0, 0)
        self.gravity = PVector(0, 1.6)
        self.jump_strength = -90
        self.block_pos = self.initial_block_pos
        self.player = self.initial_img
        self.current_jump_frame = 0
        self.jump_frames = 0
        self.on_ground = False
        self.jumps_made = 0
        self.width = self.player.width
        self.height = self.player.height
        
        self.enemy_img = loadImage("enemy.png")  # Reload enemy image
        self.enemy_img.resize(18, 0)
        self.enemies = [Enemy(platform, self.enemy_img) for platform in self.block_pos]
        self.lives = 3
        self.collision_cooldown = 0
        
        self.heart_img = loadImage("heart.png")  # Reload heart image
        self.heart_img.resize(60, 0)
        
        self.missiles = []  # Reset the list to store missiles
        self.missile_img = loadImage("missile.png")  # Reload the missile image
        self.missile_img.resize(40, 0)
        
        self.is_invincible = False
        self.invincibility_timer = 0
        self.invincibility_duration = 300  # 5 seconds at 60 fps
        
        self.powerups = []
        
    def enemy_dies(self):
        #######################################################################
        # Function Name: enemy_dies
        # Function Purpose: if an enemy dies, call the powerup logic
        # Parameters: self
        # Variables (Locally defined): powerup_type
        # Return: none
        #######################################################################

        if random.random() <= 0.5:  # 50% chance to drop a power-up
            powerup_type = random.choice(["life", "shield"])  # Randomly choose a type
            self.powerups.append(powerup_type)
        
    def apply_powerup_effect(self, powerup):
        #######################################################################
        # Function Name: apply_powerup_effect
        # Function Purpose: apply the powerup effects, then remove them from the array
        # Parameters: self, powerup
        # Variables (Locally defined): none
        # Return: none
        #######################################################################

        if powerup == "life":
            self.lives += 1
        elif powerup == "shield":
            self.activate_invincibility()
        
    def activate_invincibility(self):
        #######################################################################
        # Function Name: activate_invincibility
        # Function Purpose: activate the invincibility
        # Parameters: self
        # Variables (Locally defined): none
        # Return: none
        #######################################################################

        self.is_invincible = True
        self.invincibility_timer = self.invincibility_duration    

    def are_all_enemies_dead(self):
        #######################################################################
        # Function Name: are_all_enemies_dead
        # Function Purpose: check if all enemies are dead, so that we can move on to the next stage
        # Parameters: self
        # Variables (Locally defined): enemy
        # Return: False (enemies alive), True (enemies all dead)
        #######################################################################

        for enemy in self.enemies:
            if enemy.is_alive:
                return False
        return True
        
    def find_nearest_enemy(self, enemies, range):
        #######################################################################
        # Function Name: find_nearest_enemy
        # Function Purpose: find the enemy nearest to the player in a certain range, for the missile targeting system
        # Parameters: self, enemies, range
        # Variables (Locally defined): nearest_enemy, min_distance, enemy, distance
        # Return: nearest_enemy
        #######################################################################

        nearest_enemy = None
        min_distance = range # radius to search for enemies in
        for enemy in enemies:
            if not enemy.is_alive:
                continue  # Skip dead enemies
            distance = self.pos.dist(enemy.pos)
            if distance < min_distance:
                min_distance = distance
                nearest_enemy = enemy
        return nearest_enemy
        
    def launch_missile(self, enemies):
        #######################################################################
        # Function Name: launch_missile
        # Function Purpose: create/launch a missile object at the target found in find_nearest_enemy, or in a random direction if no target
        # Parameters: self, enemies
        # Variables (Locally defined): nearest_enemy, missile
        # Return: none
        #######################################################################

        nearest_enemy = self.find_nearest_enemy(enemies, 200)
        if nearest_enemy: # targeted
            missile = Missile(self.pos.x, self.pos.y, self.missile_img, self, self.minim, nearest_enemy)
        else: # no target
            missile = Missile(self.pos.x, self.pos.y, self.missile_img, self, self.minim)
        self.missiles.append(missile)
        
    def update_missiles(self, enemies):
        #######################################################################
        # Function Name: update_missiles
        # Function Purpose: update the missiles by updating their position, checking for collisions, and removing them if inactive
        # Parameters: self, enemies
        # Variables (Locally defined): missile
        # Return: none
        #######################################################################

        for missile in self.missiles[:]:  # Iterate over a copy of the list
            if missile.active:
                missile.update()
                missile.check_collision_with_enemies(enemies)
            else:
                self.missiles.remove(missile)  # Remove inactive missile
    
    def display_lives(self):
        #######################################################################
        # Function Name: display_lives
        # Function Purpose: to display the amount of lives as hearts drawn in the top right corner
        # Parameters: self
        # Variables (Locally defined): none
        # Return: none
        #######################################################################

        for i in range(self.lives):
            image(self.heart_img, width - (i + 1) * (self.heart_img.width + 10), 10)
            
    def check_enemy(self, enemies):
        #######################################################################
        # Function Name: check_enemy
        # Function Purpose: to check if the player has ran into an enemy, and remove a life if so
        # Parameters: self, enemies
        # Variables (Locally defined): enemy
        # Return: none
        #######################################################################

        if self.collision_cooldown == 0 and not self.is_invincible:
            for enemy in enemies:
                if enemy.check_collision_with_player(self):
                    self.lives -= 1
                    self.collision_cooldown = 60  # Reset cooldown to 60 frames
                    if self.lives <= 0:
                        self.reset()
                    break  # Exit the loop after a collision

    def apply_gravity(self):
        #######################################################################
        # Function Name: apply_gravity
        # Function Purpose: apply exponential gravity to the player for a more realistic fall
        # Parameters: self
        # Variables (Locally defined): gravity_factor, max_gravity
        # Return: none
        #######################################################################

        gravity_factor = 1.02 # exponentiation factor
        max_gravity = 5 # max fall speed

        if not self.on_ground:
            self.gravity.mult(gravity_factor)
        else:
            self.gravity = PVector(0, 1.6)
    
        self.gravity.y = constrain(self.gravity.y, -max_gravity, max_gravity)
        self.acc.add(self.gravity)
        
    def jump(self):
        #######################################################################
        # Function Name: jump
        # Function Purpose: to handle all jumping related logic, including triple jumps and calling missile launch
        # Parameters: self
        # Variables (Locally defined): none
        # Return: none
        #######################################################################

        if self.on_ground or self.jumps_made < 2:
            # Increment jump count
            self.jumps_made += 1
            
            self.jump_sound.trigger()
            
            # Perform the jump
            self.jump_frames = 5
            self.jump_increment = self.jump_strength / self.jump_frames
            self.current_jump_frame = 0
            self.on_ground = False
    
            # Launch missile on triple jump (Don't ask why this is reachable because processing decided it is)
            if self.jumps_made == 2:
                self.launch_missile(self.enemies)

    
    def check_platform_collision(self):
        #######################################################################
        # Function Name: check_platform_collision
        # Function Purpose: to check if a player is on a platform, and have them land on it
        # Parameters: self
        # Variables (Locally defined): player_bottom, player_left_edge, player_right_edge, on_a_platform, platform
        # Return: none
        #######################################################################

        player_bottom = self.pos.y + self.height
        player_left_edge = self.pos.x
        player_right_edge = self.pos.x + self.width
    
        on_a_platform = False
    
        for platform in self.block_pos:
            platform_top = platform.y + 10
            platform_left = platform.x + 27.5
            platform_right = platform.x + platform.width - 27.5
    
            # Check if the player is above the platform (vertically) and within the platform boundaries (horizontally)
            if (player_bottom >= platform_top and 
                player_bottom < platform_top + 10 and  # Assuming 10 is a reasonable threshold
                player_right_edge > platform_left and 
                player_left_edge < platform_right):
                
                on_a_platform = True
                self.pos.y = platform_top - self.height
                self.vel.y = 0  # Stop vertical movement
                self.on_ground = True
                self.jumps_made = 0
                break  # Stop checking other platforms
    
        # If the player is not on any platform, they have walked off
        if not on_a_platform:
            self.on_ground = False

    def update(self):
        #######################################################################
        # Function Name: update
        # Function Purpose: to update the player's position and update all other items that are running at the same time
        # Parameters: self
        # Variables (Locally defined): damping, max_speed, enemy, powerup
        # Return: none
        #######################################################################

        self.apply_gravity()

        # Update velocity and position
        self.vel.add(self.acc)
        self.pos.add(self.vel)
        self.acc.mult(0)

        # Damping for the velocity
        damping = 0.6
        self.vel.mult(damping)

        # Constrain the velocity to a maximum value
        max_speed = 5
        self.vel.x = constrain(self.vel.x, -max_speed, max_speed)
        self.vel.y = constrain(self.vel.y, -max_speed, max_speed)

        # Ground constraint
        if self.pos.y > height - 20:
            self.pos.y = height - 20
            self.vel.y = 0
        
        # Gradual jump strength
        if self.current_jump_frame < self.jump_frames:
            self.acc.add(PVector(0, self.jump_increment))
            self.current_jump_frame += 1
        
        # move enemies and powerup check
        for enemy in self.enemies:
            enemy.move()
            enemy.powerup_spawn(self)
        
        # check collisions with enemy
        self.check_enemy(self.enemies)
        
        # Decrement the collision cooldown timer
        if self.collision_cooldown > 0:
            self.collision_cooldown -= 1
            
        # update missiles
        self.update_missiles(self.enemies)
        
        # apply then remove powerups
        for powerup in self.powerups[:]:
            self.apply_powerup_effect(powerup)
            self.powerups.remove(powerup)
        
        # apply invincibility
        if self.is_invincible:
            self.invincibility_timer -= 1
            if self.invincibility_timer <= 0:
                self.is_invincible = False

    def display(self):
        #######################################################################
        # Function Name: display
        # Function Purpose: display the changes made in update
        # Parameters: self
        # Variables (Locally defined): platform, enemy, missile, text_width_value, text_height_value, padding
        # Return: none
        #######################################################################
        
        # bg image, platform fill
        image(self.bg_img, 0, 0)
        fill('#03fc5e')
        
        # platforms
        for platform in self.block_pos:
            platform.display()
        
        # enemies
        for enemy in self.enemies:
            enemy.display()
            
        # missiles
        for missile in self.missiles:
            missile.display(self.missile_img)
            
        # invincibility message
        if self.is_invincible:
            # Set the text size first to measure the text
            textSize(24)
    
            # Calculate the width and height for the background rectangle
            text_width_value = textWidth("INVINCIBILITY ACTIVE")
            text_height_value = 24  # Height roughly matches the text size
            padding = 10  # You can adjust the padding
    
            # Draw the black rectangle behind the text
            fill(0)  # Black color
            rectMode(CENTER)
            rect(400, 50, text_width_value + padding, text_height_value + padding)
    
            # Now draw the text over the rectangle
            fill('#00FF01')  # Green color for the text
            textAlign(CENTER, CENTER)
            text("INVINCIBILITY ACTIVE", 400, 50)
            rectMode(CORNER)
            
        # display lives
        self.display_lives()
        
        # display player
        image(self.player, self.pos.x, self.pos.y)
        
class Platform:
    def __init__(self, x, y, width, height):
        #######################################################################
        # Function Name: __init__
        # Function Purpose: initialize the Platform class
        # Parameters: self, x, y, width, height
        # Variables (Locally defined): self.x, self.y, self.width, self.height
        # Return:none
        #######################################################################

        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def display(self):
        #######################################################################
        # Function Name: display
        # Function Purpose: display the platforms
        # Parameters: self
        # Variables (Locally defined): none
        # Return: none
        #######################################################################

        fill('#03fc5e')
        rect(self.x, self.y, self.width, self.height)


class Enemy:
    def __init__(self, platform, img):
        #######################################################################
        # Function Name: __init__
        # Function Purpose: initialize the Enemy class
        # Parameters: self, platform, img
        # Variables (Locally defined): self.pos, self.platform, self.enemy_img, self.is_alive, self.direction, self.speed, self.powerup_spawned
        # Return: none
        #######################################################################

        # Position the enemy at the center of the platform
        self.pos = PVector(platform.x + platform.width / 2, platform.y - img.height)
        self.platform = platform
        self.enemy_img = img
        self.is_alive = True
        self.direction = 1  # Initial movement direction
        self.speed = 2  # Speed of enemy movement
        self.powerup_spawned = False

    def move(self):
        #######################################################################
        # Function Name: move
        # Function Purpose: move the enemy side to side within platform boundaries
        # Parameters: self
        # Variables (Locally defined): none
        # Return: none
        #######################################################################

        # Move the enemy side to side within the platform boundaries
        if self.pos.x > self.platform.x + self.platform.width - self.enemy_img.width:
            self.direction = -1
        elif self.pos.x < self.platform.x:
            self.direction = 1

        self.pos.x += self.speed * self.direction

    def display(self):
        #######################################################################
        # Function Name: display
        # Function Purpose: display the enemy at the moved position
        # Parameters: self
        # Variables (Locally defined): none
        # Return: none
        #######################################################################
        
        # display if alive
        if self.is_alive:
            image(self.enemy_img, self.pos.x, self.pos.y)

    def check_collision_with_player(self, player):
        #######################################################################
        # Function Name: check_collision_with_player
        # Function Purpose: check if the player has hit the enemy
        # Parameters: self, player
        # Variables (Locally defined): buffer
        # Return: True (if collision), False (if no collision)
        #######################################################################

        if not self.is_alive:
            return False  # Skip collision check if the enemy is dead
        
        buffer = 26  # Adjust this value to change the collision range

        # Adjusted collision logic with buffer
        if (self.pos.x + buffer < player.pos.x + player.width and
            self.pos.x + self.enemy_img.width - buffer > player.pos.x and
            self.pos.y + buffer < player.pos.y + player.height and
            self.pos.y + self.enemy_img.height - buffer > player.pos.y):
            self.is_alive = False
            return True
        return False
    
    def powerup_spawn(self, player):
        #######################################################################
        # Function Name: powerup_spawn
        # Function Purpose: start the powerup logic inside the player class
        # Parameters: self, player
        # Variables (Locally defined): none
        # Return: none
        #######################################################################

        # spawn powerup only if not alive and powerup not yet spawned
        if not self.is_alive and not self.powerup_spawned:
            player.enemy_dies()
            self.powerup_spawned = True
    
    
class Missile:
    def __init__(self, x, y, missile_img, player, minim, target=None):
        #######################################################################
        # Function Name: __init__
        # Function Purpose: initialize the Missile class
        # Parameters: self, x, y, missile_img, player, minim, target (default -> None)
        # Variables (Locally defined): self.pos, self.target, self.speed, self.active, self.missile_img, self.player, self.impact, self.vel, angle
        # Return: none
        #######################################################################

        self.pos = PVector(x, y)
        self.target = target
        self.speed = 5
        self.active = True
        self.missile_img = missile_img
        self.player = player
        self.impact = minim.loadSample('explode.mp3', 128)
        
        if self.target:
            self.vel = PVector(0, -5)  # Initial velocity towards the target
        else:
            # Set a random velocity if no target is given
            angle = random.uniform(0, TWO_PI)  # Random angle
            self.vel = PVector.fromAngle(angle) * self.speed
        
    def check_collision_with_enemies(self, enemies):
        #######################################################################
        # Function Name: check_collision_with_enemies
        # Function Purpose: check if the missile has collided with an enemy
        # Parameters: self, enemies
        # Variables (Locally defined): enemy
        # Return: none
        #######################################################################

        # collision logic with enemies
        for enemy in enemies:
            if (self.pos.x < enemy.pos.x + enemy.enemy_img.width and
                self.pos.x + self.missile_img.width > enemy.pos.x and
                self.pos.y < enemy.pos.y + enemy.enemy_img.height and
                self.pos.y + self.missile_img.height > enemy.pos.y):
                enemy.is_alive = False
                self.active = False
                self.impact.trigger()
                break  # Exit the loop after a collision

    def update(self):
        #######################################################################
        # Function Name: update
        # Function Purpose: update the missile position
        # Parameters: self
        # Variables (Locally defined): direction
        # Return: none
        #######################################################################

        if self.target and self.active:
            # Homing missile logic
            direction = PVector.sub(self.target.pos, self.pos)
            direction.normalize()
            direction.mult(self.speed)
            self.vel = direction
        # If no target, the missile continues in its initial random direction

        self.pos.add(self.vel)

    def display(self, img):
        #######################################################################
        # Function Name: display
        # Function Purpose: display the missile at the updated location
        # Parameters: self, img
        # Variables (Locally defined): none
        # Return: none
        #######################################################################

        # display missile
        if self.active:
            image(img, self.pos.x, self.pos.y)
