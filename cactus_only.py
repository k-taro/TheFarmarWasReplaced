import moves
import operations

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
                operations.preparation(Entities.Cactus)
                tmp_sorted = i
            else:
                cur = measure(None)
                next = measure(dir)
                if cur != None and next != None and measure(None) > measure(dir):
                    swap(dir)
                    tmp_sorted = i

            move(dir)

        sorted_index = tmp_sorted
            

def main(x, y, w):
    drone_list = []
    n_drone = min(max_drones(), w)
    div = w // n_drone

    moves.move_to(x,y)

    def cn():
        for _ in range(div):
            cactus_sort(North)
            move(East)

    def ce():
        for _ in range(div):
            cactus_sort(East)
            move(North)
        
    for pos_x in range(0, w-div, div):
        while num_drones() >= max_drones():
            pass

        drone = spawn_drone(cn)
        drone_list.append(drone)

        for _ in range(div):
            move(East)

    for _ in range(div):
        cactus_sort(North)
        move(East)

    for i in drone_list:
        wait_for(i)

    drone_list = []
    moves.move_to(0,w-1)

    for pos_y in range(0, w-div, div):
        while num_drones() >= max_drones():
            pass

        drone = spawn_drone(ce)
        drone_list.append(drone)

        for _ in range(div):
            move(South)

    for _ in range(div):
        cactus_sort(East)
        move(North)

    for i in drone_list:
        wait_for(i)

    harvest()

if __name__ == "__main__":
    while True:
        main(0, 0, get_world_size())
        if  num_items(Items.Cactus) >= 33554432:
            break
