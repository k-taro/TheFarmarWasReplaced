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
