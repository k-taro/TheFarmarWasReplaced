import collections
import moves
import utils
import direction
import vector
from vector import vector2tuple

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

def get_current_coordinate(base_pos):
    return get_pos_x() + 1 - base_pos[0], get_pos_y() + 1 - base_pos[1]

def get_treasure_coordinate(base_pos):
    t_pos = measure()

    if t_pos == None:
        return None
    
    return t_pos[0] + 1 - base_pos[0], t_pos[1] + 1 - base_pos[1]

def create_edge_dict():
    ret = {
        North:False, 
        West:False, 
        South:False,
        East:False
    }
    return ret
    
def create_list_dist_edge(w, h):
    global MAX_DIST
    dist_list = {}
    edge_list = {}

    for pos1_x in range(w+2):
        for pos1_y in range(h+2):
            pos1 = (pos1_x, pos1_y)

            edge_list[pos1] = create_edge_dict()
            dist_list[pos1] = MAX_DIST

    return dist_list, edge_list


def set_edge(edge_list, pos, dir):
    next_pos = get_next_pos(pos, dir)

    if not pos in edge_list:
        edge_list[pos] = create_edge_dict()
    if not next_pos in edge_list:
        edge_list[next_pos] = create_edge_dict()

    edge_list[pos][dir] = True
    edge_list[next_pos][direction.turn_back(dir)] = True


def get_dist(dist_list, pos):
    if not pos in dist_list:
        dist_list[pos] = MAX_DIST

    return dist_list[pos]


def get_next_pos(now_pos, dir):
    return (now_pos[0] + dir2vec[dir][0], now_pos[1] + dir2vec[dir][1])


def bfs(edge_list, start_pos, end_pos, need_interrupt = False, base_pos = (0, 0)):
    queue = []
    dist_list = {}
    dist_list[start_pos] = 0
    first_index = 0

    queue.append(start_pos)
    while first_index < len(queue):
        q = queue[first_index]
        first_index += 1

        tmp_treasure = get_treasure_coordinate(base_pos)
        if need_interrupt and (tmp_treasure == None or tmp_treasure != end_pos):
            return []

        for dir in direction.Directions:
            next = get_next_pos(q, dir)
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
            next_pos = get_next_pos(now_pos, dir)

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
                if tmp_edge_list[pos][dir]:
                    set_edge(edge_list, pos, dir)

    return dist_list, edge_list


def research_map(dir, base_dist, w, h, has_to_spawn = True, base_pos = (0, 0)):
    branch_pos = None
    scout_drone_list = []
    dist_list = {}
    edge_list = {}
    now_dist = base_dist

    dist_list[get_current_coordinate(base_pos)] = base_dist

    if dir != None:
        move(dir)
        now_dist += 1

    # マップ作り
    while True:
        now_pos = get_current_coordinate(base_pos)

        if branch_pos != None and now_pos == branch_pos:
            branch_pos = None

        dist_list[now_pos] = now_dist

        back_dir = None
        forward_dir_list = []

        for dir in direction.Directions:
            if can_move(dir):
                next_pos = get_next_pos(now_pos, dir)
                set_edge(edge_list, now_pos, dir)

                if (now_dist + 1) < get_dist(dist_list, next_pos):
                    forward_dir_list.append(dir)
                elif get_dist(dist_list, next_pos) < now_dist:
                    back_dir = dir

        if len(forward_dir_list) != 0:
            if len(forward_dir_list) > 1:
                if branch_pos == None:
                    branch_pos = now_pos

            while len(forward_dir_list) > 1 and branch_pos != now_pos:
                dir = forward_dir_list.pop()
                next_pos = get_next_pos(now_pos, dir)

                hdrone = None
                if has_to_spawn:
                    def wrap_r_m():
                        return research_map(dir, now_dist, w, h)
                    hdrone = spawn_drone(wrap_r_m)

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

def hunting(edge_list, have_to_spawn, max_try_cnt, substance, base_pos):
    global MAX_DIST
    treasure_pos = get_treasure_coordinate(base_pos)
    if treasure_pos == None:
        return False
    
    drone_pos = get_current_coordinate(base_pos)

    trace_list = []
    if drone_pos != treasure_pos:
        trace_list = bfs(edge_list, drone_pos, treasure_pos, True, base_pos)

    while len(trace_list):
        t = trace_list.pop()
        move(direction.turn_back(t[KEY_TRACE_DIR]))
        drone_pos = get_current_coordinate(base_pos)

        shortcut_dir = None
        shortcut_dist = MAX_DIST

        tmp_treasure = get_treasure_coordinate(base_pos)
        if tmp_treasure == None or tmp_treasure != treasure_pos:
            return False

        # 壁の状況を調べて、ショートカットできるかも調べる
        for dir in direction.Directions:
            if can_move(dir) and not edge_list[drone_pos][dir]: # 空いてなかった壁が開いている
                next_pos = get_next_pos(drone_pos,dir)

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

    return True

def treasure_hunt(x, y, w, h, has_to_spawn = True, gold_limit = None, max_try_cnt = 299):
    substance = w * 2**(num_unlocked(Unlocks.Mazes) - 1)

    # マップ作り
    dist_list, edge_list = create_list_dist_edge(w,h)
    tmp_dist_list, tmp_edge_list = research_map(None, 0, w, h, has_to_spawn, (x, y))
    for pos in tmp_dist_list:
        dist_list[pos] = tmp_dist_list[pos]

    for pos in tmp_edge_list:
        for dir in direction.Directions:
            if tmp_edge_list[pos][dir]:
                set_edge(edge_list, pos, dir)

    is_found_treasure = True
    for try_cnt in range(max_try_cnt+1):
        have_to_spawn = (try_cnt < max_try_cnt - 10) and is_found_treasure and has_to_spawn
        is_found_treasure = hunting(edge_list, have_to_spawn, 10, substance, (x, y))

        if is_found_treasure:
            if try_cnt < max_try_cnt and (gold_limit == None or num_items(Items.Gold) < (gold_limit - (try_cnt+1) * substance)):
                use_item(Items.Weird_Substance, substance)

            else:
                harvest()
                quick_print("Finish!!!!!", try_cnt)
                break
    

def main_loop():
    treasure_hunt(0, 0, get_world_size(), get_world_size())
    
def init(x, y, w):
    moves.move_to(x + w // 2, y + w // 2)
        
    plant(Entities.Bush)    
    substance = w * 2**(num_unlocked(Unlocks.Mazes) - 1)
    use_item(Items.Weird_Substance, substance)
            
if __name__ == "__main__":
    while True:
        clear()

        init(0, 0, get_world_size())
        main_loop()
    