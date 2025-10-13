import utils

unlock_dist = utils.get_full_unlock_dict()
full_item_dict = utils.get_full_item_dict()

unlock_dist[Unlocks.Expand] = 5	

run_time = simulate("strategy_general", unlock_dist, full_item_dict, {}, 1, 64)
