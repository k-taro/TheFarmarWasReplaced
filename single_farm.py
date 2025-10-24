import operations
import moves
import item_conf
import farm_strategies

FARM_ITEM = Entities.Sunflower

def init():
    clear()
    
    moves.move_zero_point()
    
    is_need_till = item_conf.is_need_till(FARM_ITEM)
    
    for pos_x in range(get_world_size()):
        for pos_y in range(get_world_size()):
            if is_need_till:
                till()
            
            move(North)
    
        move(East)

def go_north():
    while True:
        farm_strategies.harvest_if_can({Entities:FARM_ITEM})
        move(North)

def drone_method():
    moves.move_to(0,0)
    operations.do_in_area(farm_strategies.harvest_if_can, get_world_size(), get_world_size(), {Entities:FARM_ITEM})

def main_loop():
    diff_tick = 60000
    base_drone_nums = num_drones()
    moves.move_zero_point()

    if max_drones() >= get_world_size():
        for i in range(get_world_size()-1):
            spawn_drone(go_north)
            move(East)

        go_north()
    else:
        while True:
            first_drone_handler = spawn_drone(drone_method)
            first_drone_tick = get_tick_count()
            start_tick = first_drone_tick

            for _ in range(max_drones() - base_drone_nums):
                while (get_tick_count() - start_tick) < (diff_tick / (max_drones()-base_drone_nums)):
                    pass

                spawn_drone(drone_method)
                start_tick = get_tick_count()

            wait_for(first_drone_handler)

            diff_tick = get_tick_count() - first_drone_tick
        
if __name__ == "__main__":
#    init()
    main_loop()
