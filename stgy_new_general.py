import operations
import utils
import item_conf
import moves

AREA_CONF = [
    {Entities:Entities.Pumpkin, "pos":[0,0,3,3]},
    {Entities:Entities.Carrot, "pos":[3,0,5,3]},
    {Entities:Entities.Sunflower, "pos":[7,7,1,1]},
    {Entities:Entities.Cactus, "pos":[0,3,3,3]},
    {Entities:Entities.Tree, "pos":[3,3,5,3]},
]

def flower_shop():
    while True:
        if can_harvest():
            harvest()
        elif get_entity_type() != Entities.Sunflower:
            plant(Entities.Sunflower)
            
        operations.use_water_if_dry()
        
        for i in range(3):
            do_a_flip()

def preparation(context):
    
    if item_conf.is_need_till(context[Entities]) and get_ground_type() != Grounds.Soil:
        till()
        
    if context[Entities] == Entities.Tree:
        if (get_pos_x() % 2) == (get_pos_y() % 2):
            plant(Entities.Tree)
            use_item(Items.Fertilizer)
        else:
            plant(Entities.Bush)
            
    if context[Entities] != Entities.Grass:
        plant(context[Entities])

    return context

def init():
    clear()
    
    for conf in AREA_CONF:
        x,y,w,h = conf["pos"]
        moves.move_to(x, y)
        operations.do_in_area(preparation, w, h, {Entities:conf[Entities]})

        
def main_loop():
    while True:
        is_all_pumpkin = True
        for pos_x in range(get_world_size()):
            for pos_y in range(get_world_size()):
                    
                move(North)            
                            
            move(East)
        
            
if __name__ == "__main__":
    init()
    main_loop()
