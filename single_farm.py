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

def sinc_plant():
    if not plant(Entities.Sunflower):
        for _ in range(200):
            pass
    if get_water() < 0.4:
        if not use_item(Items.Water):
            for _ in range(200):
                pass
    else:
        for _ in range(201):
            pass

def go_north_flower():
    for _ in range(get_world_size()):
        if get_ground_type() == Grounds.Grassland:
            till()

        sinc_plant()
        move(North)


    while num_items(Items.Power) < 100000:
        for _ in range(get_world_size()):
            if not continue_sunflower():
                break


            move(North)

        for m in (14, 12):
            for _ in range(get_world_size()):
                if not continue_sunflower():
                    break
                tmp_m = measure()
                if tmp_m != None and tmp_m >= m:
                    if not harvest():
                        for _ in range(200):
                            pass
                else:
                    for _ in range(200):
                        pass

                move(North)
    
        for _ in range(get_world_size()):
            if not continue_sunflower():
                break

            if not harvest():
                for _ in range(200):
                    pass

            sinc_plant()
            move(North)

def go_north_maximum_flower():
    while True:
        for _ in range(get_world_size()):
            for _ in range(get_world_size()):
                if not continue_sunflower:
                    return

                if can_harvest():
                    harvest()
                
                if get_ground_type() == Grounds.Grassland:
                    till()

                plant(Entities.Sunflower)
                cnt = 0
                while measure() < 15 or cnt < 2:
                    cnt += 1
                    harvest()
                    plant(Entities.Sunflower)

                if get_water() < 0.5:
                    use_item(Items.Water)
                
                move(North)
            move(East)

        move(West)
        move(West)


def go_north():
    while True:
        farm_strategies.harvest_if_can({Entities:FARM_ITEM})
        move(North)

def drone_method():
    moves.move_to(0,0)
    operations.do_in_area(farm_strategies.harvest_if_can, get_world_size(), get_world_size(), {Entities:FARM_ITEM})

def continue_sunflower():
    return num_items(Items.Power) < 100000

def ret_true():
    return True

def launch_subdrones(limit):
    diff_tick = 100000
    base_drone_nums = num_drones()
    while limit():
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


def main_loop():
    moves.move_zero_point()

    f = go_north

    if max_drones() >= get_world_size():
        if FARM_ITEM == Entities.Sunflower:
            f = go_north_maximum_flower

            for i in range(get_world_size()//2):
                spawn_drone(f)
                move(East)
                move(East)

            launch_subdrones(continue_sunflower)
        else:
            for i in range(get_world_size()-1):
                spawn_drone(f)
                move(East)

            f()
    else:
        launch_subdrones(ret_true)
        
if __name__ == "__main__":
#    init()
    main_loop()
