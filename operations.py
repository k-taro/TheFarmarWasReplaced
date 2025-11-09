import item_conf
import operations
import utils

ORDER_ZIGZAG = "ORDER_ZIGZAG"
ORDER_COLUMN_MAJOR = "ORDER_COLUMN_MAJOR"
KEY_ABORT = "KEY_ABORT"

def use_water_if_dry():
    if (get_water() < 0.7) and num_items(Items.Water) > 0:
        use_item(Items.Water)

def do_in_area(g, width, height, context, order = ORDER_ZIGZAG):
    dir_x = East
    dir_y = North

    if width < 0:
        dir_x = West
    
    if height < 0:
        dir_y = South

    for x in range(abs(width)):
        for y in range(abs(height)-1):
            context = g(context)
            if (x % 2 == 1) and (order == ORDER_ZIGZAG):
                move(utils.dir_opposite[dir_y])
            else:
                move(dir_y)

        context = g(context)
        if KEY_ABORT in context and context[KEY_ABORT]:
            return context
        
        if x < width-1:
            move(dir_x)
            if order == ORDER_COLUMN_MAJOR:
                for y in range(abs(height)-1):
                    move(utils.dir_opposite[dir_y])

    return context

# do_in_area に渡す関数を作る関数
# 前提条件: f は引数1つで、処理を終了したいときにTrueを返す関数
def wrap_ope(f, arg):
    def ope(context):
        ret = f(arg)
        if ret:
            context[KEY_ABORT] = True
        return context

    return ope


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
