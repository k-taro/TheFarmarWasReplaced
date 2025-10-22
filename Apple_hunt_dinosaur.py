# 恐竜の骨を収穫する

import moves
import vector

tail_count = 0

def zigzag_move(pos_apple):
    global tail_count
    ret = vector.create_vector(pos_apple[0], pos_apple[1])

    while get_pos_x() < get_world_size()-1:
        dir = North
        y_diff = get_world_size() - 1 - get_pos_y()
        if get_pos_x() % 2 == 1:
            dir = South
            y_diff = get_pos_y() - 1
        
        while y_diff >= 0:
            if not can_move(dir):
                return vector.create_vector(-1, -1)
            move(dir)
            if(get_entity_type() == Entities.Apple):
                ret[0], ret[1] = measure()
                tail_count += 1
                
            y_diff = get_world_size() - 1 - get_pos_y()
            if dir == South:
                y_diff = get_pos_y() - 1

        if get_pos_x() < get_world_size()-1:
            if not can_move(East):
                return vector.create_vector(-1, -1)
            move(East)
            if(get_entity_type() == Entities.Apple):
                ret[0], ret[1] = measure()
                tail_count += 1

    return ret

def move_to_without_warp(x, y, pos_apple, stop_if_apple = False):
    global tail_count
    now_pos = [get_pos_x(), get_pos_y()]
    target = [x, y]
    ret = vector.create_vector(pos_apple[0], pos_apple[1])

    dir_x = East
    dir_y = North

    if (target[0] - now_pos[0]) < 0:
        dir_x = West

    if (target[1] - now_pos[1]) < 0:
        dir_y = South

    while target[0] != get_pos_x():
        if not move(dir_x):
            ret = vector.create_vector(-1, -1)
            break
        if get_entity_type() == Entities.Apple:
            ret[0], ret[1] = measure()
            tail_count += 1
            if stop_if_apple:
                return ret

    while target[1] != get_pos_y():
        if not move(dir_y):
            ret = vector.create_vector(-1, -1)
            break
        if get_entity_type() == Entities.Apple:
            ret[0], ret[1] = measure()
            tail_count += 1
            if stop_if_apple:
                return ret
    
    return ret

def go_to_apple(pos_apple):
    global tail_count
    zigzag_lane = tail_count // (get_world_size() - 1) + 1

    zigzag_start_pos = vector.create_vector(
            get_world_size() - zigzag_lane,
            get_world_size() - 1
        )
    
    if zigzag_start_pos[0] % 2 == 0:
        zigzag_start_pos[1] = 1

    if (zigzag_start_pos[0]-1) >= get_pos_x():
        pos_apple = move_to_without_warp(zigzag_start_pos[0]-1, zigzag_start_pos[1], pos_apple)
        if pos_apple[0] < 0:
            return None    
        if not move(East):
            return None
        
        if get_entity_type() == Entities.Apple:
            pos_apple[0], pos_apple[1] = measure()

    pos_apple = zigzag_move(pos_apple)
    if pos_apple[0] < 0:
        return None
    
    move(South)
    if get_entity_type() == Entities.Apple:
        pos_apple[0], pos_apple[1] = measure()

    for _ in range(get_pos_x()-pos_apple[0]):
        if not move(West):
            return None
    
        if get_entity_type() == Entities.Apple:
            pos_apple[0], pos_apple[1] = measure()

    zigzag_lane = tail_count // (get_world_size() - 1) + 1
    zigzag_start_pos = vector.create_vector(
            get_world_size() - zigzag_lane,
            get_world_size() - 1
        )
    
    if get_pos_x() >= zigzag_start_pos[0]-1:
        for _ in range(get_pos_x()-zigzag_start_pos[0]+2):
            if not move(West):
                return None
            
        if not move(North):
            return None
        if get_entity_type() == Entities.Apple:
            pos_apple[0], pos_apple[1] = measure()
            tail_count += 1

        pos_apple = zigzag_move(pos_apple)

    else:
        pos_apple = move_to_without_warp(pos_apple[0], pos_apple[1], pos_apple, True)
        zigzag_lane = tail_count // (get_world_size() - 1) + 1

        while (get_pos_x() < pos_apple[0]) and (pos_apple[0] < (get_world_size() - zigzag_lane - 3)):
            pos_apple = move_to_without_warp(pos_apple[0], pos_apple[1], pos_apple, True)
            zigzag_lane = tail_count // (get_world_size() - 1) + 1

    return pos_apple


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
    target_x, target_y = measure()
    target = vector.create_vector(target_x, target_y)
    tail_count = 0

#    while True:
#        main()

    while target != None:
        target = go_to_apple(target)

    print(tail_count)
    #change_hat(Hats.Brown_Hat)
