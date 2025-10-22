import utils
import collections

def move_zero_point():
    while (get_pos_x() != 0):
        move(West)

    while (get_pos_y() != 0):
        move(South)    

def move_center():
    move_zero_point()

    while (get_pos_x() < (get_world_size() / 2)):
        move(East)

    while (get_pos_y() < (get_world_size() / 2)):
        move(North)

def move_to_without_warp(x, y):
    now_pos = [get_pos_x(), get_pos_y()]
    target = [x, y]

    dir_x = East
    dir_y = North

    if (target[0] - now_pos[0]) < 0:
        dir_x = West

    if (target[1] - now_pos[1]) < 0:
        dir_y = South

    ret = True
    while target[0] != get_pos_x():
        if not move(dir_x):
            ret = False
            break

    while target[1] != get_pos_y():
        if not move(dir_y):
            ret = False
            break
    
    return ret


def move_to(x, y):
    now_pos = [get_pos_x(), get_pos_y()]
    target = [x, y]

    dir_x = East
    dir_y = North

    t_minus = [x - get_world_size(), y - get_world_size()]
    t_plus = [x + get_world_size(), y + get_world_size()]

    diff_x_list = [target[0] - now_pos[0] , t_minus[0] - now_pos[0], t_plus[0] - now_pos[0]]
    diff_y_list = [target[1] - now_pos[1] , t_minus[1] - now_pos[1], t_plus[1] - now_pos[1]]

    abs_dxl = []
    abs_dyl = []

    for i in diff_x_list:
        abs_dxl.append(abs(i))

    for i in diff_y_list:
        abs_dyl.append(abs(i))

    x_idx = collections.sorted_index(abs_dxl)
    y_idx = collections.sorted_index(abs_dyl)
    
    if diff_x_list[x_idx[0]] < 0:
        dir_x = West

    if diff_y_list[y_idx[0]] < 0:
        dir_y = South

    ret = True
    while target[0] != get_pos_x():
        if not move(dir_x):
            ret = False
            break

    while target[1] != get_pos_y():
        if not move(dir_y):
            ret = False
            break

    return ret