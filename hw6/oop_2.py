"""
В этом задании будем улучшать нашу систему классов из задания прошлой лекции
(Student, Teacher, Homework)
Советую обратить внимание на defaultdict из модуля collection для
использования как общую переменную
1. Как то не правильно, что после do_homework мы возвращаем все тот же
объект - будем возвращать какой-то результат работы (HomeworkResult)
HomeworkResult принимает объект автора задания, принимает исходное задание
и его решение в виде строки
Атрибуты:
    homework - для объекта Homework, если передан не этот класс -  выкинуть
    подходящие по смыслу исключение с сообщением:
    'You gave a not Homework object'
    solution - хранит решение ДЗ как строку
    author - хранит объект Student
    created - c точной датой и временем создания
2. Если задание уже просрочено хотелось бы видеть исключение при do_homework,
а не просто принт 'You are late'.
Поднимайте исключение DeadlineError с сообщением 'You are late' вместо print.
3. Student и Teacher имеют одинаковые по смыслу атрибуты
(last_name, first_name) - избавиться от дублирования с помощью наследования
4.
Teacher
Атрибут:
    homework_done - структура с интерфейсом как в словаре, сюда поподают все
    HomeworkResult после успешного прохождения check_homework
    (нужно гаранитировать отсутствие повторяющихся результатов по каждому
    заданию), группировать по экземплярам Homework.
    Общий для всех учителей. Вариант ипользования смотри в блоке if __main__...
Методы:
    check_homework - принимает экземпляр HomeworkResult и возвращает True если
    ответ студента больше 5 символов, так же при успешной проверке добавить в
    homework_done.
    Если меньше 5 символов - никуда не добавлять и вернуть False.
    reset_results - если передать экземпряр Homework - удаляет только
    результаты этого задания из homework_done, если ничего не передавать,
    то полностью обнулит homework_done.
PEP8 соблюдать строго.
Всем перечисленным выше атрибутам и методам классов сохранить названия.
К названием остальных переменных, классов и тд. подходить ответственно -
давать логичные подходящие имена.
"""
from collections import defaultdict
from datetime import datetime, timedelta


class DeadlineError(Exception):
    """ Error for situation when have done hw too late"""

    pass


class Person:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name


class Homework:
    def __init__(self, text: str, deadline: timedelta):
        self.text = text
        self.deadline = deadline
        self.created = datetime.now()

    def is_active(self):
        """
        Method for checking whether homework is expired or not
        """
        current_data = datetime.now()
        return current_data - self.created < self.deadline


class Student(Person):
    def __init__(self, first_name: str, last_name: str):
        super(Student, self).__init__(first_name, last_name)

    def do_homework(self, homework: Homework, solution: str):
        """
        Return a HomeworkResult instance if homework isn't expired
        """
        if not homework.is_active():
            raise DeadlineError("You are late")
        return HomeworkResult(homework, solution, author=self, created=datetime.now())


class HomeworkResult:
    def __init__(
        self, homework: Homework, solution: str, author: Student, created: datetime
    ):
        if not isinstance(homework, Homework):
            raise ValueError("You gave not a Homework object")
        self.homework = homework
        self.solution = solution
        self.author = author
        self.created = created


class Teacher(Person):
    homework_done = defaultdict(set)  # what to do there?

    def __init__(self, first_name: str, last_name: str):
        super().__init__(first_name, last_name)

    def check_homework(self, hw_result: HomeworkResult):
        """
        Add HomeworkResult instance to homework_done if solution is valid
        """
        if len(hw_result.solution) < 5:
            return False
        type(self).homework_done[hw_result.homework].add(hw_result)
        return True

    @classmethod
    def reset_results(cls, homework=None):
        """
        If homework is passed delete set of HomeworkResult instances from homework_done
        If not - clear homework_done
        """
        if homework is None:
            cls.homework_done.clear()
        else:
            cls.homework_done.pop(homework)

    @staticmethod
    def create_homework(text, days_limit):
        return Homework(text, timedelta(days=days_limit))


if __name__ == "__main__":
    opp_teacher = Teacher("Daniil", "Shadrin")
    advanced_python_teacher = Teacher("Aleksandr", "Smetanin")

    lazy_student = Student("Roman", "Petrov")
    good_student = Student("Lev", "Sokolov")

    oop_hw = opp_teacher.create_homework("Learn OOP", 1)
    docs_hw = opp_teacher.create_homework("Read docs", 5)

    result_1 = good_student.do_homework(oop_hw, "I have done this hw")
    result_2 = good_student.do_homework(docs_hw, "I have done this hw too")
    result_3 = lazy_student.do_homework(docs_hw, "done")
    try:
        result_4 = HomeworkResult(good_student, "fff", "Solution")
    except Exception:
        print("There was an exception here")
    opp_teacher.check_homework(result_1)
    temp_1 = opp_teacher.homework_done

    advanced_python_teacher.check_homework(result_1)
    temp_2 = Teacher.homework_done
    assert temp_1 == temp_2

    opp_teacher.check_homework(result_2)
    opp_teacher.check_homework(result_3)

    print(Teacher.homework_done[oop_hw])
    Teacher.reset_results()
