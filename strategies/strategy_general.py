import utils

def flower_shop():
	while True:
		if can_harvest():
			harvest()
		elif get_entity_type() != Entities.Sunflower:
			plant(Entities.Sunflower)
			
		utils.use_water_if_dry()
		
		for i in range(3):
			do_a_flip()

def init():
	clear()
	
	utils.move_zero_point()

	for pos_x in range(get_world_size()):
		for pos_y in range(get_world_size()):
			if (pos_x >= 3 and pos_y < 3):
				till()
				plant(Entities.Carrot)
			
			if (pos_x < 3 and pos_y < 3):
				till()
				plant(Entities.Pumpkin)
				
			if (pos_x == get_world_size()-1 and pos_y == get_world_size()-1):
				till()
				plant(Entities.Sunflower)
				spawn_drone(flower_shop)
		
			move(North)
	
		move(East)
		
def main_loop():
	while True:
		is_all_pumpkin = True
		for pos_x in range(get_world_size()):
			for pos_y in range(get_world_size()):
				if can_harvest() and get_entity_type() != Entities.Pumpkin:
					harvest()
					
				if (pos_x >= 3 and pos_y < 3):
					if get_entity_type() != Entities.Carrot:
						plant(Entities.Carrot)
					utils.use_water_if_dry()
					
				elif pos_y == 4 or pos_y == 6:
					if (get_pos_x() % 2) != 1:
						if get_entity_type() != Entities.Tree:
							plant(Entities.Tree)
							use_item(Items.Fertilizer)
						utils.use_water_if_dry()
					else:
						if get_entity_type() != Entities.Bush:
							plant(Entities.Bush)
							
				elif (pos_x < 3 and pos_y < 3):
					if get_entity_type() != Entities.Pumpkin:
						plant(Entities.Pumpkin)
						is_all_pumpkin = False
						
					utils.use_water_if_dry()
				
				elif (pos_x == get_world_size()-1 and pos_y == get_world_size()-1):
					if get_entity_type() != Entities.Sunflower:
						plant(Entities.Sunflower)
					utils.use_water_if_dry()
					
				move(North)			
							
			move(East)
		
		if is_all_pumpkin:
			harvest()
			
if __name__ == "__main__":
	init()
	main_loop()
