# すべての構文が使える前提で良い
import farm_strategies
import operations
from operations import wrap_ope
from utils import wrap_has_enough_items, wrap_proc, item2ent
import utils

FIRST_TARGET = (Unlocks.Speed, Unlocks.Plant, Unlocks.Expand)
SECOND_TARGET = (Unlocks.Expand, Unlocks.Speed, Unlocks.Watering, Unlocks.Carrots)
THIRD_TARGET = (
    Unlocks.Expand,
    Unlocks.Speed,
    Unlocks.Trees,
    Unlocks.Grass,
    Unlocks.Expand,
    Unlocks.Watering,
    Unlocks.Carrots,
    Unlocks.Grass,
    Unlocks.Trees,
    Unlocks.Sunflowers,
    Unlocks.Fertilizer,
    Unlocks.Grass,
    Unlocks.Speed,
    Unlocks.Pumpkins,
    Unlocks.Watering,
    Unlocks.Fertilizer,
    Unlocks.Expand,
    Unlocks.Speed,
    Unlocks.Pumpkins,
    Unlocks.Trees,
    Unlocks.Carrots,
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
    Unlocks.Hats,
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
    Unlocks.Cactus,
    Unlocks.Dinosaurs,
    Unlocks.Leaderboard,
)


def do_unlock(target_unlock):
    area = (0, 0, get_world_size(), get_world_size())
    power_limit = 3 * (get_world_size() ** 2)
    costs = get_cost(target_unlock)
    milestone_list = [costs]

    if target_unlock == Unlocks.Mazes and num_items(Items.Weird_Substance) < 50:
        power_limit *= 30

    start_index = len(milestone_list) - 1

    for index in range(len(milestone_list)):
        is_all_enough = True
        milestone = milestone_list[start_index]

        for item in milestone:
            if milestone[item] > num_items(item):
                is_all_enough = False
                break

        if is_all_enough:
            start_index = index
            break

    while len(milestone_list)-1 > start_index:
        milestone_list.pop()

    while len(milestone_list) > 0:
        milestone = milestone_list.pop()

        for item in milestone:
            amount = milestone[item]
            if num_items(item) >= amount:
                continue

            if num_unlocked(Unlocks.Sunflowers) > 0 and num_items(Items.Power) < power_limit:
                farm_strategies.farm_single_plant(Items.Power, 2 * power_limit , area)
            farm_strategies.farm_single_plant(item,amount,area)

    return unlock(target_unlock)


def calc_milestone_list(costs):
    target_item_list = []
    while len(costs) > 0:
        target_item_list.append(costs)

        tmp_costs = {}
        for item in costs:
            ent = item2ent(item)
            item_costs = {}
            if ent == None:
                if item == Items.Gold:
                    item_costs[Items.Weird_Substance] = 2

            else:
                item_costs = get_cost(ent)

            if len(item_costs) == 0:
                continue

            for i in item_costs:
                if not i in tmp_costs:
                    tmp_costs[i] = 0

                tmp_costs[i] += item_costs[i] * costs[item]

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
        do_unlock(target_unlock)


if __name__ == "__main__":
    main()