import moves
moves.move_zero_point()


for pos_x in range(get_world_size()):
	for pos_y in range(get_world_size()):
		harvest()
		move(North)
		
	move(East)