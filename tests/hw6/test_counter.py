from hw6.counter import instances_counter


@instances_counter
class User:
    pass


# what if I want create new classes in each test?
def test_decorator_is_counting_instances():

    get_instance_count_from_class = User.get_created_instances()

    user, _, _ = User(), User(), User()
    get_instance_count_from_instance = user.get_created_instances()
    get_instance_count_after_reset = user.reset_instances_counter()

    assert get_instance_count_from_class == 0
    assert get_instance_count_from_instance == 3
    assert get_instance_count_after_reset == 3


def test_class_and_instance_get_the_same_result():

    user, _, _ = User(), User(), User()
    get_instance_count_from_instance = user.get_created_instances()
    get_instance_count_from_class = User.get_created_instances()

    assert get_instance_count_from_class == get_instance_count_from_instance
    user.reset_instances_counter()


def test_reset_instance_count():

    user, _, _ = User(), User(), User()
    instance_count_before_reset = user.get_created_instances()
    user.reset_instances_counter()
    instance_count_after_reset = user.get_created_instances()

    assert instance_count_before_reset == 3
    assert instance_count_after_reset == 0
