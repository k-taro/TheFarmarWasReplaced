import collections
import moves
import utils
import direction
import vector
from vector import vector2tuple

ORIGIN = (1, 1)
MAX_DIST = 10000
KEY_TRACE_POS = "KEY_TRACE_POS"
KEY_TRACE_DIR = "KEY_TRACE_DIR"

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
    
def create_list_dist_edge(w, h):
    dist_list = {}
    edge_list = {}

    for pos1_x in range(w+2):
        for pos1_y in range(h+2):
            pos1 = (pos1_x, pos1_y)

            edge_list[pos1] = {
                North:False, 
                West:False, 
                South:False,
                East:False
            }

            dist_list[pos1] = MAX_DIST

    return dist_list, edge_list

def get_next_pos(now_pos, dir):
    return vector.create_vector(now_pos[0] + dir2vec[dir][0], now_pos[1] + dir2vec[dir][1])


def bfs(dist_list, edge_list, start_pos, end_pos):
    queue = []
    dist_list[start_pos] = 0
    first_index = 0

    queue.append(start_pos)
    while first_index < len(queue):
        q = queue[first_index]
        first_index += 1

        for dir in direction.Directions:
            next = vector2tuple(get_next_pos(q, dir))
            if edge_list[q][dir] and (not next in dist_list):
                queue.append(next)
                dist_list[next] = dist_list[q] + 1

                if next == end_pos:
                    first_index = len(queue)
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
                trace.append({KEY_TRACE_POS:now_pos, KEY_TRACE_DIR:dir})
                now_pos = next_pos
                break

    return trace


def await_scout(scout_drone_list, dist_list, edge_list):
    for hdrone in scout_drone_list:
        tmp_dist_list, tmp_edge_list = wait_for(hdrone)
        for pos in tmp_dist_list:
            dist_list[pos] = tmp_dist_list[pos]

        for pos in tmp_edge_list:
            for dir in direction.Directions:
                edge_list[pos][dir] = edge_list[pos][dir] or tmp_edge_list[pos][dir]

    return dist_list, edge_list


def research_map(dir, base_dist, w, h):
    branch_pos = None
    scout_drone_list = []
    dist_list, edge_list = create_list_dist_edge(w, h)
    now_dist = base_dist

    dist_list[(get_pos_x()+1, get_pos_y()+1)] = base_dist

    if dir != None:
        move(dir)
        now_dist += 1

    # マップ作り
    while True:
        now_pos = (get_pos_x() + 1, get_pos_y() + 1)

        if branch_pos != None and now_pos == branch_pos:
            branch_pos = None

        dist_list[now_pos] = now_dist

        back_dir = None
        forward_dir_list = []

        for dir in direction.Directions:
            if can_move(dir):
                next_pos = vector2tuple(get_next_pos(now_pos, dir))
                edge_list[now_pos][dir] = True
                edge_list[next_pos][direction.turn_back(dir)] = True

                if (now_dist + 1) < dist_list[next_pos]:
                    forward_dir_list.append(dir)
                elif dist_list[next_pos] < now_dist:
                    back_dir = dir

        if len(forward_dir_list) != 0:
            if len(forward_dir_list) > 1:
                if branch_pos == None:
                    branch_pos = now_pos

            while len(forward_dir_list) > 1:
                dir = forward_dir_list.pop()
                next_pos = vector2tuple(get_next_pos(now_pos, dir))
                def wrap_r_m():
                    return research_map(dir, now_dist, w, h)

#                hdrone = spawn_drone(wrap_r_m)
                hdrone = None
                if hdrone != None:
                    dist_list[next_pos] = now_dist + 1
                    scout_drone_list.append(hdrone)
                else:
                    forward_dir_list.append(dir)
                    break

            now_dist += 1
            move(forward_dir_list.pop())

        elif back_dir != None:
            if (branch_pos == None):
                break

            move(back_dir)
            now_dist -= 1

        else:
            break

    return await_scout(scout_drone_list,dist_list,edge_list)   

        
def treasure_hunt(x, y, w, h):
    global ORIGIN
    global MAX_DIST

    # マップ作り
    origin_dist_list, edge_list = research_map(None, 0, w, h)

    max_try_cnt = 300
    for try_cnt in range(max_try_cnt+1):
        t_x, t_y = measure()
        treasure_pos = (t_x + 1, t_y + 1) # 宝箱の位置から探索
        drone_pos = (get_pos_x() + 1, get_pos_y() + 1)
        dist_list = {}

        trace_list = []
        if drone_pos != treasure_pos:
            trace_list = bfs(dist_list, edge_list, drone_pos, treasure_pos)

        while len(trace_list):
            t = trace_list.pop()
            move(direction.turn_back(t[KEY_TRACE_DIR]))
            drone_pos = (get_pos_x() + 1, get_pos_y() + 1)

            shortcut_dir = None
            shortcut_dist = MAX_DIST
            # 壁の状況を調べて、ショートカットできるかも調べる
            for dir in direction.Directions:
                if can_move(dir) and not edge_list[drone_pos][dir]: # 空いてなかった壁が開いている
                    next_pos = vector2tuple(get_next_pos(drone_pos,dir))

                    edge_list[drone_pos][dir] = True
                    edge_list[next_pos][direction.turn_back(dir)] = True

                    # 通る予定だったかを調べ、一番ショートカットできる方向を記録する
                    for i in range(len(trace_list)):
                        if trace_list[i][KEY_TRACE_POS] == next_pos:
                            if shortcut_dist > (i+1):
                                shortcut_dir = dir
                                shortcut_dist = i+1
                            break
            
            if shortcut_dir != None:
                while len(trace_list) > shortcut_dist:
                    trace_list.pop()

                trace_list.append({KEY_TRACE_POS:drone_pos, KEY_TRACE_DIR:shortcut_dir})

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
        main_loop()
    