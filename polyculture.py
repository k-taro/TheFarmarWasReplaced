import utils
import moves
import farm_strategies
import operations

TARGET = Entities.Tree

PolyEntities = (Entities.Grass, Entities.Bush, Entities.Tree, Entities.Carrot)

def rand_plant(tpl_option):
    if len(tpl_option) == 0:
        return

    ent = utils.pick_random(tpl_option)
    farm_strategies.preparation(ent)


def poly_harvest(plant_option):

    if get_entity_type() != TARGET:
        farm_strategies.preparation(TARGET)

    if not can_harvest():
        return
    
    c_info = get_companion()

    if c_info != None:
        target_ent = c_info[0]
        target_pos = c_info[1]
        
        def f():
            moves.move_to(target_pos[0], target_pos[1])
            harvest()
            farm_strategies.preparation(target_ent, True)

        h = spawn_drone(f)

        if h != None:
            wait_for(h)

    harvest()
    rand_plant(plant_option)


def poly_farm(x, y, w, h, plant_option = PolyEntities, abort_condition = None):
    if abort_condition == None:
        def g():
            return False

        abort_condition = g

    while True:
        moves.move_to(x, y)
        for x_index in range(w):
            for y_index in range(h):
                poly_harvest(plant_option)
                if abort_condition():
                    return

                move(North)
            
            move(East)
            for y_index in range(h):
                move(South)


if __name__ == "__main__":
    drone_list = []

    def condition():
        return num_items(Items.Wood) >= 10000000000

    drone_num = ((max_drones())//2)
    for i in range(drone_num-1):
        def drone_operation():
            poly_farm(get_world_size() - (i+1) * (get_world_size() // drone_num), (i % 2) * get_world_size() // 2, get_world_size(), get_world_size(), (TARGET,), condition)

        h = spawn_drone(drone_operation)
        drone_list.append(h)

        for _ in range(get_world_size() * 1000 / drone_num):
            pass

    poly_farm(0, 0, get_world_size(), get_world_size(), (TARGET,), condition)

    for h in drone_list:
        wait_for(h)
