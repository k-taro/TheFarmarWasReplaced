dir_opposite = {
	North:South,
	West:East,
	South:North,
	East:West}
	
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

		