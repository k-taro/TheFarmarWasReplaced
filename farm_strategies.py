import moves
from moves import move_to
import operations
from operations import preparation
import utils
import flower_info
import leaderboard_maze
import treasure_over_hunt
import Apple_hunt_dinosaur
import polyculture
import cactus_only

KEY_COUNT_CAN_HARVEST = "KEY_COUNT_CAN_HARVEST"
KEY_IS_NO_SORT = "KEY_IS_NO_SORT"
KEY_POS = "KEY_POS"
KEY_FLOWER_INFO = "KEY_FLOWER_INFO"

POLY_PLANT = (
    Entities.Carrot,
    Entities.Bush,
    Entities.Tree,
    Entities.Grass,
)

def harvest_horiz_stripe(start_x, start_y, width, height, item, amount):
    use_fertilizer = (item == Items.Weird_Substance)
    while True:
        for _ in range(width):
            for _ in range(height):
                if can_harvest():
                    harvest()

                y = get_pos_y()

                if y % height >= 2 * height // 3:
                    if num_unlocked(Unlocks.Trees) > 0:
                        preparation(Entities.Tree, False, use_fertilizer)
                    elif get_entity_type() != Entities.Bush:
                        preparation(Entities.Bush, False, use_fertilizer)

                elif y % height >= 1 * height // 3:
                    preparation(Entities.Carrot, False, use_fertilizer)

                else:
                    preparation(Entities.Grass, False, use_fertilizer)

                if item != None and num_items(item) >= amount:
                    if item == Items.Weird_Substance:
                        clear()
                    return
                
                move(North)

            move(East)

        move_to(start_x, start_y)


def sort_south_west(o_x, o_y):
    is_sorted = True
    cur_size = measure(None)
    south_size = measure(South)
    west_size = measure(West)

    if get_pos_y() != o_y:
        if (south_size != None) and (cur_size < south_size):
            is_sorted = False
            swap(South)
            south_size = cur_size
            cur_size = measure(None)

    if get_pos_x() != o_x:
        if (west_size != None) and (cur_size < west_size):
            is_sorted = False
            swap(West)

    return is_sorted

def harvest_sunflower(context):
    x, y, w, h = context[KEY_POS]
    flower_info_list = []

    dir_x = East
    dir_y = North

    if w < 0:
        dir_x = West
    
    if h < 0:
        dir_y = South

    for x_idx in range(abs(w)):
        for _ in range(abs(h)-1):
            if get_entity_type() != Entities.Sunflower:
                preparation(Entities.Sunflower)
            
            while not can_harvest():
                pass

            flower_info_list.append(
                {
                    flower_info.KEY_MEASURE:measure(),
                    flower_info.KEY_POS:[get_pos_x(), get_pos_y()]
                }
            )
            if (x_idx % 2 == 1):
                move(utils.dir_opposite[dir_y])
            else:
                move(dir_y)

        if x_idx < w-1:
            move(dir_x)


    m_idx = utils.max_index(flower_info_list, flower_info.comp_flower)
    target_x, target_y = flower_info_list.pop(m_idx)[flower_info.KEY_POS]

    moves.move_to(target_x, target_y)
    harvest()
    preparation(Entities.Sunflower)


def harvest_cactus(context):
    x, y, w, h = context[KEY_POS]

    if get_pos_x() == x and get_pos_y() == y:
        context[KEY_IS_NO_SORT] = True

    if get_entity_type() != Entities.Cactus:
        preparation(Entities.Cactus)

    if can_harvest():
        is_no_sort = sort_south_west(x, y)
        context[KEY_IS_NO_SORT] = context[KEY_IS_NO_SORT] and is_no_sort
        context[KEY_COUNT_CAN_HARVEST] += 1
    else:
        context[KEY_COUNT_CAN_HARVEST] = 0

    if (get_pos_x() == x + w - 1) and (get_pos_y() == y + h - 1):
        if (context[KEY_COUNT_CAN_HARVEST] >= w * h) and context[KEY_IS_NO_SORT]:
            harvest()

    return context

def harvest_pumpkin(context):
    x, y, w, h = context[KEY_POS]

    if get_entity_type() != Entities.Pumpkin:
        preparation(Entities.Pumpkin)

    if not can_harvest():
        context[KEY_COUNT_CAN_HARVEST] = 0
    else:
        context[KEY_COUNT_CAN_HARVEST] += 1
        if context[KEY_COUNT_CAN_HARVEST] >= w * h:
            harvest()

    return context

