# すべての構文が使える前提で良い
import farm_strategies
import operations
from operations import wrap_ope
from utils import wrap_has_enough_items, wrap_proc

FIRST_TARGET = (Unlocks.Speed, Unlocks.Plant, Unlocks.Expand)
SECOND_TARGET = (Unlocks.Expand, Unlocks.Speed, Unlocks.Watering, Unlocks.Carrots)
THIRD_TARGET = (Unlocks.Expand, Unlocks.Speed, Unlocks.Trees, Unlocks.Grass, Unlocks.Expand, Unlocks.Watering, Unlocks.Carrots, Unlocks.Sunflowers)
FOURTH_TARGET = (
    Unlocks.Fertilizer,
    Unlocks.Grass,
    Unlocks.Speed,
    Unlocks.Pumpkins,
    Unlocks.Watering,
    Unlocks.Expand,
    Unlocks.Speed,
    Unlocks.Pumpkins,
    Unlocks.Trees,
    Unlocks.Carrots,
    Unlocks.Fertilizer,
    Unlocks.Mazes,
    Unlocks.Megafarm,
    Unlocks.Grass,
    Unlocks.Polyculture,
    Unlocks.Watering,
    Unlocks.Pumpkins,
    Unlocks.Trees,
    Unlocks.Cactus,
    Unlocks.Carrots,
    Unlocks.Expand,
    Unlocks.Megafarm,
    Unlocks.Fertilizer,
    Unlocks.Dinosaurs,
    Unlocks.Dinosaurs,
    Unlocks.Polyculture,
    Unlocks.Mazes,
    Unlocks.Grass,
    Unlocks.Watering,
    Unlocks.Pumpkins,
    Unlocks.Trees,
    Unlocks.Cactus,
    Unlocks.Carrots,
    Unlocks.Megafarm,
    Unlocks.Polyculture,
    Unlocks.Watering,
    Unlocks.Fertilizer,
    Unlocks.Grass,
    Unlocks.Pumpkins,
    Unlocks.Expand,
    Unlocks.Trees,
    Unlocks.Cactus,
    Unlocks.Carrots,
    Unlocks.Watering,
    Unlocks.Mazes,
    Unlocks.Megafarm,
    Unlocks.Dinosaurs,
    Unlocks.Polyculture,
    Unlocks.Trees,
    Unlocks.Grass,
    Unlocks.Pumpkins,
    Unlocks.Expand,
    Unlocks.Mazes,
    Unlocks.Megafarm,
    Unlocks.Trees,
    Unlocks.Watering,
    Unlocks.Carrots,
    Unlocks.Cactus,
    Unlocks.Watering,
    Unlocks.Carrots,
    Unlocks.Pumpkins,
    Unlocks.Pumpkins,
    Unlocks.Expand,
    Unlocks.Cactus,
    Unlocks.Dinosaurs,
    Unlocks.Polyculture,
    Unlocks.Grass,
    Unlocks.Trees,
    Unlocks.Grass,
    Unlocks.Trees,
    Unlocks.Carrots,
    Unlocks.Carrots,
    Unlocks.Pumpkins,
    Unlocks.Pumpkins,
    Unlocks.Cactus,
    Unlocks.Dinosaurs,
    Unlocks.Mazes,
    Unlocks.Dinosaurs,
    Unlocks.Mazes,
    Unlocks.Leaderboard,
)

def harvest_hwc(f):
    if can_harvest():
        harvest()

    y = get_pos_y()

    if y % get_world_size() >= 2 * get_world_size() // 3:
        if num_unlocked(Unlocks.Trees) > 0:
            farm_strategies.preparation(Entities.Tree)
        elif get_entity_type() != Entities.Bush:
            farm_strategies.preparation(Entities.Bush)

    elif y % get_world_size() >= 1 * get_world_size() // 3:
        farm_strategies.preparation(Entities.Carrot)

    else:
        farm_strategies.preparation(Entities.Grass)

    return f()

def calc_milestone_list(costs):
    target_item_list = []
    while len(costs) > 0:
        target_item_list.append(costs)

        tmp_costs = {}
        for item in costs:
            item_costs = get_cost(item)
            if len(item_costs) == 0:
                continue

            for i in item_costs:
                if not i in tmp_costs:
                    tmp_costs[i] = 0

                tmp_costs[i] += item_costs[i] * costs[i]

        costs = tmp_costs

    return target_item_list


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

    farm_strategies.farm_single_plant(Entities.Sunflower, Items.Power, 500, (0, 0, get_world_size(), get_world_size()))

    for target_unlock in FOURTH_TARGET:
        costs = get_cost(target_unlock)
        milestone_list = calc_milestone_list(costs)

        start_index = len(milestone_list) - 1

        while start_index > 0:
            is_all_enough = True
            milestone = milestone_list[start_index]

            for item in milestone:
                if milestone[item] < num_items(item):
                    is_all_enough = False
                    break

            if is_all_enough:
                break

            start_index -= 1

        for index in range(start_index, len(milestone_list)):
            milestone = milestone_list[index]

            for item in milestone:
                amount = milestone[item]
                if amount >= num_items(item):
                    continue

                farm_strategies.farm_single_plant








if __name__ == "__main__":
    main()