dir_opposite = {
    North:South,
    West:East,
    South:North,
    East:West}

def pick_random(tpl_option):
    if len(tpl_option) == 0:
        return
    
    r = random()
    r *= len(tpl_option)

    ret = tpl_option[-1]

    for i in range(len(tpl_option)):
        if r < i+1:
            ret = tpl_option[i]
            break

    return ret


def get_full_unlock_dict():
    unlock_dict = {}
    for ul in Unlocks:
        unlock_dict[ul] = 100

    return unlock_dict

def get_full_item_dict():
    item_dict = {}
    for it in Items:
        item_dict[it] = 4294967296

    return item_dict

def calc_manhattan_dist(pos1, pos2):
    diff = 0
    diff = abs(pos1[0] - pos2[0])
    diff = diff + abs(pos1[1] - pos2[1])

def nop():
    return None

# comp は比較関数 a, bを比較し、aが小さければマイナスを返す
# comp(a, b):
#     return a - b
#
def max_index(l, comp):
    max_index = 0
    for i in range(len(l)):
        if comp(l[i], l[max_index]) > 0:
            max_index = i

    return max_index

def wrap_has_enough_items(item, amount):
    def f():
        return num_items(item) >= amount
    
    return f

def wrap_proc(f, arg):
    def g():
        return f(arg)
    return g

i2e_dict = {
    Items.Bone:None,
    Items.Cactus:Entities.Cactus,
    Items.Carrot:Entities.Carrot,
    Items.Fertilizer:None,
    Items.Gold:None,
    Items.Hay:Entities.Grass,
    Items.Power:Entities.Sunflower,
    Items.Pumpkin:Entities.Pumpkin,
    Items.Water:None,
    Items.Weird_Substance:None,
    Items.Wood:Entities.Tree,
}
def item2ent(item):
    return i2e_dict[item]