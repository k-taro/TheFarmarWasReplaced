import treasure_over_hunt
import moves
import direction

def init(w):
    clear()
    
    moves.move_to(0, 0)
        
    plant(Entities.Bush)    
    substance = w * 2**(num_unlocked(Unlocks.Mazes) - 1)
    use_item(Items.Weird_Substance, substance)

def get_treasure_coordinate():
    ret = measure()
    if ret != None:
        ret = (ret[0] + 1, ret[1] + 1)

    return ret


def hunting(edge_list, area_set, substance):
    treasure_pos = (-1, -1)
    before_tre_pos = (-1, 0)
    before_dir = None

    while True:
        while not treasure_pos in area_set:
            for _ in range(100):
                pass
            treasure_pos = get_treasure_coordinate()
            if treasure_pos == None:
                return

        drone_pos = treasure_over_hunt.get_current_coordinate()
        trace = []
        if drone_pos != treasure_pos:
            trace = treasure_over_hunt.bfs(edge_list, drone_pos, treasure_pos)

        while len(trace) > 0:
            t = trace.pop()
            before_dir = direction.turn_back(t[treasure_over_hunt.KEY_TRACE_DIR])
            move(before_dir)
        
        use_item(Items.Weird_Substance, substance)
        next_treasure_pos = get_treasure_coordinate()
        if treasure_pos == next_treasure_pos and next_treasure_pos == before_tre_pos:
            harvest()
            return
            
        before_tre_pos = treasure_pos
        treasure_pos = next_treasure_pos


def place_drones(edge_list, w, substance):
    SENTINEL = (-1, -1)
    search_stack=[]
    root_list = []
    children = {}
    now_pos = treasure_over_hunt.get_current_coordinate()
    visited_pos = set()
    children_threshold = (w*w*4 - 1) // (3*max_drones()) + 1

    for x in range(w+2):
        for y in range(w+2):
            children[x,y] = set()

    search_stack.append(SENTINEL) # 番兵
    while now_pos != SENTINEL:
        visited_pos.add(now_pos)
        next_pos = None
        for dir in direction.Directions:
            tmp_pos = treasure_over_hunt.get_next_pos(now_pos, dir)
            if edge_list[now_pos][dir] and not tmp_pos in visited_pos:
                next_pos = tmp_pos
                break
        
        if next_pos != None:
            search_stack.append(now_pos)
            now_pos = next_pos
            continue

        back_pos = search_stack.pop()
        children[now_pos].add(now_pos)

        child_cnt = 1
        next_child_list = []
        for dir in direction.Directions:
            cp = treasure_over_hunt.get_next_pos(now_pos,dir)
            if edge_list[now_pos][dir] and back_pos != cp and len(children[cp]) <= children_threshold:
                child_cnt += len(children[cp])
                if len(next_child_list) > 0:
                    if len(children[next_child_list[0]]) > len(children[cp]):
                        next_child_list.insert(0, cp)
                    elif len(children[next_child_list[-1]]) > len(children[cp]):
                        next_child_list.insert(-1, cp)
                    else:
                        next_child_list.append(cp)
                else:
                    next_child_list.append(cp)

        if child_cnt <= children_threshold:
            for c in next_child_list:
                children[now_pos].add(c)
                for gc in children[c]:
                    children[now_pos].add(gc)
            
        else:
            root_list.append(next_child_list.pop())
            for c in next_child_list:
                children[now_pos].add(c)
                for gc in children[c]:
                    children[now_pos].add(gc)

            if len(children[now_pos]) > children_threshold:
                root_list.append(now_pos)

        if back_pos == SENTINEL:
            root_list.append(now_pos)

        now_pos = back_pos

    parent_root = root_list[-1]
    parent_area = children[parent_root]

    for index in range(len(root_list)):
        r = root_list[index]
        trace = treasure_over_hunt.bfs(edge_list,treasure_over_hunt.get_current_coordinate(),r)
        while len(trace) > 0:
            t = trace.pop()
            move(direction.turn_back(t[treasure_over_hunt.KEY_TRACE_DIR]))
        def wrap_hunting():
            hunting(edge_list, children[r], substance)
        if index < len(root_list)-1:
            drone = spawn_drone(wrap_hunting)
            if drone == None:
                for c in children[r]:
                    parent_area.add(c)

    hunting(edge_list, parent_area, substance)

def treasure_hunt(x, y, w):
    substance = w * 2**(num_unlocked(Unlocks.Mazes) - 1)

    # マップ作り
    dist_list, edge_list = treasure_over_hunt.create_list_dist_edge(w,w)
    tmp_dist_list, tmp_edge_list = treasure_over_hunt.research_map(None, 0, w, w)
    for pos in tmp_dist_list:
        dist_list[pos] = tmp_dist_list[pos]

    for pos in tmp_edge_list:
        for dir in direction.Directions:
            if tmp_edge_list[pos][dir]:
                treasure_over_hunt.set_edge(edge_list, pos, dir)

    place_drones(edge_list, w, substance)

if __name__ == "__main__":
#    while True:
    init(get_world_size())
    treasure_hunt(0, 0, get_world_size())
