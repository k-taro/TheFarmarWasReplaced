import farm_strategies
from farm_strategies import harvest_cactus, harvest_if_can, harvest_pumpkin, preparation
import operations
import utils
import moves
from utils import nop

AREA_CONF = [
    {Entities:Entities.Pumpkin, KEY_POS:[0,0,5,5]},
    {Entities:Entities.Carrot, KEY_POS:[5,0,6,5]},
    {Entities:Entities.Cactus, KEY_POS:[0,5,5,5]},
    {Entities:Entities.Tree, KEY_POS:[5,5,6,5]},
    {Entities:Entities.Grass, KEY_POS:[0,10,11,2]},
    {Entities:Entities.Sunflower, KEY_POS:[11,11,1,-12]},
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

        elif ent == Entities.Sunflower:
            operations.do_in_area(farm_strategies.harvest_sunflower, w, h, {KEY_POS:conf[KEY_POS]})

        else:
            operations.do_in_area(harvest_if_can, w, h, {Entities:ent})

    g()

            
if __name__ == "__main__":
    # spawn_drone(wrap_main_loop)

    # for i in range(3):
    #     do_a_flip()

    # main_loop(nop)

    drone_handler = spawn_drone(wrap_main_loop)
    start_tick = get_tick_count()
    wait_for(drone_handler)
    end_tick = get_tick_count()

    diff_tick = end_tick - start_tick

    while True:
        first_drone_handler = spawn_drone(wrap_main_loop)
        first_drone_tick = get_tick_count()
        start_tick = first_drone_tick

        for _ in range(max_drones() - 2):
            while (get_tick_count() - start_tick) < (diff_tick / (max_drones()-1)):
                pass

            spawn_drone(wrap_main_loop)
            start_tick = get_tick_count()

        wait_for(first_drone_handler)

        diff_tick = get_tick_count() - first_drone_tick

