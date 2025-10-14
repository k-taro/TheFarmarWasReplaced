import utils

def use_water_if_dry():
    if (get_water() < 0.5) and num_items(Items.Water) > 0:
        use_item(Items.Water)

def do_in_area(g, width, height, context):
    dir_x = East
    dir_y = North

    if width < 0:
        dir_x = West
    
    if height < 0:
        dir_y = North

    for x in range(abs(width)):
        for y in range(abs(height)-1):
            context = g(context)
            if x % 2 == 0:
                move(dir_y)
            else:
                move(utils.dir_opposite[dir_y])

        context = g(context)
        if x < width-1:
            move(dir_x)
            # for y in range(abs(height)-1):
            #     move(utils.dir_opposite[dir_y])

    return context
