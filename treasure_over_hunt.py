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

def get_trace(dist_list, start_pos, is_opp = False):
    trace = []
    now_pos = start_pos

    while dist_list[now_pos[0]][now_pos[1]] > 0:
        for dir in direction.Directions:
            next_pos = get_next_pos(now_pos, dir)

            if dist_list[now_pos[0]][now_pos[1]] < dist_list[next_pos[0]][next_pos[1]]:
                if is_opp:
                    trace.append(direction.turn_back(dir))
                else:
                    trace.append(dir)

                now_pos = next_pos
                break

    return trace
        
def treasure_hunt(x, y, w, h):
    MAX_DIST = 10000

    dist_list = [[]]
    edge_list = [[]]

    dir2index = {
        North:0,
        West:1,
        South:2,
        East:3,
    }

    # 初期化
    for index_x in range(w+2):
        for index_y in range(h+2):
            dist_list[index_x][index_y] = MAX_DIST
            edge_list[index_x][index_y] = [False, False, False, False]

    now_dist = 0

    while True:
        now_pos = vector.create_vector(get_pos_x() + 1, get_pos_y() + 1)

        dist_list[now_pos[0]][now_pos[1]] = now_dist
        back_dir = None

        for dir in direction.Directions:
            if can_move(dir):
                edge_list[now_pos[0]][now_pos[1]][dir2index[dir]] = True
                
                next_pos = get_next_pos(now_pos, dir)

                if (now_dist + 1) < dist_list[next_pos[0]][next_pos[1]]:
                    dist_list[next_pos[0]][next_pos[1]] = now_dist + 1
                    move(dir)
                elif dist_list[next_pos[0]][next_pos[1]] < now_dist:
                    back_dir = dir

        if back_dir == None:
            break
        else:
             move(back_dir)
        
    for _ in range(10):
        trace = []

        t_x, t_y = measure()
        treasure_pos = vector.create_vector(t_x, t_y) # 宝箱の位置から探索

        trace.add(get_trace(dist_list, treasure_pos, True))
        trace.add(get_trace(dist_list, vector.create_vector(get_pos_x()+1,get_pos_y()+1)))

        while len(trace) > 0:
            dir = trace.pop()

        substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
        use_item(Items.Weird_Substance, substance)


def main_loop():
    treasure_hunt()
    
def init():
    clear()
    
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
    