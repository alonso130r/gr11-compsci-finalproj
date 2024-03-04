import random
from math import sin, radians

class Star:
    def __init__(self, x, y, max_brightness):
        #######################################################################
        # Function Name: __init__
        # Function Purpose: initialize the Star class
        # Parameters: self, x, y, max_brightness
        # Variables (Locally defined): self.x, self.y, self.brightness, self.max_brightness, self.speed
        # Return: none
        #######################################################################

        self.x = x
        self.y = y
        self.brightness = 0
        self.max_brightness = max_brightness
        self.speed = random.uniform(2, 4)  # Adjust speed for different fading effects

    def update(self):
        #######################################################################
        # Function Name: update
        # Function Purpose: update the stars to their new brightness
        # Parameters: self
        # Variables (Locally defined): none
        # Return: none
        #######################################################################

        self.brightness += self.speed
        if self.brightness > self.max_brightness or self.brightness < 0:
            self.speed *= -1  # Reverse the direction of fading

    def display(self):
        #######################################################################
        # Function Name: display
        # Function Purpose: display the stars' new brightness
        # Parameters: self
        # Variables (Locally defined): none
        # Return: none
        #######################################################################

        fill(255, 255, 255, self.brightness)
        noStroke()
        ellipse(self.x, self.y, 5, 5)  # Adjust size if needed

class WelcomeScreen:
    def __init__(self, message, width=800, height=600, num_stars=100):
        #######################################################################
        # Function Name: __init__
        # Function Purpose: initialize the WelcomeScreen class
        # Parameters: self, message, width, height, num_stars
        # Variables (Locally defined): self.message, self.width, self.height, self.stars, self.textSize, self.text_size, self.text_size_change, self.color_angle, self.color_array
        # Return: none
        #######################################################################

        self.message = message
        self.width = width
        self.height = height
        self.stars = [Star(random.randint(0, width), random.randint(0, height), random.randint(100, 255)) for _ in range(num_stars)]
        self.text_size = 26
        self.text_size_change = 0.03  # Rate at which text size changes
        self.color_angle = 0  # Starting angle for color change
        self.color_array = []
        
    def update(self):
        #######################################################################
        # Function Name: update
        # Function Purpose: update the stars and text for the next display call
        # Parameters: self
        # Variables (Locally defined): star
        # Return: none
        #######################################################################

        # update stars
        for star in self.stars:
            star.update()
            
        # Update text size for pulsing effect
        self.text_size += self.text_size_change
        if self.text_size > 32 or self.text_size < 20:  # Adjust these limits as needed
            self.text_size_change *= -1  # Reverse the direction of size change

        # Update text color for rainbow effect
        self.color_angle += 2
        if self.color_angle > 360:
            self.color_angle = 0  # Reset angle after completing a full cycle
            
        self.color_array = self.rainbow_color(self.color_angle)
    
    def display(self):
        #######################################################################
        # Function Name: display
        # Function Purpose: display the next frame of the screen
        # Parameters: self
        # Variables (Locally defined): star
        # Return: none
        #######################################################################

        # display background with stars
        background(0)
        for star in self.stars:
            star.display()
        textSize(self.text_size)
        fill(self.color_array[0], self.color_array[1], self.color_array[2])
        textAlign(CENTER, CENTER)
        text(self.message, self.width / 2, self.height / 2)
        
    def rainbow_color(self, angle):
        #######################################################################
        # Function Name: rainbow_color
        # Function Purpose: generate the color for the rainbow text through sin waves
        # Parameters: self, angle
        # Variables (Locally defined): red, green, blue
        # Return: red, green, blue
        #######################################################################

        #Generate RGB color based on an angle
        red = sin(radians(angle)) * 127 + 128
        green = sin(radians(angle + 120)) * 127 + 128
        blue = sin(radians(angle + 240)) * 127 + 128
        return int(red), int(green), int(blue)
