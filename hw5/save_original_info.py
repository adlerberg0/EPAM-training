"""
Написать декоратор который позволит сохранять информацию из
исходной функции (__name__ and __doc__), а так же сохранит саму
исходную функцию в атрибуте __original_func

print_result изменять нельзя, за исключением добавления вашего
декоратора на строку отведенную под него - замените комментарий

До применения вашего декоратор будет вызываться AttributeError при custom_sum.__original_func
Это корректное поведение
После применения там должна быть исходная функция

Ожидаемый результат:
print(custom_sum.__doc__)  # 'This function can sum any objects which have __add___'
print(custom_sum.__name__)  # 'custom_sum'
print(custom_sum.__original_func)  # <function custom_sum at <some_id>>
"""


def save_function_params(origin_function):
    def wraps(custom_func):
        custom_func.__name__ = origin_function.__name__
        custom_func.__doc__ = origin_function.__doc__
        custom_func.__original_func = origin_function

        return custom_func

    return wraps


def print_result(func):
    @save_function_params(func)
    def wrapper(*args, **kwargs):
        """Function-wrapper which print result of an original function"""
        result = func(*args, **kwargs)
        print(result)
        return result

    return wrapper
