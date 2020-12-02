import random
import math
import pygame

# Initialize the pygame
pygame.init()

# Create the screen
# To access the modules inside pygame 
screen = pygame.display.set_mode( (800, 600) )

        # Anything happening inside our game window is an "Event".

# Background        
background = pygame.image.load("background.png")

# Background Music
pygame.mixer.music.load("background.wav")
# -1 is added because we have to play the sound constantly
pygame.mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)


# Player
playerImg = pygame.image.load("space-invaders.png")

# Coordinates (or position) where the player will be positioned
playerX = 370
playerY = 480
playerX_change = 0

def player(x, y):                                                # Player Function
    # blit function is used to draw an image of player onto our screen
    screen.blit(playerImg, (x, y))


# Enemy
alienImg = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
max_aliens = 6

# Coordinates (or positions) where the enemy will be positioned
for i in range(max_aliens):
    alienImg.append(pygame.image.load("alien.png"))
    alienX.append(random.randint(0, 736))
    alienY.append(random.randint(50, 150))
    alienX_change.append(1.5)
    alienY_change.append(40)


def enemy(x, y, i):                                               # Enemy Function
    screen.blit(alienImg[i], (x, y))


# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletY_change = 4

# Bullet State
# Ready = You can't see the bullet on the screen 
# Fire = The bullet is currently moving
bullet_state = "ready"

def fire_bullet(x, y):                                            # Fire Bullet Function
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


# Collision Score Count
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 35)

textX = 20
textY = 20

def show_score(x, y):                                              # Show Score Function
    # Font is not displayed (or blited) diirectly onto the screen
    # It is rendered in a new object, which is then blited onto the screen
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def isCollision(alienX, alienY, bulletX, bulletY):                 # Collision Funtion

    # Calculate distance between 2 coordinates (i.e. bullet and alien)
    distance = math.sqrt(( math.pow((alienX - bulletX), 2) ) + ( math.pow((alienY - bulletY), 2) ))
    if distance < 27:
        return True
    return False


# Game Over
game_over_font = pygame.font.Font("freesansbold.ttf", 40)

def game_over():                                                   # Game Over Function
    game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (270, 260))


# Whenever we want to exit our game we will change our running variable to False.
running = True

# Game Loop
while running:

    # Giving Background color in rgb format
    screen.fill( (0, 0, 0) )

    # Background Image
    screen.blit(background, (0, 0))

    # for looping through the events happening inside our game window 
    for event in pygame.event.get():
        
        # Check whenever the close window is pressed, change running var to False
        if event.type == pygame.QUIT:
            running = False

        # If Keystroke is Pressed check whether it's left key or right key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # When left key is pressed, we decrease the value by 0.1
                playerX_change = -3

            if event.key == pygame.K_RIGHT:
                # When rigth key is pressed, we increase the value by 0.1
                playerX_change = 3

            if event.key == pygame.K_SPACE:
                # Bullet state is ready, only then fire another bullet
                if bullet_state == "ready":
                    # Adding sound of bullet being shot
                    bullet_sound = pygame.mixer.Sound("laser.wav")
                    bullet_sound.play()
                    # Gets the current position where the player is and from that position bullet is fired
                    bulletX = playerX
                    # When space bar is pressed, bullet will be fired
                    fire_bullet(bulletX, bulletY)    

        # If Keystroke is Released        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # When key will be released the player will not move.
                playerX_change = 0            

    playerX = playerX + playerX_change

    # Setting the boundary for the ship, so that it doesn't move out of the screen
    if playerX <= 0:
        playerX = 0

    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(max_aliens):

        # Game Over Conditions
        if alienY[i] > 440:
            for j in range(max_aliens):
                alienY[j] = 2000
                playerY = 2000
                bulletY = 2000
                bulletY_change = 2000
            game_over()
            break    

        alienX[i] += alienX_change[i]

        if alienX[i] <= 0:
            alienX_change[i] = 1.5
            alienY[i] += alienY_change[i]

        elif alienX[i] >= 736:
            alienX_change[i] = -1.5
            alienY[i] += alienY_change[i]  

        # Enemy Function Calling
        enemy(alienX[i], alienY[i], i)

        # Collision Operations
        if isCollision(alienX[i], alienY[i], bulletX, bulletY):
            bulletY = 480
            bullet_state = "ready"

            # Explosion Sound
            # When bullet hits the alien
            explosion_sound = pygame.mixer.Sound("explosion.wav")
            explosion_sound.play()
            
            # Score Updation
            score_value += 1
    
            # Creating new alien
            alienX[i] = random.randint(0, 736)
            alienY[i] = random.randint(50, 150)

    # Bullet Movement
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # When bullet goes out of bounds, we can then fire another bullet
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready" 

    # Function Calling
    player(playerX, playerY)
    show_score(textX, textY)

    # Updating the display window
    pygame.display.update()