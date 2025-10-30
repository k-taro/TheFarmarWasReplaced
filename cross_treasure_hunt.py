import moves

SIZE = 7
TRY_CNT = 300
SUBSTANCE = SIZE * 2**(num_unlocked(Unlocks.Mazes) - 1)

def relocate():
    harvest()
    plant(Entities.Bush)
    use_item(Items.Weird_Substance, SUBSTANCE)

def hunting():
    is_started = False
    base_p = (get_pos_x(), get_pos_y())

    while True:
        cur_p = measure()
        if cur_p == None:
            is_started = True
            continue

        # elif not is_started:
        #     continue

        if cur_p == base_p:
            harvest()

        elif cur_p == (base_p[0] + 1, base_p[1]) and can_move(East):
            spawn_drone(hunting)
            move(East)
            harvest()
            return

        elif cur_p == (base_p[0], base_p[1] + 1) and can_move(North):
            spawn_drone(hunting)
            move(North)
            harvest()
            return

        elif cur_p == (base_p[0] - 1 , base_p[1]) and can_move(West):
            spawn_drone(hunting)
            move(West)
            harvest()
            return

        elif cur_p == (base_p[0] , base_p[1] - 1) and can_move(South):
            spawn_drone(hunting)
            move(South)
            harvest()
            return

def harvest_if_can():
    while True:
        if can_harvest():
            harvest()


def single():
    for i in range(SIZE):
        for j in range(SIZE):
            drone = spawn_drone(harvest_if_can)
            move(East)

        for j in range(SIZE):
            move(West)

        move(North)

def main():
    drone_list = []
    for i in range(SIZE):
        for j in range(SIZE):
            if (i + j) % 2 == 0:
                drone = spawn_drone(hunting)
                drone_list.append(drone)

            move(East)

        for j in range(SIZE):
            move(West)

        move(North)


if __name__ == "__main__":
    #while True:
    change_hat(Hats.Top_Hat)
    if SIZE < 6:
        single()
    else:
        main()

    moves.move_to(0, 0)
    relocate()

    try_cnt = 0

    while num_items(Items.Gold) < 9863168:
        for _ in range(100):
            pass
        relocate()
        quick_print(num_items(Items.Gold))
