import moves
import farm_strategies

def to_north():
    for pos_y in range(get_world_size()):
        harvest()
        move(North)

def cactus_sort(dir):
    start_pos = (get_pos_x(), get_pos_y())
    sorted_index = get_world_size()

    while sorted_index > 0:
        tmp_sorted = 0

        moves.move_to(start_pos[0], start_pos[1])

        for i in range(sorted_index):
            if get_entity_type() != Entities.Cactus:
                farm_strategies.preparation(Entities.Cactus)
                tmp_sorted = i
            else:
                cur = measure(None)
                next = measure(dir)
                if cur != None and next != None and measure(None) > measure(dir):
                    swap(dir)
                    tmp_sorted = i

            move(dir)

        sorted_index = tmp_sorted
            

def main():
    drone_list = []

    moves.move_to(0,0)

    def cn():
        cactus_sort(North)

    def ce():
        cactus_sort(East)
        
    for pos_x in range(get_world_size()-1):
        while num_drones() >= max_drones():
            pass

        drone = spawn_drone(cn)
        drone_list.append(drone)

        move(East)

    cactus_sort(North)

    for i in drone_list:
        wait_for(i)

    moves.move_to(0,0)

    for pos_y in range(get_world_size()-1):
        while num_drones() >= max_drones():
            pass

        drone = spawn_drone(ce)
        drone_list.append(drone)

        move(North)

    cactus_sort(East)

    for i in drone_list:
        wait_for(i)

    harvest()

if __name__ == "__main__":
    while True:
        main()
