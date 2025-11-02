import moves
import operations
import item_conf
import farm_strategies

FARM_ITEM = Entities.Pumpkin

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

def main_loop(condition, start_x, start_y, w):
    pumpkin_id_list = {}
    pumpkin_size = min(6, w)

    for x in range(w):
        for y in range(-pumpkin_size+1, w, 1):
            pumpkin_id_list[x,y] = 0

    while True:
        moves.move_to(start_x, start_y)
        for pos_x in range(w):
            for pos_y in range(w):
                if condition():
                    return
                
                if get_entity_type() != FARM_ITEM:
                    farm_strategies.preparation(FARM_ITEM)
                    operations.use_water_if_dry()
                    pumpkin_id_list[pos_x, pos_y] = 0
                else:
                    id = 0
                    if can_harvest():
                        id = measure()
                    pumpkin_id_list[pos_x, pos_y] = id

                    if id == pumpkin_id_list[pos_x, pos_y-pumpkin_size+1]:
                        harvest()
                    
                move(North)
            
            moves.move_to(start_x+pos_x, start_y)
            move(East)
        
if __name__ == "__main__":
    def single_condition():
        return num_items(Items.Pumpkin) >= 10000000

    main_loop(single_condition, 0, 0, 6)
    