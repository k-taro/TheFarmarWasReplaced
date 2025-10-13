from utils import move_zero_point


def move_center():
	move_zero_point()

	while (get_pos_x() < (get_world_size() / 2)):
		move(East)

	while (get_pos_y() < (get_world_size() / 2)):
		move(North)