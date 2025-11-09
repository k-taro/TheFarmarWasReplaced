import item_conf
import moves
from moves import move_to
import operations
import utils
import flower_info
import treasure_over_hunt
import Apple_hunt_dinosaur

KEY_COUNT_CAN_HARVEST = "KEY_COUNT_CAN_HARVEST"
KEY_IS_NO_SORT = "KEY_IS_NO_SORT"
KEY_POS = "KEY_POS"
KEY_FLOWER_INFO = "KEY_FLOWER_INFO"

def preparation(ent, force = False, use_fertilizer = False):
    harvest()
    if (item_conf.is_need_till(ent)) == (get_ground_type() == Grounds.Grassland):
        till()

    if ent == Entities.Tree and not force:
        if (get_pos_x() % 2) == (get_pos_y() % 2):
            plant(Entities.Tree)
        else:
            plant(Entities.Bush)
    
    elif ent != Entities.Grass:
        plant(ent)

    operations.use_water_if_dry()
    if use_fertilizer and num_items(Items.Fertilizer) > 0:
        use_item(Items.Fertilizer)

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


def harvest_poly(start_x, start_y, width, height, weight = {Entities.Carrot:1, Entities.Bush:1, Entities.Tree:1, Entities.Grass:1}, item = None, amount = 999999999999999):
    vote_before = []
    vote_after = []

    for x in range(width):
        vote_before.append([])
        vote_after.append([])
        for y in range(height):
            vote_after[x].append({
                Entities.Carrot:0,
                Entities.Bush:0,
                Entities.Tree:0,
                Entities.Grass:0,
            })
            vote_before[x].append({
                Entities.Carrot:0,
                Entities.Bush:0,
                Entities.Tree:0,
                Entities.Grass:0,
            })

    for x_index in range(width):
        for y_index in range(height):
            max_ent = None
            max_vote = 0

            # 植える植物を投票数で決める
            for ent in [Entities.Carrot, Entities.Bush, Entities.Tree, Entities.Grass]:
                vote = vote_before[x][y][ent]
                vote += vote_after[x][y][ent]

                if vote > max_vote:
                    max_vote = vote
                    max_ent = ent

            if max_ent == None:
                r = random()

                if r < 0.25:
                    max_ent = Entities.Carrot
                elif r < 0.5:
                    max_ent = Entities.Bush
                elif r < 0.75:
                    max_ent = Entities.Tree
                else:
                    max_ent = Entities.Grass

            # 投票済みの票を回収
            companion = get_companion()
            if companion != None:
                vote_ent = companion[0]
                vote_x, vote_y = companion[1]

                if (start_x < vote_x) and (vote_x < (start_x + width)) and (start_y < vote_y) and (vote_y < (start_y + height)):
                    vote_x -= start_x
                    vote_y -= start_y
                    if (vote_x < x_index) or ((vote_x == x_index) and (vote_y < y_index)):
                        vote_before[vote_x][vote_y][vote_ent] -= 1
                    else:
                        vote_after[vote_x][vote_y][vote_ent] -= 1

                    while not can_harvest():
                        pass

            harvest()
            if item != None and num_items(item) >= amount:
                if item == Items.Weird_Substance:
                    clear()
                return
            if max_ent == Entities.Carrot:
                cost = get_cost(Entities.Carrot)
                for e in cost:
                    if num_items(e) < cost[e]:
                        max_ent = e

            preparation(max_ent, False, item == Items.Weird_Substance)

            # 投票
            companion = get_companion()
            if companion != None:
                vote_ent = companion[0]
                vote_x, vote_y = companion[1]
                if (start_x < vote_x) and (vote_x < (start_x + width)) and (start_y < vote_y) and (vote_y < (start_y + height)):
                    vote_x -= start_x
                    vote_y -= start_y
                    if (vote_x < x_index) or ((vote_x == x_index) and (vote_y < y_index)):
                        vote_before[vote_x][vote_y][vote_ent] += weight[max_ent]
                    else:
                        vote_after[vote_x][vote_y][vote_ent] += weight[max_ent]

            move(North)

        for i in range(height):
            move(South)

        move(East)

    for i in range(width):
        move(West)


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
            farm_single_plant(Items.Carrot, 5 * carrot_amount, (start_x, start_y, w, w))

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

def farm_single_plant(item, amount, area):
    ent = utils.item2ent(item)
    weight = {
        Entities.Carrot:1,
        Entities.Bush:1,
        Entities.Tree:1,
        Entities.Grass:1,
    }
    POLY_PLANT = (
        Entities.Carrot,
        Entities.Bush,
        Entities.Tree,
        Entities.Grass,
    )

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
                harvest_poly(area[0],area[1],area[2],area[3],weight,item, amount)
            else:
                harvest_horiz_stripe(area[0],area[1],area[2],area[3],item,amount)

        elif strategy == Leaderboards.Sunflowers:
            move_to(area[0], area[1])
            carrot_limit = 2 * area[2] * area[3] * get_cost(Entities.Sunflower)[Items.Carrot]
            if num_items(Items.Carrot) < carrot_limit:
                farm_single_plant(Items.Carrot, max(amount, carrot_limit), area)
            operations.do_in_area(harvest_if_can, area[2], area[3], {Entities:ent})

        elif strategy == Leaderboards.Pumpkins:
            farm_pumpkin(amount, area[0], area[1], min(area[2], area[3]))
        
        elif strategy == Leaderboards.Cactus:
            cactus_ctxt = {
                    KEY_POS:area, 
                    KEY_COUNT_CAN_HARVEST:True,
                    KEY_IS_NO_SORT:True,
                }
            pumpkin_amount = 2 * (min(area[2] , area[3]) ** 2) * get_cost(Entities.Cactus)[Items.Pumpkin]
            if num_items(Items.Pumpkin) < pumpkin_amount:
                farm_single_plant(Items.Pumpkin, pumpkin_amount, area)
            move_to(area[0], area[1])
            operations.do_in_area(harvest_cactus, area[2], area[3], cactus_ctxt, operations.ORDER_COLUMN_MAJOR)

        elif strategy == Leaderboards.Maze:
            size = min(area[2], area[3])
            substance = amount + (size * 2**(num_unlocked(Unlocks.Mazes) - 1))
            farm_single_plant(Items.Weird_Substance, substance,area)
            harvest_all(area)
            treasure_over_hunt.init(area[0], area[1], size)
            treasure_over_hunt.treasure_hunt(area[0], area[1], size, size, False, amount)

        elif strategy == Leaderboards.Dinosaur:
            Apple_hunt_dinosaur.init()
            target_x, target_y = measure()
            target = (target_x, target_y)
            Apple_hunt_dinosaur.tail_count = 0

            while target != None:
                target = Apple_hunt_dinosaur.go_to_apple(target)

            change_hat(Hats.Brown_Hat)
