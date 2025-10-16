import item_conf
import moves
import operations

KEY_COUNT_CAN_HARVEST = "KEY_COUNT_CAN_HARVEST"
KEY_IS_NO_SORT = "KEY_IS_NO_SORT"
KEY_POS = KEY_POS

def preparation(ent):
    if (item_conf.is_need_till(ent)) == (get_ground_type() == Grounds.Grassland):
        till()

    if ent == Entities.Tree:
        if (get_pos_x() % 2) == (get_pos_y() % 2):
            plant(Entities.Tree)
            use_item(Items.Fertilizer)
        else:
            plant(Entities.Bush)

    elif ent != Entities.Grass:
        plant(ent)

    operations.use_water_if_dry()

def sort_entities(w, h):
    while True:
        is_sorted = True

        for x_idx in range(w):
            for y_idx in range(h):
                cur_size = measure(None)
                south_size = measure(South)
                west_size = measure(West)

                if y_idx != 0:
                    if cur_size < south_size:
                        is_sorted = False
                        swap(South)
                        south_size = cur_size
                        cur_size = measure(None)

                if x_idx != 0:
                    if cur_size < west_size:
                        is_sorted = False
                        swap(West)

                move(North)

            move(East)
            for y_idx in range(h):
                move(South)

        for x_idx in range(w):
            move(West)

        if is_sorted:
            break

def sort_south_west(o_x, o_y):
    is_sorted = True
    cur_size = measure(None)
    south_size = measure(South)
    west_size = measure(West)

    if get_pos_y() != o_y:
        if cur_size < south_size:
            is_sorted = False
            swap(South)
            south_size = cur_size
            cur_size = measure(None)

    if get_pos_x() != o_x:
        if cur_size < west_size:
            is_sorted = False
            swap(West)

    return is_sorted

def harvest_sunflower(context):
    x, y, w, h = context[KEY_POS]
    flower_info = context["flower_info"]

    if get_entity_type() != Entities.Sunflower:
        preparation(Entities.Sunflower)

    if can_harvest():
        harvest()
        # sort_south_west(x, y)
        # if (get_pos_x() == x + w - 1) and (get_pos_y() == y + h - 1):
        #     harvest()

    return context

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