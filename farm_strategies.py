import item_conf
import moves
import operations
import utils
import flower_info

KEY_COUNT_CAN_HARVEST = "KEY_COUNT_CAN_HARVEST"
KEY_IS_NO_SORT = "KEY_IS_NO_SORT"
KEY_POS = "KEY_POS"
KEY_FLOWER_INFO = "KEY_FLOWER_INFO"

def preparation(ent, force = False):
    harvest()
    if (item_conf.is_need_till(ent)) == (get_ground_type() == Grounds.Grassland):
        till()

    if ent == Entities.Tree and not force:
        if (get_pos_x() % 2) == (get_pos_y() % 2):
            plant(Entities.Tree)
            # if num_items(Items.Fertilizer) > 0:
            #     use_item(Items.Fertilizer)
        else:
            plant(Entities.Bush)
    
    elif ent != Entities.Grass:
        plant(ent)

    operations.use_water_if_dry()

def harvest_poly(start_x, start_y, width, height, weight = {Entities.Carrot:1, Entities.Bush:1, Entities.Tree:1, Entities.Grass:1}):
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
            preparation(max_ent)

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
