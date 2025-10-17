import collections
import moves
import utils

turn_dir = [North, West, East, South]
dir_name = ["N","W","E","S"]

dir2vec = {
    North:[0, 1],
    West:[-1, 0],
    South:[0, -1],
    East:[1, 0]
    }

turn_strategy = {
    North:[West, East, South], 
    West:[South, North, East],
    South:[East, West, North],
    East:[North, South, West]
    }
    
has_reached = []
move_stack = []
is_get_treasure = False

treasure_x = 0
treasure_y = 0

def get_next_pos(now_pos, dir):
    now_pos[0] = now_pos[0] + dir2vec[dir][0]
    now_pos[1] = now_pos[1] + dir2vec[dir][1]
    
    return now_pos

def maze_strategy_init():
    global is_get_treasure
    global has_reached
    global move_stack
    global treasure_x
    global treasure_y

    is_get_treasure = False
    has_reached = []
    move_stack = []
    
    treasure_x, treasure_y = measure()    
    
    # 到達フラグの初期化
    for pos_x in range(get_world_size()+2):
        tmp_list = [True]
        for pos_y in range(get_world_size()):
            if pos_x == 0 or pos_x == get_world_size()+1:
                tmp_list.append(True)
            else:
                tmp_list.append(False)
                
        tmp_list.append(True)
        has_reached.append(tmp_list)
        
def treasure_hunt():
    global is_get_treasure
    global has_reached
    global move_stack

    is_get_treasure = False
    
    # 分岐を探す
    while True:
        now_pos = [get_pos_x()+1, get_pos_y()+1]
        has_reached[now_pos[0]][now_pos[1]] = True
    
        if get_entity_type() == Entities.Treasure:
            is_get_treasure = True
            harvest()
            return
        
        dir_priority = []
        dir_diff = []
        
        for dir in turn_dir:
            next_pos = get_next_pos([now_pos[0], now_pos[1]], dir)
            
            diff = 0
            diff = abs(treasure_x - (next_pos[0] - 1))
            diff = diff + abs(treasure_y - (next_pos[1] - 1))
            
            dir_diff.append(diff)

        for dir_idx in collections.sorted_index(dir_diff):
            dir_priority.append(turn_dir[dir_idx])
        
        for dir in dir_priority:
            next_pos = get_next_pos([now_pos[0], now_pos[1]], dir)
            
            if get_entity_type() != Entities.Grass and not has_reached[next_pos[0]][next_pos[1]] and can_move(dir):
                    
                move_stack.append(dir)
                move(dir)
                    
                treasure_hunt()
                if is_get_treasure:
                    return
                
        # ここに来たらすべて行き止まり
        if (len(move_stack) == 0 or get_entity_type() == Entities.Grass):
            return
        else:
            move(utils.dir_opposite[move_stack.pop()])
            
def main_loop():
    treasure_hunt()
    
def spawn_drone_function():
    change_hat(Hats.Gray_Hat)
    
    while get_entity_type() != Entities.Hedge:
        do_a_flip()
    
    maze_strategy_init()            
    main_loop()

def init():
    clear()
    
    moves.move_to(0, 0)
        
    move(South)
    spawn_drone(spawn_drone_function)
    move(West)
    spawn_drone(spawn_drone_function)
    move(North)
    spawn_drone(spawn_drone_function)
    
    moves.move_to(0, 0)
        
    plant(Entities.Bush)    
    substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
    use_item(Items.Weird_Substance, substance)
            
if __name__ == "__main__":
    while True:
        init()
        change_hat(Hats.Traffic_Cone)    
        maze_strategy_init()
        main_loop()
    