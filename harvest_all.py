import moves
def to_north():
    for pos_y in range(get_world_size()):
        harvest()
        move(North)


moves.move_zero_point()


for pos_x in range(get_world_size()):
    while num_drones() >= max_drones():
        pass

    spawn_drone(to_north)
    move(East)