import collections
import moves
import utils
import direction
import vector

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
    return vector.create_vector(now_pos[0] + dir2vec[dir][0], now_pos[1] + dir2vec[dir][1])

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

def get_trace(dist_list, edge_list, start_pos, is_opp = False):
    trace = []
    now_pos = start_pos

    while dist_list[now_pos[0]][now_pos[1]] > 0:
        for dir in direction.Directions:
            next_pos = get_next_pos(now_pos, dir)

            is_can_move = edge_list[now_pos[0]][now_pos[1]][direction.dir2index[dir]]
            is_root_dir = (dist_list[now_pos[0]][now_pos[1]] > dist_list[next_pos[0]][next_pos[1]])

            if is_can_move and is_root_dir:
                if is_opp:
                    trace.append(direction.turn_back(dir))
                else:
                    trace.append(dir)

                now_pos = next_pos
                break

    return trace
        
def treasure_hunt(x, y, w, h):
    MAX_DIST = 10000

    dist_list = []
    edge_list = []

    # 初期化
    for index_x in range(w+2):
        dist_list.append([])
        edge_list.append([])
        for index_y in range(h+2):
            dist_list[index_x].append(MAX_DIST)
            edge_list[index_x].append([False, False, False, False, False])

    now_dist = 0

    # マップ作り
    while True:
        now_pos = vector.create_vector(get_pos_x() + 1, get_pos_y() + 1)

        dist_list[now_pos[0]][now_pos[1]] = now_dist
        back_dir = None
        forward_dir = None

        for dir in direction.Directions:
            if can_move(dir):
                edge_list[now_pos[0]][now_pos[1]][direction.dir2index[dir]] = True
                
                next_pos = get_next_pos(now_pos, dir)

                if (now_dist + 1) < dist_list[next_pos[0]][next_pos[1]]:
                    forward_dir = dir
                elif dist_list[next_pos[0]][next_pos[1]] < now_dist:
                    back_dir = dir

        if forward_dir != None:
            now_dist += 1
            move(forward_dir)

        elif back_dir != None:
             move(back_dir)
             now_dist -= 1

        else:
            break

    for i in dist_list:
        quick_print(i)

    max_try_cnt = 200
    for try_cnt in range(max_try_cnt+1):
        trace = []

        t_x, t_y = measure()
        treasure_pos = vector.create_vector(t_x + 1, t_y + 1) # 宝箱の位置から探索

        treasure_trace = get_trace(dist_list, edge_list, treasure_pos)
        drone_trace = get_trace(dist_list, edge_list, vector.create_vector(get_pos_x()+1,get_pos_y()+1))

        lca_dist = 0

        while True:
            if lca_dist >= len(treasure_trace):
                lca_dist = len(treasure_trace)
                break

            elif lca_dist >= len(drone_trace):
                lca_dist = len(drone_trace)
                break
            
            elif (treasure_trace[len(treasure_trace)-1-lca_dist] != drone_trace[len(drone_trace)-1-lca_dist]):
                break

            lca_dist += 1

        trace_index = 0
        while trace_index < len(treasure_trace) - lca_dist:
            trace.append(direction.turn_back(treasure_trace[trace_index]))
            trace_index += 1

        trace_index = 0
        while trace_index < len(drone_trace) - lca_dist:
            trace.append(drone_trace[len(drone_trace) - 1 - (lca_dist + trace_index)])
            trace_index += 1

        while len(trace) > 0:
            dir = trace.pop()
            move(dir)
        if try_cnt < max_try_cnt:
            substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
            use_item(Items.Weird_Substance, substance)
        else:
            harvest()
            break
    

def main_loop():
    treasure_hunt(0, 0, get_world_size(), get_world_size())
    
def init():
    clear()
    
    moves.move_to(0, 0)
        
    plant(Entities.Bush)    
    substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
    use_item(Items.Weird_Substance, substance)
            
if __name__ == "__main__":
    while True:
        init()
        maze_strategy_init()
        main_loop()
    