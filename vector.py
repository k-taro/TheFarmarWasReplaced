KEY_X = "X"
KEY_Y = "Y"

def create_vector(x, y):
    return {KEY_X:x, KEY_Y:y}

def add(vec1, vec2):
    x = vec1[KEY_X] + vec2[KEY_X]
    y = vec1[KEY_Y] + vec2[KEY_Y]
    return create_vector(x, y)

def minus(vec1):
    return create_vector(-vec1[KEY_X], -vec1[KEY_Y])

def turn_right(vec1):
    return create_vector(vec1[KEY_Y], -vec1[KEY_X])

def turn_left(vec1):
    return create_vector(-vec1[KEY_Y], vec1[KEY_X])
