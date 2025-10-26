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


def bfs(dist_list, edge_list, start_pos, end_pos):
    queue = []
    dist_list[start_pos] = 0
    first_index = 0

    queue.append(start_pos)
    while first_index < len(queue):
        q = queue[first_index]
        first_index += 1

        tmp_treasure = measure()
        if tmp_treasure == None or (tmp_treasure[0] + 1, tmp_treasure[1] + 1) != end_pos:
            return []

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
                if tmp_edge_list[pos][dir]:
                    set_edge(edge_list, pos, dir)

    return dist_list, edge_list


def research_map(dir, base_dist, w, h):
    branch_pos = None
    scout_drone_list = []
    dist_list = {}
    edge_list = {}
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
                next_pos = vector2tuple(get_next_pos(now_pos, dir))
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

def hunting(edge_list, have_to_spawn, max_try_cnt, substance):
    global MAX_DIST
    tmp_treasure = measure()
    if tmp_treasure == None:
        return False
    
    treasure_pos = (tmp_treasure[0] + 1, tmp_treasure[1] + 1) # 宝箱の位置から探索
    drone_pos = (get_pos_x() + 1, get_pos_y() + 1)
    dist_list = {}

    trace_list = []
    if drone_pos != treasure_pos:
        trace_list = bfs(dist_list, edge_list, drone_pos, treasure_pos)

    if len(trace_list) > 0 and have_to_spawn:
        def wrap_hunting():
            subdrone_hunting(edge_list, measure(), max_try_cnt, substance)
        spawn_drone(wrap_hunting)

    while len(trace_list):
        t = trace_list.pop()
        move(direction.turn_back(t[KEY_TRACE_DIR]))
        drone_pos = (get_pos_x() + 1, get_pos_y() + 1)

        shortcut_dir = None
        shortcut_dist = MAX_DIST

        tmp_treasure = measure()
        if tmp_treasure == None or (tmp_treasure[0] + 1, tmp_treasure[1] + 1) != treasure_pos:
            return False

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

    return True

def subdrone_hunting(edge_list, first_treasure, max_try_cnt, substance):
    while True:
        tmp_treasure = measure()
        if tmp_treasure == None:
            return
        elif first_treasure != tmp_treasure:
            break
        else:
            pass

    for try_cnt in range(max_try_cnt):
        is_found_treasure = hunting(edge_list, substance, max_try_cnt, substance)
        if is_found_treasure:
            use_item(Items.Weird_Substance, substance)

def treasure_hunt(x, y, w, h):
    substance = w * 2**(num_unlocked(Unlocks.Mazes) - 1)

    # マップ作り
    dist_list, edge_list = create_list_dist_edge(w,h)
    tmp_dist_list, tmp_edge_list = research_map(None, 0, w, h)
    for pos in tmp_dist_list:
        dist_list[pos] = tmp_dist_list[pos]

    for pos in tmp_edge_list:
        for dir in direction.Directions:
            if tmp_edge_list[pos][dir]:
                set_edge(edge_list, pos, dir)

    max_try_cnt = 299
    is_found_treasure = True
    for try_cnt in range(max_try_cnt+1):
        have_to_spawn = (try_cnt < max_try_cnt - 10) and is_found_treasure
        is_found_treasure = hunting(edge_list, have_to_spawn, 10, substance)

        if is_found_treasure:
            if try_cnt < max_try_cnt:
                use_item(Items.Weird_Substance, substance)

            else:
                harvest()
                print("Finish!!!!!", try_cnt)
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
    