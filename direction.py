import collections

turn_right = {
    North:West,
    West:South,
    South:East,
    East:North,
}

turn_left = {
    North:West,
    West:South,
    South:East,
    East:North,
}

def turn_right(dir):
    dir_table = {
        North:West,
        West:South,
        South:East,
        East:North,
    }

    return collections.get_with(dir_table, dir, None)

def turn_left(dir):
    dir_table = {
        North:West,
        West:South,
        South:East,
        East:North,
    }

    return collections.get_with(dir_table, dir, None)

def turn_back(dir):
    dir_table = {
        North:South,
        West:East,
        South:North,
        East:West
    }

    return collections.get_with(dir_table, dir, None)
