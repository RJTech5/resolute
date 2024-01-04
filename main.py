import pygame
import math
import random
import time
from assets.pygameAssets import basic_gun, basic_enemy, basic_bullet
from logic.enemyLogic import move_enemy, find_vectors
from logic.gunLogic import fire_gun, despawn_check

background_colour = (0, 0, 0)
screen = pygame.display.set_mode((300, 300), pygame.RESIZABLE)
pygame.display.set_caption('Resolute')
cord_grid_offset = 35
cord_grid_size = 735
wave_increment = 360
wave_duration = 800

# game_state contains all information needed to run the game simulation
# game_state is a dict where
# - guns is a list of gun
# - enemies is a list of active enemies
# - bullets is a list of bullets currently in the game field
# - ticks is a count of the game loop
# - tot_ticks is the total number of ticks that I have gone by
# - wave_count is the number of waves that have occured
# - wave_sum is the sum of enemies in the current wave
# - wave_left is the number of enemies yet to spawn in a wave
# - next_wave is when the next wave will spawn in game ticks
# - running_score is the score of the game
game_state = {"guns": [],
              "enemies": [],
              "bullets": [],
              "objects": [],
              "ticks": 0,
              "tot_ticks": 0,
              "wave_count": 0,
              "wave_sum": 0,
              "wave_left": 0,
              "next_wave": 360,
              "running_score": 0,}

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

# bullet is a bullet on the game field
# bullet is a dict where
# - cord is the cord of bullet
# - damage is the damage a bullet inflicts
# - size is the size of bullet
# - x_velocity is the x vel of bullet
# - y_velocity is the y vel of bullet
bullet_example = {"cords": (), "damage": 10, "size": 3, "x_velocity":100, "y_velocity":100}


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

# Creates an ID for an entity
def get_id():
    id_proposed = random.randint(100000, 999999)
    for gun  in game_state["guns"]:
        if gun["id"] == id_proposed:
            return get_id()

    for enemy in game_state["enemies"]:
        if enemy["id"] == id_proposed:
            return get_id()

    return id_proposed

# Finds the nearest player gun to a given cord set
def find_gun(cords):
    leader = (None, (367, 367))

    for gun in game_state["guns"]:
        distance = math.sqrt(((gun["cord"][0] - cords[0]) ** 2) + ((gun["cord"][1] - cords[1]) ** 2))
        if leader[0] == None:
            leader = (distance, (gun["cord"][0], gun["cord"][1]))
        elif distance < leader[0]:
            leader = (distance, (gun["cord"][0], gun["cord"][1]))

    return leader[1]

# Finds nearest enemy from cords
def find_enemy(cords):
    leader = (None, (367, 367), None)

    for enemy in game_state["enemies"]:
        distance = math.sqrt(((enemy["cord"][0] - cords[0]) ** 2) + ((enemy["cord"][1] - cords[1]) ** 2))
        if leader[0] == None:
            leader = (distance, (enemy["cord"][0], enemy["cord"][1]), enemy)
        elif distance < leader[0]:
            leader = (distance, (enemy["cord"][0], enemy["cord"][1]), enemy)

    return leader[1], leader[2]

# Checks if the mouse if over an active gun

def remove_gun(cords):
    for gun in enumerate(game_state["guns"]):
        if gun[1]["cord"][0] <= cords[0] < (gun[1]["cord"][0] + 35) and gun[1]["cord"][1] <= cords[1] < (gun[1]["cord"][1] + 35):
            game_state["guns"].pop(gun[0])




running = True
item_placement = False

