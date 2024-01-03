import math


def find_vectors(cords1, cords2):
    speed = 2
    x_distance = abs(cords2[0] - cords1[0])
    y_distance = abs(cords2[1] - cords1[1])
    try:
        angle = math.degrees(math.atan(x_distance/y_distance))
    except:
        angle = 0
    angle_a = math.radians(180 - (90 + angle))
    x_velocity = math.cos(angle_a) * speed
    y_velocity = math.sin(angle_a) * speed

    if (cords2[0] - cords1[0]) < 0:
        x_velocity = x_velocity * -1

    if (cords2[1] - cords1[1]) < 0:
        y_velocity = y_velocity * -1

    return x_velocity, y_velocity

# Moves an enemy entity
def move_enemy(enemy, game_state):
    xv, yv = find_vectors(enemy["cord"], enemy["target_cord"])
    x = enemy["cord"][0]
    y = enemy["cord"][1]
    x += xv
    y += yv
    enemy["cord"] = (x, y)


    return game_state