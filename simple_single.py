# simple_single.py
from moves import move_to
import utils
import operations
import farm_strategies

TARGET = Leaderboards.Sunflowers_Single

CONDITION = {
    Leaderboards.Hay_Single:(Entities.Grass, Items.Hay, 100000000),
    Leaderboards.Cactus_Single:(Entities.Carrot, Items.Carrot, 100000000),
    Leaderboards.Wood_Single:(Entities.Tree,Items.Wood, 500000000),
    Leaderboards.Sunflowers_Single:(Entities.Sunflower, Items.Power, 10000),
}

if __name__ == "__main__":
    farm_strategies.farm_single_plant(CONDITION[TARGET][0], CONDITION[TARGET][1], CONDITION[TARGET][2], (0,0,get_world_size(),get_world_size()))
