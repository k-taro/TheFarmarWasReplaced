import utils

clear()

unlock_dist = utils.get_full_unlock_dict()
full_item_dict = utils.get_full_item_dict()

unlock_dist[Unlocks.Expand] = 6    

run_time = simulate("treasure_over_hunt", unlock_dist, full_item_dict, {}, 2, 2)
