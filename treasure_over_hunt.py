import collections
import moves
import utils
import direction
import vector
from vector import vector2tuple

ORIGIN = (1, 1)
MAX_DIST = 10000

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

def set_dist(dist_list, pos1, pos2, dist):
    dist_list[pos1][pos2] = dist
    dist_list[pos2][pos1] = dist


# start_pos, end_pos はタプル！
def get_trace(dist_list, edge_list, start_pos, end_pos):
    trace = []
    now_pos = start_pos

    while now_pos == end_pos:
        for dir in direction.Directions:
            next_pos = get_next_pos(now_pos, dir)

            is_can_move = edge_list[now_pos][dir]
            is_close = dist_list[now_pos][end_pos] > dist_list[next_pos][end_pos]

            if is_can_move and is_close:
                trace.append(dir)
                now_pos = next_pos
                break

    return trace
        
def treasure_hunt(x, y, w, h):
    global ORIGIN
    global MAX_DIST

    dist_list = {}
    edge_list = {}

    # 初期化
    for pos1_x in range(w+2):
        for pos1_y in range(h+2):
            pos1 = (pos1_x, pos1_y)

            edge_list[pos1] = {
                North:False, 
                West:False, 
                South:False,
                East:False
            }

            dist_list[pos1] = {}
            for pos2_x in range(w+2):
                for pos2_y in range(h+2):
                    pos2 = (pos2_x, pos2_y)
                    dist_list[pos1][pos2] = MAX_DIST

    now_dist = 0

    # マップ作り
    while True:
        now_pos = (get_pos_x() + 1, get_pos_y() + 1)

        dist_list[ORIGIN][now_pos] = now_dist
        dist_list[now_pos] = {}
        dist_list[now_pos][ORIGIN] = now_dist

        back_dir = None
        forward_dir = None

        for dir in direction.Directions:
            if can_move(dir):
                edge_list[now_pos][dir] = True
                
                next_pos = vector2tuple(get_next_pos(now_pos, dir))

                if (now_dist + 1) < dist_list[ORIGIN][next_pos]:
                    forward_dir = dir
                elif dist_list[ORIGIN][next_pos] < now_dist:
                    back_dir = dir

        if forward_dir != None:
            now_dist += 1
            move(forward_dir)

        elif back_dir != None:
             move(back_dir)
             now_dist -= 1

        else:
            break

    for pos1_x in range(w+2):
        for pos1_y in range(h+2):
            pos1 = (pos1_x, pos1_y)
            for pos2_x in range(w+2):
                for pos2_y in range(h+2):
                    pos2 = (pos2_x, pos2_y)
                    dist_list[pos1][pos2] = abs(dist_list[ORIGIN][pos1] - dist_list[ORIGIN][pos2])
                    dist_list[pos2][pos1] = dist_list[pos1][pos2]


    max_try_cnt = 5
    for try_cnt in range(max_try_cnt+1):
        t_x, t_y = measure()
        treasure_pos = (t_x + 1, t_y + 1) # 宝箱の位置から探索
        drone_pos = (get_pos_x() + 1, get_pos_y() + 1)

        trace_list = get_trace(dist_list, edge_list, drone_pos, treasure_pos)

        for t in trace_list:
            move(t)
            drone_pos = (get_pos_x() + 1, get_pos_y() + 1)
            for dir in direction.Directions:
                if can_move(dir):
                    edge_list[drone_pos][dir] = True

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
    