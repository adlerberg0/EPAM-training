"""
Написать декоратор instances_counter, который применяется к любому классу
и добавляет ему 2 метода:
get_created_instances - возвращает количество созданых экземпляров класса
reset_instances_counter - сбросить счетчик экземпляров,
возвращает значение до сброса
Имя декоратора и методов не менять
Ниже пример использования
"""


def instances_counter(cls):

    cls.created_instances = 0

    def __new__(cls):
        obj = super(cls, cls).__new__(cls)
        cls.created_instances += 1
        return obj

    def get_created_instances(*args):
        return cls.created_instances

    def reset_instances_counter(*args):
        val = cls.created_instances
        cls.created_instances = 0
        return val

    cls.__new__ = __new__
    cls.get_created_instances = get_created_instances
    cls.reset_instances_counter = reset_instances_counter
    """Some code"""
    return cls