def farm_pumpkin(amount, start_x, start_y, w):
    pumpkin_id_list = {}
    pumpkin_size = min(6, w)
    carrot_amount = 3 * (w ** 2) * get_cost(Entities.Pumpkin)[Items.Carrot]

    for x in range(w):
        for y in range(-pumpkin_size+1, w, 1):
            pumpkin_id_list[x,y] = 0

    while True:
        moves.move_to(start_x, start_y)
        if num_items(Items.Carrot) <= carrot_amount:
            farm_multi_plant(Items.Carrot, 5 * carrot_amount, (start_x, start_y, w, w))

        is_less_carrot = False

        for pos_x in range(w):
            for pos_y in range(w):
                if num_items(Items.Pumpkin) >= amount:
                    return
                
                if get_entity_type() != Entities.Pumpkin:
                    preparation(Entities.Pumpkin)
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

                if num_items(Items.Carrot) <= carrot_amount:
                    is_less_carrot = True
                    break

            if is_less_carrot:
                break
            
            moves.move_to(start_x+pos_x, start_y)
            move(East)

def mult_famr_pumpkin(item, amount, area):
    drone_list = []
    pumpkin_area = [
        # {Entities:Entities.Pumpkin, KEY_POS:[0,0,6,6]}, # sample
    ]

    x_pos = area[0]
    while x_pos < area[2]:
        y_pos = area[1]
        remain_x = area[2] - x_pos
        while y_pos < area[3]:
            remain_y = area[3] - y_pos

            size = min(remain_y, 6)
            size = min(size, remain_x) # y側の余白が小さかった場合、x側でさらに枠を確保できるかもしれないが省略

            tmp_area = (x_pos, y_pos, size, size)
            pumpkin_area.append({Entities:Entities.Pumpkin, KEY_POS:tmp_area})

            y_pos += size + 1

        x_pos += min(remain_x, 6) + 1

    num_area = len(pumpkin_area) // max_drones()

    while num_items(item) < amount:
        if num_items(Items.Carrot) < get_cost(Entities.Pumpkin)[Items.Carrot] * area[2] * area[3]:
            farm_multi_plant(Items.Carrot, amount, area)

        for drone_index in range(max_drones()-1):
            def f():
                while num_items(item) < amount:
                    if num_items(Items.Carrot) < get_cost(Entities.Pumpkin)[Items.Carrot] * area[2] * area[3]:
                        return

                    for conf_index in range(drone_index * num_area, (drone_index+1)*num_area):
                        conf  = pumpkin_area[conf_index]
                        pos = conf[KEY_POS]
                        move_to(pos[0], pos[1])
                        operations.do_in_area(harvest_pumpkin, pos[2], pos[3], {KEY_POS:conf[KEY_POS], KEY_COUNT_CAN_HARVEST:0})

            h = spawn_drone(f)
            drone_list.append(h)

        drone_index = max_drones()-1
        def f():
            while num_items(item) < amount:
                if num_items(Items.Carrot) < get_cost(Entities.Pumpkin)[Items.Carrot] * area[2] * area[3]:
                    return

                for conf_index in range(drone_index * num_area, len(pumpkin_area)):
                    conf  = pumpkin_area[conf_index]
                    pos = conf[KEY_POS]
                    move_to(pos[0], pos[1])
                    operations.do_in_area(harvest_pumpkin, pos[2], pos[3], {KEY_POS:conf[KEY_POS], KEY_COUNT_CAN_HARVEST:0})

        f()

        for h in drone_list:
            wait_for(h)


def harvest_if_can(context):
    ent = context[Entities]

    if can_harvest():
        harvest()

    if get_entity_type() != ent:
        preparation(ent)

    return context

def wait_and_harvest(context):
    ent = context[Entities]

    if get_entity_type() != ent:
        preparation(ent)
        return context

    while not can_harvest():
        pass

    harvest()
    if get_entity_type() != ent:
        preparation(ent)

    return context

def harvest_all(area):
    move_to(area[0],area[1])
    operations.do_in_area(harvest_if_can,area[2],area[3],{Entities:Entities.Grass})


