for hat in Hats:
    if num_unlocked(hat) > 0:
        print(hat, "can use.")
        change_hat(hat)
        do_a_flip()
    else:
        print(hat, "can not use.")