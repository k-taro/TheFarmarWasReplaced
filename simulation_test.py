import utils

clear()

unlock_dist = utils.get_full_unlock_dict()
full_item_dict = utils.get_full_item_dict()

unlock_dist[Unlocks.Expand] = 8    

run_time = simulate("Apple_hunt_dinosaur", unlock_dist, full_item_dict, {}, 1, 2)