def farm_multi_plant(item, amount, area):
    ent = utils.item2ent(item)
    drone_list = []
    weight = {
        Entities.Carrot:1,
        Entities.Bush:1,
        Entities.Tree:1,
        Entities.Grass:1,
    }

    strategy = None

    move_to(area[0], area[1])
    if ent == None:
        if item == Items.Bone:
            strategy = Leaderboards.Dinosaur
        elif item == Items.Gold:
            strategy = Leaderboards.Maze

    elif ent == Entities.Sunflower:
        strategy = Leaderboards.Sunflowers

    elif ent == Entities.Pumpkin:
        strategy = Leaderboards.Pumpkins

    elif ent == Entities.Cactus:
        strategy = Leaderboards.Cactus

    elif ent in POLY_PLANT:
        # 対象の植物のみ投票権を与える
        for e in weight:
            if e != ent:
                weight[e] = 0

    while num_items(item)<amount:
        if strategy == None:
            if num_unlocked(Unlocks.Polyculture) > 0:
                if max_drones() > 2:
                    polyculture.multi_polyculture(item, amount, area)

                else:
                    polyculture.single_polyculture(area[0],area[1],area[2],area[3],weight,item, amount)

            else:
                harvest_horiz_stripe(area[0],area[1],area[2],area[3],item,amount)

        elif strategy == Leaderboards.Sunflowers:
            move_to(area[0], area[1])
            carrot_limit = 2 * area[2] * area[3] * get_cost(Entities.Sunflower)[Items.Carrot]
            if num_items(Items.Carrot) < carrot_limit:
                farm_multi_plant(Items.Carrot, max(amount, carrot_limit), area)

            w = area[2] // max_drones()
            h = area[3] // max_drones()
            y = area[1]

            for i in range(max_drones()-1):
                x = area[0] + area[2] - (i+1) * w
                move_to(x,y)
                def f():
                    operations.do_in_area(harvest_if_can, w, h, {Entities:ent})

                h_drone = spawn_drone(f)
                drone_list.append(h_drone)

            move_to(area[0], area[1])
            operations.do_in_area(harvest_if_can, area[2], area[3], {Entities:ent})

            for h_drone in drone_list:
                wait_for(h_drone)

        elif strategy == Leaderboards.Pumpkins:
            mult_famr_pumpkin(item, amount, area)
        
        elif strategy == Leaderboards.Cactus:
            pumpkin_amount = 2 * (min(area[2] , area[3]) ** 2) * get_cost(Entities.Cactus)[Items.Pumpkin]
            if num_items(Items.Pumpkin) < pumpkin_amount:
                farm_multi_plant(Items.Pumpkin, pumpkin_amount, area)
            move_to(area[0], area[1])
            cactus_only.main(area[0], area[1], min(area[2], area[3]))

        elif strategy == Leaderboards.Maze:
            # area は正方形であることを前提とする
            length = min(area[2], area[3])
            substance = amount + (length * 2**(num_unlocked(Unlocks.Mazes) - 1))
            farm_multi_plant(Items.Weird_Substance, substance,area)
            harvest_all(area)
            drone_list = []
            if num_unlocked(Unlocks.Megafarm) < 2:
                # 2台以下なら手分けしづらいので1台で探索する
                treasure_over_hunt.init(area[0], area[1], length)
                treasure_over_hunt.treasure_hunt(area[0], area[1], length, length, False, amount)
            else:
                # 4or16台ならちょうどよく分割できる
                div = 2
                # 8台は4台へ丸める。32台は16台に丸める
                if num_unlocked(Unlocks.Megafarm) > 2:
                    div = 4

                single_length = length // div
                single_tick = 500
                max_tick = div*div*single_tick

                l = []
                for i in range(div):
                    for j in range(div):
                        if i == 0 and j == 0:
                            continue

                        pos = (area[0]+i*single_length,area[1]+j*single_length)
                        def f():
                            leaderboard_maze.hunting(pos, single_length, max_tick - single_tick * len(drone_list))

                        h_drone = spawn_drone(f)
                        drone_list.append(h_drone)

                while num_items(item) < amount:
                    treasure_over_hunt.init(area[0], area[1], single_length)
                    treasure_over_hunt.treasure_hunt(area[0], area[1], single_length, single_length, False, amount)

        elif strategy == Leaderboards.Dinosaur:
            cactus_amount = get_cost(Entities.Apple)[Items.Cactus] * area[2] * area[3]
            farm_multi_plant(Items.Cactus, cactus_amount, area)

            Apple_hunt_dinosaur.init()
            target_x, target_y = measure()
            target = (target_x, target_y)
            Apple_hunt_dinosaur.tail_count = 0

            while target != None:
                target = Apple_hunt_dinosaur.go_to_apple(target)

            change_hat(Hats.Brown_Hat)
