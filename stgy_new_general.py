import farm_strategies
from farm_strategies import harvest_cactus, harvest_if_can, harvest_pumpkin, KEY_POS
import operations
from operations import preparation
import polyculture
import utils
import moves
from utils import nop

AREA_CONF = [
    {Entities:Entities.Pumpkin, KEY_POS:[0,0,6,6]},
    {Entities:Entities.Pumpkin, KEY_POS:[12,0,6,6]},
    {Entities:Entities.Pumpkin, KEY_POS:[6,6,6,6]},
    {Entities:Entities.Pumpkin, KEY_POS:[18,6,6,6]},
    {Entities:Entities.Pumpkin, KEY_POS:[0,12,6,6]},
    {Entities:Entities.Pumpkin, KEY_POS:[12,12,6,6]},
    {Entities:Entities.Cactus, KEY_POS:[0,18,14,14]},
#    {Entities:Entities.Carrot, KEY_POS:[0,18,24,7]},
#    {Entities:Entities.Tree, KEY_POS:[0,25,24,7]},
#    {Entities:Entities.Grass, KEY_POS:[24,0,8,30]},
#    {Entities:Entities.Sunflower, KEY_POS:[24,30,8,2]},
]

AREA_FLOWER = [24,30,8,2]

AREA_POLY = [
    [6,0,6,6],
    [18,0,6,6],
    [0,6,6,6],
    [12,6,6,6],
    [6,12,6,6],
    [18,12,6,6],
    [14, 18, 10, 7],
    [14, 25, 10, 7],
    [24, 0, 8, 10],
    [24, 10, 8, 10],
    [24, 20, 8, 10],
]

def wrap_preparation(context):

    preparation(context[Entities])

    return context

def wrap_main_loop():
    main_loop(nop)

def main_loop(g):
    cactus_ctxt = {
            KEY_POS:[0, 0, 0, 0], 
            farm_strategies.KEY_COUNT_CAN_HARVEST:True,
            farm_strategies.KEY_IS_NO_SORT:True,
        }

#    while True:
    for conf in AREA_CONF:
        ent = conf[Entities]
        x,y,w,h = conf[KEY_POS]

        moves.move_to(x,y)

        if ent == Entities.Pumpkin:
            operations.do_in_area(harvest_pumpkin, w, h, {KEY_POS:conf[KEY_POS], farm_strategies.KEY_COUNT_CAN_HARVEST:0})
        
        elif ent == Entities.Cactus:
            cactus_ctxt[KEY_POS] = conf[KEY_POS]
            operations.do_in_area(harvest_cactus, w, h, cactus_ctxt, operations.ORDER_COLUMN_MAJOR)

        # elif ent == Entities.Sunflower:
        #     pos = conf[KEY_POS]
        #     moves.move_to(pos[0], pos[1])
        #     farm_strategies.harvest_sunflower_mod({KEY_POS:pos})
        #     operations.do_in_area(farm_strategies.harvest_sunflower_mod, w, h, {KEY_POS:conf[KEY_POS]})

        else:
            operations.do_in_area(harvest_if_can, w, h, {Entities:ent})

    g()

            
if __name__ == "__main__":
    # spawn_drone(wrap_main_loop)

    # for i in range(3):
    #     do_a_flip()

    # main_loop(nop)

    # while True:
    #     farm_strategies.harvest_sunflower_mod({farm_strategies.KEY_POS:[11, 0, 1, 12]})
    #     spawn_drone(wrap_main_loop)

    def harv_flower():
        while True:
            moves.move_to(AREA_FLOWER[0], AREA_FLOWER[1])
            operations.do_in_area(
                farm_strategies.wait_and_harvest,
                AREA_FLOWER[2], 
                AREA_FLOWER[3], 
                {Entities:Entities.Sunflower}
            )
    moves.move_to(AREA_FLOWER[0], AREA_FLOWER[1])
    spawn_drone(harv_flower)

    diff_tick = 60000

    for area in AREA_POLY:
        def harv_poly():
            while True:
                polyculture.single_polyculture(area[0], area[1], area[2], area[3])

        moves.move_to(area[0], area[1])
        spawn_drone(harv_poly)

    moves.move_zero_point()

    base_drone_nums = num_drones()

    while True:
        first_drone_handler = spawn_drone(wrap_main_loop)
        first_drone_tick = get_tick_count()
        start_tick = first_drone_tick

        for _ in range(max_drones() - base_drone_nums):
            while (get_tick_count() - start_tick) < (diff_tick / (max_drones()-base_drone_nums)):
                pass

            spawn_drone(wrap_main_loop)
            start_tick = get_tick_count()

        wait_for(first_drone_handler)

        diff_tick = get_tick_count() - first_drone_tick

