import pygame
import math
from assets.pygameAssets import basic_gun
background_colour = (0, 0, 0)
screen = pygame.display.set_mode((300, 300), pygame.RESIZABLE)
pygame.display.set_caption('Resolute')
cord_grid_offset = 35
cord_grid_size = 735

# game_state contains all information needed to run the game simulation
# game_state is a dict where
# - guns is a list of gun
# - enemies is a list of active enemies
# - bullets is a list of bullets currently in the game field
game_state = {"guns": [{"cord": (35, 35),
                                                                "health": 100,
                                                                "reload_timer": 2,
                                                                "reload_time": 5,
                                                                "damage": 10,
                                                                "velocity": 800,
                                                                "id": 123456}], "enemies": [], "bullets": [], "objects": []}

# gun is a gun on the game field
# gun is a dict where
# cord is a tuple containing the coordinates of the gun
# health is the health of a gun
# reload_timer is the count in ticks until the gun can fire again
# reload_time shows what value the reload timer should be reset to when 0
# damage indicates how much health (0 to 100) one bullet of the gun inflicts upon enemies
# velocity provides the speed of the bullet in pixels per second
# id is a random 6 digit number representing a gun object
gun_example = {"cord": (), "health": 100, "reload_timer": 2, "reload_time": 5, "damage": 10, "velocity": 800, "id": 123456}

# enemy is an enemy entitiy activly on the game field
# a enemy is a dict where
# cord is a tuple containing the coordinates of the enemy
# health is the health of a enemy
# target_cord is the cords of the enemy's target
# x velocity is the velocity in x direction in pixels per second
# y velocity is the velocity in y direction in pixels per second
# damage is the amount of damage a enemy does when colliding with a gun
# id is a random 6 digit number representing a enemy object
enemy_example = {"cord":(), "health": 100, "target_cord": (), "x_velocity": 100, "y_velocity": 200, "id": 654321}

# An object is a passive object located in the game field
# An object is a dict where
# cord is a tuple containing the coordinates of the object
# health is the health of an object
object_example = {"cord":(), "health": 100}

screen.fill(background_colour)
menu_items = [{"type":"basic", "x":753, "y": 0,}]

# A menu item is a item which the player can click on the side of the game field
# A menu is a dict where
# type is a type of gun or object referenced in pygameAssets.py with the same name as the definition
# x the x cords of the bound box for mouse collision
# y is the y cords of bound box for mouse collision
example_item = {"type":"basic", "x":0, "y": 0,}

#checks if mouse cords are over a menu item, returns true and the item type or false
def check_menu(cords):
    for item in menu_items:
        print(cords)
        if item["x"] <= cords[0] <= (item["x"] + 35) and item["y"] <= cords[1] <= (item["y"] + 35):
            return True, item["type"]
        else:
            return False, None

# Checks whether a gun should be placed. If the cords are over an existing gun or outside game field,e
# validate_placement will return False. Otherwise, it will return true
def validate_placement():
    x = math.floor(pygame.mouse.get_pos()[0] / 35) * 35
    y = math.floor(pygame.mouse.get_pos()[1] / 35) * 35
    for gun in game_state["guns"]:
        if gun["cord"][0] == x and gun["cord"][1] == y:
            return False

    if x >= 735 or y >= 735:
        return False
    else:
        return True

running = True
item_placement = False

# game loop
while running:
    # Creates the initial cord grid given grid size and offset
    for i in range(math.floor(cord_grid_size / cord_grid_offset)):
        pygame.draw.line(screen, (211, 211, 211), ((cord_grid_offset * i + cord_grid_offset), 0), ((cord_grid_offset * i + cord_grid_offset), cord_grid_size), 1)
        pygame.draw.line(screen, (211, 211, 211), (0, (cord_grid_offset * i)), (cord_grid_size, (cord_grid_offset * i)),
                         1)

    # Creates menu items selectable by player
    for item in menu_items:
        if item['type'] == "basic":
            basic_gun(pygame, screen, item["x"], item["y"])

    # Renders guns
    for gun in game_state["guns"]:
        basic_gun(pygame, screen, gun["cord"][0], gun["cord"][1])

    pygame.display.flip()
    # for loop through the event queue
    for event in pygame.event.get():

        # Check for QUIT event
        if event.type == pygame.QUIT:
            running = False

        # checks if the mouse is being pressed
        if pygame.mouse.get_pressed()[0]:
            if item_placement == False:
                item_check_res, item_type = check_menu(pygame.mouse.get_pos())
                if item_check_res:
                    item_placement = True
            elif validate_placement():
                item_placement = False
                x = math.floor(pygame.mouse.get_pos()[0] / 35) * 35
                y = math.floor(pygame.mouse.get_pos()[1] / 35) * 35
                game_state["guns"].append({"cord": (x, y),
                                                                "health": 100,
                                                                "reload_timer": 2,
                                                                "reload_time": 5,
                                                                "damage": 10,
                                                                "velocity": 800,
                                                                "id": 123456})

