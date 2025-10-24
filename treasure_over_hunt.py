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


def bfs(dist_list, edge_list, start_pos, end_pos):
    queue = []
    dist_list[start_pos] = 0
    first_index = 0

    queue.append(start_pos)
    while len(queue) > 0:
        q = queue[first_index]
        first_index += 1

        for dir in direction.Directions:
            next = vector2tuple(get_next_pos(q, dir))
            if edge_list[q][dir] and (not next in dist_list):
                queue.append(next)
                dist_list[next] = dist_list[q] + 1

                if next == end_pos:
                    queue = []
                    break
    
    return get_trace(dist_list, edge_list, end_pos)


# start_pos, end_pos はタプル！
def get_trace(dist_list, edge_list, end_pos):
    trace = []
    now_pos = end_pos

    while dist_list[now_pos] > 0:
        for dir in direction.Directions:
            next_pos = vector2tuple(get_next_pos(now_pos, dir))

            if not next_pos in dist_list:
                continue

            is_can_move = edge_list[now_pos][dir]
            is_close = dist_list[now_pos] > dist_list[next_pos]

            if is_can_move and is_close:
                trace.append(dir)
                now_pos = next_pos
                break

    return trace
        
def treasure_hunt(x, y, w, h):
    global ORIGIN
    global MAX_DIST

    origin_dist_list = {}
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

            origin_dist_list[pos1] = MAX_DIST
            dist_list[pos1] = MAX_DIST

    now_dist = 0

    # マップ作り
    while True:
        now_pos = (get_pos_x() + 1, get_pos_y() + 1)

        origin_dist_list[now_pos] = now_dist

        back_dir = None
        forward_dir = None

        for dir in direction.Directions:
            if can_move(dir):
                next_pos = vector2tuple(get_next_pos(now_pos, dir))
                edge_list[now_pos][dir] = True
                edge_list[next_pos][direction.turn_back(dir)] = True

                if (now_dist + 1) < origin_dist_list[next_pos]:
                    forward_dir = dir
                elif origin_dist_list[next_pos] < now_dist:
                    back_dir = dir

        if forward_dir != None:
            now_dist += 1
            move(forward_dir)

        elif back_dir != None:
             move(back_dir)
             now_dist -= 1

        else:
            break

    max_try_cnt = 10
    for try_cnt in range(max_try_cnt+1):
        t_x, t_y = measure()
        treasure_pos = (t_x + 1, t_y + 1) # 宝箱の位置から探索
        drone_pos = (get_pos_x() + 1, get_pos_y() + 1)
        dist_list = {}

        trace_list = bfs(dist_list, edge_list, drone_pos, treasure_pos)

        while len(trace_list):
            t = trace_list.pop()
            move(direction.turn_back(t))
            drone_pos = (get_pos_x() + 1, get_pos_y() + 1)
            for dir in direction.Directions:
                if can_move(dir):
                    next_pos = vector2tuple(get_next_pos(drone_pos,dir))

                    edge_list[drone_pos][dir] = True
                    edge_list[next_pos][direction.turn_back(dir)] = True

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
    