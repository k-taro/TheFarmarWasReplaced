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