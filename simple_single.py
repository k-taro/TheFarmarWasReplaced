# simple_single.py
import farm_strategies

TARGET = Leaderboards.Sunflowers_Single

CONDITION = {
    Leaderboards.Hay_Single:(Entities.Grass, Items.Hay, 100000000),
    Leaderboards.Cactus_Single:(Entities.Carrot, Items.Carrot, 100000000),
    Leaderboards.Wood_Single:(Entities.Tree,Items.Wood, 500000000),
    Leaderboards.Sunflowers_Single:(Entities.Sunflower, Items.Power, 10000),
}

def main():
    ent = CONDITION[TARGET][0]
    item = CONDITION[TARGET][1]
    amount = CONDITION[TARGET][2]

    weight = {
        Entities.Carrot:1,
        Entities.Bush:1,
        Entities.Tree:1,
        Entities.Grass:1,
    }

    weight[ent] = 1
    while num_items(item)<amount:
        if ent != Entities.Sunflower:
            farm_strategies.harvest_poly(0,0,get_world_size(),get_world_size())
        else:
            for x in range(get_world_size()):
                for y in range(get_world_size()):
                    if num_items(item)>=amount:
                        return

                    if get_entity_type() != ent:
                        farm_strategies.preparation(ent)
                    if can_harvest():
                        harvest()
                    move(North)
                move(East)


if __name__ == "__main__":
    main()
