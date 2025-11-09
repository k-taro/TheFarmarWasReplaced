import moves
import operations
import direction

def swap_swap(start_timing, size, dir):
    move_dir = East
    if dir == East:
        move_dir = North
    
    while get_time() < start_timing:
        pass

    for pos in range(size):
        for swap_cnt in range(size-1):
            if measure(None) > measure(dir):
                swap(dir)
            else:
                for _ in range(200):
                    pass

            for _ in range(0):
                pass

        move(move_dir)

def plant_cuctas():
    for _ in range(get_world_size()):
        operations.preparation(Entities.Cactus)
        move(North)


def main():

    moves.move_to(0,0)

    # サボテン植える
    for pos_x in range(get_world_size()-1):
        while num_drones() >= max_drones():
            pass

        drone = spawn_drone(plant_cuctas)

        move(East)

    plant_cuctas()
    moves.move_to(0,0)
    
    for dir in ((North, North), (East, East)):
        drone_list = []
        start_time = get_time() + 2
    
        for i in range(get_world_size()-1):
            def wrap():
                swap_swap(start_time, get_world_size(), dir[0])

            d = spawn_drone(wrap)
            drone_list.append(d)

            move(dir[1])
        
        moves.move_to(0,0)
        for i in drone_list:
            wait_for(i)

    harvest()

    return

if __name__ == "__main__":
    while True:
        main()
        if  num_items(Items.Cactus) >= 33554432:
            break
