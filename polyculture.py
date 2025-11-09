from operations import preparation
import utils
import moves
import operations

TARGET = Entities.Tree

PolyEntities = (Entities.Grass, Entities.Bush, Entities.Tree, Entities.Carrot)

def rand_plant(tpl_option):
    if len(tpl_option) == 0:
        return

    ent = utils.pick_random(tpl_option)
    operations.preparation(ent)


def single_polyculture(start_x, start_y, width, height, weight = {Entities.Carrot:1, Entities.Bush:1, Entities.Tree:1, Entities.Grass:1}, item = None, amount = 999999999999999):
    vote_before = []
    vote_after = []

    for x in range(width):
        vote_before.append([])
        vote_after.append([])
        for y in range(height):
            vote_after[x].append({
                Entities.Carrot:0,
                Entities.Bush:0,
                Entities.Tree:0,
                Entities.Grass:0,
            })
            vote_before[x].append({
                Entities.Carrot:0,
                Entities.Bush:0,
                Entities.Tree:0,
                Entities.Grass:0,
            })

    for x_index in range(width):
        for y_index in range(height):
            max_ent = None
            max_vote = 0

            # 植える植物を投票数で決める
            for ent in [Entities.Carrot, Entities.Bush, Entities.Tree, Entities.Grass]:
                vote = vote_before[x][y][ent]
                vote += vote_after[x][y][ent]

                if vote > max_vote:
                    max_vote = vote
                    max_ent = ent

            if max_ent == None:
                r = random()

                if r < 0.25:
                    max_ent = Entities.Carrot
                elif r < 0.5:
                    max_ent = Entities.Bush
                elif r < 0.75:
                    max_ent = Entities.Tree
                else:
                    max_ent = Entities.Grass

            # 投票済みの票を回収
            companion = get_companion()
            if companion != None:
                vote_ent = companion[0]
                vote_x, vote_y = companion[1]

                if (start_x < vote_x) and (vote_x < (start_x + width)) and (start_y < vote_y) and (vote_y < (start_y + height)):
                    vote_x -= start_x
                    vote_y -= start_y
                    if (vote_x < x_index) or ((vote_x == x_index) and (vote_y < y_index)):
                        vote_before[vote_x][vote_y][vote_ent] -= 1
                    else:
                        vote_after[vote_x][vote_y][vote_ent] -= 1

                    while not can_harvest():
                        pass

            harvest()
            if item != None and num_items(item) >= amount:
                if item == Items.Weird_Substance:
                    clear()
                return
            if max_ent == Entities.Carrot:
                cost = get_cost(Entities.Carrot)
                for e in cost:
                    if num_items(e) < cost[e]:
                        max_ent = e

            preparation(max_ent, False, item == Items.Weird_Substance)

            # 投票
            companion = get_companion()
            if companion != None:
                vote_ent = companion[0]
                vote_x, vote_y = companion[1]
                if (start_x < vote_x) and (vote_x < (start_x + width)) and (start_y < vote_y) and (vote_y < (start_y + height)):
                    vote_x -= start_x
                    vote_y -= start_y
                    if (vote_x < x_index) or ((vote_x == x_index) and (vote_y < y_index)):
                        vote_before[vote_x][vote_y][vote_ent] += weight[max_ent]
                    else:
                        vote_after[vote_x][vote_y][vote_ent] += weight[max_ent]

            move(North)

        for i in range(height):
            move(South)

        move(East)

    for i in range(width):
        move(West)


def poly_harvest(plant_option, use_fertilizer):

    if get_entity_type() != TARGET:
        operations.preparation(TARGET)

    if not can_harvest():
        return
    
    c_info = get_companion()

    if c_info != None:
        target_ent = c_info[0]
        target_pos = c_info[1]
        
        def f():
            moves.move_to(target_pos[0], target_pos[1])
            harvest()
            operations.preparation(target_ent, True, use_fertilizer)

        h = spawn_drone(f)

        if h != None:
            wait_for(h)

    harvest()
    rand_plant(plant_option)


def poly_farm(x, y, w, h, item, amount):
    plant_option = PolyEntities
    ent = None
    
    if item in utils.i2e_dict:
        ent = utils.item2ent(item)

    if ent != None:
        plant_option = (ent, )

    while True:
        moves.move_to(x, y)
        for x_index in range(w):
            for y_index in range(h):
                poly_harvest(plant_option, item == Items.Weird_Substance)
                if item != None and num_items(item) >= amount:
                    return

                move(North)
            
            move(East)
            for y_index in range(h):
                move(South)


def multi_polyculture(item, amount, area):
    drone_list = []

    ent = utils.item2ent(item)
#    target_entities = (ent, )

#    if ent == None:
#        target_entities = PolyEntities

    drone_num = ((max_drones())//2)
    for i in range(drone_num-1):
        def drone_operation():
            poly_farm(area[0] + area[2] - (i+1) * (area[2] // drone_num), area[1] + (i % 2) * area[3] // 2, area[2], area[3], item, amount)

        h = spawn_drone(drone_operation)
        drone_list.append(h)

        for _ in range(area[2] * area[3] * 10 // drone_num):
            pass

    poly_farm(area[0], area[1], area[2], area[3], item, amount)

    for h in drone_list:
        wait_for(h)


if __name__ == "__main__":
    multi_polyculture(TARGET, 10000000000, (0, 0, get_world_size(), get_world_size()))

