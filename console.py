import moves
import operations

def wrap_flip(context):
    do_a_flip()
    
    return context

moves.move_zero_point()
operations.do_in_area(wrap_flip, 3, 3, {})

