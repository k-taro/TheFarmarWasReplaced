# 恐竜の骨を収穫する

import moves
import vector


def main():
    move(North)

    for x_index in range(get_world_size()):
        for y_index in range(get_world_size() - 2):
            dir = North
            if get_pos_x() % 2 == 1:
                dir = South

            if not can_move(dir):
                return 0
            move(dir)

        if x_index < get_world_size() - 1:
            if not can_move(East):
                return 0
            move(East)

    if not can_move(South):
        return 0
    move(South)

    for x_index in range(get_world_size()-1):
        if not can_move(West):
            return 0
        move(West)
    
    return 1

def init():
    clear()
    change_hat(Hats.Brown_Hat)
    moves.move_to(0, 0)
    change_hat(Hats.Dinosaur_Hat)

if __name__ == "__main__":
    init()
    can_m = 1
    while can_m == 1:
        can_m = main()
