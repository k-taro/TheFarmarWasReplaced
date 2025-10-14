import operations
import utils
import item_conf
import moves

AREA_CONF = [
    {Entities:Entities.Pumpkin, "pos":[0,0,3,3]},
    {Entities:Entities.Carrot, "pos":[3,0,5,3]},
    {Entities:Entities.Cactus, "pos":[0,3,3,3]},
    {Entities:Entities.Tree, "pos":[3,3,5,3]},
    {Entities:Entities.Grass, "pos":[0,6,7,2]},
    {Entities:Entities.Sunflower, "pos":[7,7,1,1]},
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

def wrap_preparation(context):

    preparation(context[Entities])

    return context

def preparation(ent):
    
    if (item_conf.is_need_till(ent)) == (get_ground_type() == Grounds.Grassland):
        till()
        
    if ent == Entities.Tree:
        if (get_pos_x() % 2) == (get_pos_y() % 2):
            plant(Entities.Tree)
            use_item(Items.Fertilizer)
        else:
            plant(Entities.Bush)

    elif ent != Entities.Grass:
        plant(ent)

def sort_cactus(w, h):
    while True:
        is_sorted = True

        for x_idx in range(w):
            for y_idx in range(h):
                cur_size = measure(None)
                south_size = measure(South)
                west_size = measure(West)

                if y_idx != 0:
                    if cur_size < south_size:
                        is_sorted = False
                        swap(South)
                        south_size = cur_size
                        cur_size = measure(None)

                if x_idx != 0:
                    if cur_size < west_size:
                        is_sorted = False
                        swap(West)

                move(North)

            move(East)
            for y_idx in range(h):
                move(South)

        for x_idx in range(w):
            move(West)

        if is_sorted:
            break

def harvest_cactus(context):
    x, y, w, h = context["pos"]

    if get_entity_type() != Entities.Cactus:
        preparation(Entities.Cactus)

    if not can_harvest():
        context["is_all_cactus"] = False

    elif (get_pos_x() == x + w - 1) and (get_pos_y() == y + h - 1):
        if context["is_all_cactus"]:
            moves.move_to(x,y)
            sort_cactus(w, h)
            harvest()

    if item_conf.is_need_water(Entities.Cactus):
        operations.use_water_if_dry()

    return context
   

def harvest_pumpkin(context):
    x, y, w, h = context["pos"]

    if get_entity_type() != Entities.Pumpkin:
        preparation(Entities.Pumpkin)

    if not can_harvest():
        context["is_all_pumpkin"] = False

    elif (get_pos_x() == x + w - 1) and (get_pos_y() == y + h - 1):
        if context["is_all_pumpkin"]:
            harvest()

    if item_conf.is_need_water(Entities.Pumpkin):
        operations.use_water_if_dry()

    return context

def harvest_if_can(context):
    ent = context[Entities]

    if can_harvest():
        harvest()

    if get_entity_type() != ent:
        preparation(ent)

    if item_conf.is_need_water(ent):
        operations.use_water_if_dry()

    return context

def nop():
    return None

def wrap_main_loop():
    main_loop(do_a_flip)

def main_loop(g):
    while True:
        for conf in AREA_CONF:
            ent = conf[Entities]
            x,y,w,h = conf["pos"]

            moves.move_to(x,y)

            if ent == Entities.Pumpkin:
                operations.do_in_area(harvest_pumpkin, w, h, {"pos":conf["pos"], "is_all_pumpkin":True})
            
            elif ent == Entities.Cactus:
                operations.do_in_area(harvest_cactus, w, h, {"pos":conf["pos"], "is_all_cactus":True})

            else:
                operations.do_in_area(harvest_if_can, w, h, {Entities:ent})

        g()

            
if __name__ == "__main__":
#    spawn_drone(wrap_main_loop)

    for i in range(3):
        do_a_flip()

    main_loop(nop)
