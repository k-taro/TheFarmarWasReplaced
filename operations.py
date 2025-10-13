def use_water_if_dry():
	if (get_water() < 0.5) and num_items(Items.Water) > 0:
		use_item(Items.Water)