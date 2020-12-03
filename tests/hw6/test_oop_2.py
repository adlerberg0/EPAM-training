from datetime import timedelta

import pytest

from hw6.oop_2 import DeadlineError, Homework, HomeworkResult, Student, Teacher


@pytest.fixture(scope="module")
def first_teacher_instance():
    instance = Teacher("Daniil", "Shadrin")
    yield instance


@pytest.fixture(scope="module")
def second_teacher_instance():
    instance = Teacher("Aleksandr", "Smetanin")
    yield instance


@pytest.fixture(scope="module")
def good_student_instance():
    instance = Student("Roman", "Petrov")
    yield instance


@pytest.fixture(scope="module")
def lazy_student_instance():
    instance = Student("Lev", "Sokolov")
    yield instance


def test_creating_instances(
    first_teacher_instance, good_student_instance, lazy_student_instance
):
    teacher = first_teacher_instance
    good_student = good_student_instance
    lazy_student = lazy_student_instance

    the_deadline_was_yesterday = -1
    homework = Homework(
        "Text of the homework", timedelta(days=the_deadline_was_yesterday)
    )
    assert teacher.first_name == "Daniil"
    assert teacher.last_name == "Shadrin"

    assert good_student.first_name == "Roman"
    assert good_student.last_name == "Petrov"

    assert lazy_student.first_name == "Lev"
    assert lazy_student.last_name == "Sokolov"

    assert homework.is_active() is False


def test_check_hw_exception(good_student_instance):
    with pytest.raises(ValueError):
        HomeworkResult(good_student_instance, "fff", "Solution", 0)


def test_positive_hw_check(first_teacher_instance, good_student_instance):
    oop_hw = first_teacher_instance.create_homework("Learn OOP", 1)

    hw_result = good_student_instance.do_homework(oop_hw, "I have done this hw")
    temp_1 = first_teacher_instance.check_homework(hw_result)

    assert temp_1 is True
    assert isinstance(hw_result, HomeworkResult)
    assert hw_result.solution == "I have done this hw"
    first_teacher_instance.reset_results()


def test_negative_hw_check(first_teacher_instance, good_student_instance):
    oop_hw = first_teacher_instance.create_homework("Learn OOP", 0)

    with pytest.raises(DeadlineError):
        good_student_instance.do_homework(oop_hw, "I've done it too late")


def test_homework_done_structure(first_teacher_instance, good_student_instance):
    oop_hw = first_teacher_instance.create_homework("Learn OOP", 1)
    docs_hw = first_teacher_instance.create_homework("Read docs", 5)

    result_1 = good_student_instance.do_homework(oop_hw, "I have done this hw")
    result_2 = good_student_instance.do_homework(docs_hw, "I have done this hw too")

    temp_1 = first_teacher_instance.check_homework(result_1)
    temp_2 = first_teacher_instance.check_homework(result_2)

    assert result_1 in first_teacher_instance.homework_done[oop_hw]
    assert result_2 in first_teacher_instance.homework_done[docs_hw]
    assert temp_1 is True
    assert temp_2 is True
    first_teacher_instance.reset_results()


def test_homework_reset_results_method(
    first_teacher_instance,
    second_teacher_instance,
    good_student_instance,
    lazy_student_instance,
):
    oop_hw = first_teacher_instance.create_homework("Learn OOP", 1)
    docs_hw = first_teacher_instance.create_homework("Read docs", 5)

    result_1 = good_student_instance.do_homework(oop_hw, "I have done this hw")
    result_2 = good_student_instance.do_homework(docs_hw, "I have done this hw too")

    temp_1 = first_teacher_instance.check_homework(result_1)
    temp_2 = first_teacher_instance.check_homework(result_2)
    assert temp_1 is True
    assert temp_2 is True

    second_teacher_instance.reset_results(oop_hw)
    assert oop_hw not in second_teacher_instance.homework_done

    second_teacher_instance.reset_results(docs_hw)
    assert docs_hw not in second_teacher_instance.homework_done
    assert len(second_teacher_instance.homework_done) == 0


def test_homework_done_does_not_contain_duplicates(
    first_teacher_instance, second_teacher_instance, good_student_instance
):
    oop_hw = first_teacher_instance.create_homework("Learn OOP", 1)

    result_1 = good_student_instance.do_homework(oop_hw, "I have done this hw")

    first_teacher_instance.check_homework(result_1)
    temp_1 = first_teacher_instance.homework_done

    second_teacher_instance.check_homework(result_1)
    temp_2 = Teacher.homework_done
    Teacher.reset_results()

    assert temp_1 == temp_2
