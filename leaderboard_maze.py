import treasure_over_hunt
import moves

def hunting(pos, size):
    moves.move_to(pos[0], pos[1])
     
    treasure_over_hunt.treasure_hunt(pos[0], pos[1], size, size)


if __name__ == "__main__":
    drone = []

    base_x, base_y = 0, 0
    size = 5
    for i in range(6):
        for j in range(6):
            pos = (base_x + i * size, base_y + j * size)

            def wrap():
                hunting(pos, 5)

            d = spawn_drone(wrap)
            drone.append(d)


    while True:
        treasure_hunt.init()
        change_hat(Hats.Traffic_Cone)    
        treasure_hunt.maze_strategy_init()
        treasure_hunt.main_loop()
    