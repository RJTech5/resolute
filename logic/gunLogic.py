import math
def find_vectors(cords1, cords2, speed, enemy):
    tot_distance = math.sqrt(((cords2[0] - cords1[0]) ** 2) + ((cords2[1] - cords1[1]) ** 2))
    print(tot_distance)
    t_target = tot_distance / speed
    print(t_target)
    cords2 = (cords2[0] + (enemy["x_velocity"] * t_target) + 17.5, cords2[1] + (enemy["y_velocity"] * t_target) + 17.5)
    print(cords2)

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

def fire_gun(cords, target_cords, damage, velo, size, game_state, enemy):
    xv, yv = find_vectors(cords, target_cords, velo, enemy)

    game_state["bullets"].append({"cords": cords, "damage": damage, "size": size, "x_velocity":xv, "y_velocity":yv})

    return game_state

def despawn_check(cord, game_state):
    if 753 < cord[0] or cord[0] < 0 or 735 < cord[1] or cord[1] < 0:
        return True, None

    for enemy in game_state["enemies"]:
        if enemy["cord"][0] < cord[0] < (enemy["cord"][0] + 35) and enemy["cord"][1] < cord[1] < (enemy["cord"][1] + 35):
            return True, enemy["id"]

    return False, None

