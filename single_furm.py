import utils
import item_conf

FURM_ITEM = Entities.Pumpkin

def init():
	clear()
	
	utils.move_zero_point()
	
	is_need_till = item_conf.is_need_till(FURM_ITEM)
	
	for pos_x in range(get_world_size()):
		for pos_y in range(get_world_size()):
			if is_need_till:
				till()
			
			move(North)
	
		move(East)

def main_loop():
	is_need_water = item_conf.is_need_water(FURM_ITEM)
	while True:
		for pos_y in range(get_world_size()):
			if can_harvest():
				harvest()
			
			if get_entity_type() != FURM_ITEM:
				plant(FURM_ITEM)
			
			if is_need_water:
				utils.use_water_if_dry()
				
			move(North)
		
		move(East)
		
if __name__ == "__main__":
	init()
	main_loop()
