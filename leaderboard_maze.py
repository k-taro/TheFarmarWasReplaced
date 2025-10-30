import treasure_over_hunt
import moves

GOLD_LIMIT = 9863168

def hunting(pos, size, wait_cnt):
    moves.move_to(pos[0], pos[1])
    max_try_cnt = 299
    if size == 6:
        max_try_cnt = 280

    for i in range(wait_cnt):
        pass

    while num_items(Items.Gold) < GOLD_LIMIT:
        treasure_over_hunt.init(pos[0], pos[1], size)
        treasure_over_hunt.treasure_hunt(pos[0], pos[1], size, size, False, GOLD_LIMIT, max_try_cnt)
        if size == 6:
            if num_items(Items.Gold) < GOLD_LIMIT * 0.7:
                max_try_cnt = 20
                size = 5
            else:
                break
        else:
            if num_items(Items.Gold) < GOLD_LIMIT * 0.2:
                max_try_cnt = 80
            elif num_items(Items.Gold) < GOLD_LIMIT * 0.4:
                max_try_cnt = 40
            elif num_items(Items.Gold) < GOLD_LIMIT * 0.8:
                max_try_cnt = 20
            else:
                max_try_cnt = 5


if __name__ == "__main__":
    clear()
    drone = []

    single_tick = 500
    max_tick = 6*6*single_tick

    size = 6
    base_x, base_y = 32-size, 0
    for i in range(4):
        pos = (base_x, base_y + i * size)

        def wrap():
            hunting(pos, size, max_tick - single_tick * len(drone))

        d = spawn_drone(wrap)
        if d != None:
            drone.append(d)

    size = 6
    base_x, base_y = 0, 32-2*size
    for i in range(4):
        for j in range(2):
            pos = (base_x + i * size, base_y + j * size)

            def wrap():
                hunting(pos, size, max_tick - single_tick * len(drone))

            d = spawn_drone(wrap)
            if d != None:
                drone.append(d)

    size = 5
    base_x, base_y = 0, 0
    for i in range(5):
        for j in range(4):
            if i == 0 and j == 0:
                continue

            pos = (base_x + i * size, base_y + j * size)

            def wrap():
                hunting(pos, size, max_tick - single_tick * len(drone))

            d = spawn_drone(wrap)
            if d != None:
                drone.append(d)

#    change_hat(Hats.Traffic_Cone)
    pos = (0, 0)
    moves.move_to(pos[0], pos[1])

    while num_items(Items.Gold) < GOLD_LIMIT:
        treasure_over_hunt.init(pos[0], pos[1], size)
        treasure_over_hunt.treasure_hunt(pos[0], pos[1], size, size, False, GOLD_LIMIT)