# game loop
while running:
    start = time.process_time()
    if game_state["ticks"] >= 24:
        game_state["ticks"] = 0

    # Creates the initial cord grid given grid size and offset
    for i in range(math.floor(cord_grid_size / cord_grid_offset)):
        pygame.draw.line(screen, (211, 211, 211), ((cord_grid_offset * i + cord_grid_offset), 0), ((cord_grid_offset * i + cord_grid_offset), cord_grid_size), 1)
        pygame.draw.line(screen, (211, 211, 211), (0, (cord_grid_offset * i)), (cord_grid_size, (cord_grid_offset * i)),
                         1)

    # Creates menu items selectable by player
    for item in menu_items:
        if item['type'] == "basic":
            basic_gun(pygame, screen, item["x"], item["y"])

    # Renders and fires guns
    for gun in game_state["guns"]:
        if gun["reload_timer"] <= 0:
            target_cords, enemy = find_enemy((gun["cord"][0] + 17.5, gun["cord"][1] + 17.5))
            if not enemy == None:
                fire_gun((gun["cord"][0] + 17.5, gun["cord"][1] + 17.5), target_cords, gun["damage"],gun["velocity"], 3, game_state, enemy)
                gun["reload_timer"] = gun["reload_time"]
        else:
            gun["reload_timer"] -= 1

        basic_gun(pygame, screen, gun["cord"][0], gun["cord"][1])

    # renders and moves bullets
    for bullet in enumerate(game_state["bullets"]):
        despawn_ck = despawn_check(bullet[1]["cords"], game_state)
        if despawn_ck[0]:
            game_state["bullets"].pop(bullet[0])
            if not despawn_ck[1] == None:
                damage = bullet[1]["damage"]

                for enemy in enumerate(game_state["enemies"]):
                    if despawn_ck[1] == enemy[1]["id"]:
                        enemy[1]["health"] -= damage
                        if enemy[1]["health"] <= 0:
                            game_state["enemies"].pop(enemy[0])
            pass

        x = bullet[1]["cords"][0] + bullet[1]["x_velocity"]
        y = bullet[1]["cords"][1] + bullet[1]["y_velocity"]

        bullet[1]["cords"] = (x, y)
        basic_bullet(pygame, screen, x, y, bullet[1]["size"])



    # Renders and moves enemies
    for enemy in game_state["enemies"]:
        enemy["target_cord"] = find_gun(enemy["cord"])
        move_enemy(enemy, game_state)
        basic_enemy(pygame, screen, enemy["cord"][0], enemy["cord"][1])

    # creates an enemy and adds it to the gamestate
    if game_state["tot_ticks"] >= game_state["next_wave"]:
        spawn_tot = random.randint(10, 50) * (game_state["wave_count"] + 1)
        game_state["wave_left"] = spawn_tot
        game_state["wave_sum"] = spawn_tot
        game_state["next_wave"] = game_state["tot_ticks"] + wave_duration

    # finds the number of enemies to spawn within 1 second
    if game_state["wave_left"] > 0 and game_state["ticks"] == 0:
        number_spawn = random.randint(0,25)
        if number_spawn >= game_state["wave_left"]:
            number_spawn = game_state["wave_left"]

        game_state["wave_left"] -= number_spawn

        if game_state["wave_left"] <= 0:
            game_state["wave_left"] = 0
            game_state["wave_count"] += 1

        for i in range(number_spawn):
            # wall picks the wall the enemy will spawn against
            wall = random.randint(1,4)
            random_pos = random.randint(0,735)

            if wall == 1:
                cords = (random_pos, 0)
            elif wall == 2:
                cords = (735, random_pos)
            elif wall == 3:
                cords = (random_pos, 735)
            else:
                cords = (0, random_pos)

            target_cords = find_gun(cords)
            x_vector, y_vector = find_vectors(cords, target_cords)

            id = get_id()

            enemy_add = {"cord": cords, "health": 100, "target_cord": target_cords, "x_velocity": x_vector, "y_velocity": y_vector,
                             "id": id}

            game_state["enemies"].append(enemy_add)

    pygame.display.flip()
    screen.fill(background_colour)
    # for loop through the event queue
    for event in pygame.event.get():

        # Check for QUIT event
        if event.type == pygame.QUIT:
            print(game_state)
            running = False
        

        # checks if the mouse is being pressed
        if pygame.mouse.get_pressed()[0]:
            if item_placement == False:
                item_check_res, item_type = check_menu(pygame.mouse.get_pos())
                if item_check_res:
                    item_placement = True
                else:
                    remove_gun(pygame.mouse.get_pos())
            elif validate_placement():
                item_placement = False
                x = math.floor(pygame.mouse.get_pos()[0] / 35) * 35
                y = math.floor(pygame.mouse.get_pos()[1] / 35) * 35
                id = get_id()
                game_state["guns"].append({"cord": (x, y),
                                                                "health": 100,
                                                                "reload_timer": 2,
                                                                "reload_time": 5,
                                                                "damage": 25,
                                                                "velocity": 10,
                                                                "id": id})

    end = time.process_time()
    delta = end - start
    if delta < 0.0417:
        time.sleep(0.0417 - delta)
    game_state["ticks"] += 1
    game_state["tot_ticks"] += 1
