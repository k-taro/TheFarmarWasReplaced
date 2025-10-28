import moves
import farm_strategies


def to_north():
    for pos_y in range(get_world_size()):
        harvest()
        move(North)

def cactus_sort():
    for i in range(get_world_size()):
        if get_pos_x() < get_world_size()-1:
            # 東から小さいサボテンを持ってくる
            cur = measure(None)
            next = measure(East)

            if cur != None and next != None and cur > next:
                swap(East)
            else:
                pass
                # for _ in range(200):
                #     pass

        # 北に大きいサボテンを運ぶ
        if get_pos_y() < get_world_size()-1:
            cur = measure(None)
            next = measure(North)

            if cur != None and next != None and cur > next:
                swap(North)
            else:
                for _ in range(200):
                    pass

        move(North)


def plant_cuctas():
    for _ in range(get_world_size()):
        farm_strategies.preparation(Entities.Cactus)
        move(North)


def main():
    drone_list = []

    moves.move_to(0,0)

    # サボテン植える
    for pos_x in range(get_world_size()):
        while num_drones() >= max_drones():
            pass

        drone = spawn_drone(plant_cuctas)

        move(East)

    plant_cuctas()

    drone_list = []
    moves.move_to(0,0)
    for d_cnt in range(get_world_size()):
        drone_list = []
        for pos_x in range(get_world_size()):
            cnt = 0
            while num_drones() >= max_drones() or cnt < 200:
                cnt += 1 # 1tick消費

            drone = spawn_drone(cactus_sort)
            drone_list.append(drone)

            move(East)

    for i in drone_list:
        wait_for(i)

    harvest()

if __name__ == "__main__":
    while True:
        main()
        if  num_items(Items.Cactus) >= 33554432:
            break
