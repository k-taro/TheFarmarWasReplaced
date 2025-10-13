dir_opposite = {
	North:South,
	West:East,
	South:North,
	East:West}
	
def sorted_index(data):
	index = list(range(len(data)))
	
	for i in range(len(data)):
		for j in range(len(data) - i -1):
			if data[index[j]] > data[index[j+1]]: #左の方が大きい場合
				index[j], index[j+1] = index[j+1], index[j] #前後入れ替え
				
	return index

def is_conntain(list, item):
	ret = False
	for i in list:
		if(i == item):
			ret = True
			
	return ret

def use_water_if_dry():
	if (get_water() < 0.5) and num_items(Items.Water) > 0:
		use_item(Items.Water)
		
def move_zero_point():
	while (get_pos_x() != 0):
		move(West)
	
	while (get_pos_y() != 0):
		move(South)
		
def move_center():
	move_zero_point()

	while (get_pos_x() < (get_world_size() / 2)):
		move(East)
	
	while (get_pos_y() < (get_world_size() / 2)):
		move(North)
		
def get_full_unlock_dict():
	unlock_dict = {}
	for ul in Unlocks:
		unlock_dict[ul] = 100

	return unlock_dict

def get_full_item_dict():
	item_dict = {}
	for it in Items:
		item_dict[it] = 65535

	return item_dict

		