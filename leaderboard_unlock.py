# すべての構文が使える前提で良い
import farm_strategies
import operations

FIRST_TARGET = (Unlocks.Speed, Unlocks.Plant, Unlocks.Expand)
SECOND_TARGET = (Unlocks.Expand, Unlocks.Carrots, Unlocks.Watering)
THIRD_TARGET = (Unlocks.Trees, Unlocks.Expand, Unlocks.Sunflowers)

def wrap_proc(f, arg):
    def g():
        return f(arg)
    return g


def wrap_ope(f, arg):
    def ope(context):
        ret = f(arg)
        if ret:
            context[operations.KEY_ABORT] = True
        return context
    
    return ope


def wrap_has_enough_items(item, amount):
    def f():
        return num_items(item) >= amount
    
    return f


def harvest_hwc(f):
    if can_harvest():
        harvest()

    x = get_pos_x()

    if x % get_world_size() == 1:
        if num_unlocked(Unlocks.Trees) > 0:
            farm_strategies.preparation(Entities.Tree)
        elif get_entity_type() != Entities.Bush:
            farm_strategies.preparation(Entities.Bush)

    elif x % get_world_size() > 1:
        farm_strategies.preparation(Entities.Carrot)

    else:
        farm_strategies.preparation(Entities.Grass)

    return f()


def harvest_sunflower(f):
    farm_strategies.preparation(Entities.Sunflower)
    return f()


def main():
    for target_unlock in FIRST_TARGET:
        while True:
            if can_harvest():
                harvest()
            if unlock(target_unlock):
                break

    for target_unlock in SECOND_TARGET:
        while True:

            for _ in range(get_world_size()):
                if can_harvest():
                    harvest()
                    plant(Entities.Bush)
                move(North)

            if unlock(target_unlock):
                break
            
            move(East)

    clear()

    for target_unlock in THIRD_TARGET:
        is_target_unlocked = wrap_proc(unlock, target_unlock)

        context = {operations.KEY_ABORT:False}
        ope = wrap_ope(harvest_hwc, is_target_unlocked)

        while context[operations.KEY_ABORT] == False:
            operations.do_in_area(ope, get_world_size(), get_world_size(), context)

    has_enough_carrot = wrap_has_enough_items(Items.Carrot, 500)
    ope = wrap_ope(harvest_hwc, has_enough_carrot)
    context = {operations.KEY_ABORT:False}
    while context[operations.KEY_ABORT] == False:
        operations.do_in_area(ope, get_world_size(), get_world_size(), context)

    has_enough_power = wrap_has_enough_items(Items.Power, 500)
    ope = wrap_ope(harvest_sunflower, has_enough_power)
    context = {operations.KEY_ABORT:False}
    while context[operations.KEY_ABORT] == False:
        operations.do_in_area(ope, get_world_size(), get_world_size(), context)

    while True:
        do_a_flip()

if __name__ == "__main__":
    main()