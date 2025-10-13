import utils

need_water_items = [
	Entities.Carrot, 
	Entities.Pumpkin, 
	Entities.Sunflower,
	Entities.Tree
	]
	
need_till_items = [
	Entities.Carrot, 
	Entities.Pumpkin, 
	Entities.Sunflower,
	]
	
def is_need_water(item):
	return utils.is_conntain(need_water_items, item)
	
def is_need_till(item):
	return utils.is_conntain(need_till_items, item)