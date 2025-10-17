def is_conntain(list, item):
    ret = False
    for i in list:
        if(i == item):
            ret = True

    return ret


def sorted_index(data):
    index = list(range(len(data)))

    for i in range(len(data)):
        for j in range(len(data) - i -1):
            if data[index[j]] > data[index[j+1]]: #左の方が大きい場合
                index[j], index[j+1] = index[j+1], index[j] #前後入れ替え

    return index


def get_with_defalt(dict, key, defalt):
    if not (key in dict):
        return defalt
    else:
        return dict[key]
