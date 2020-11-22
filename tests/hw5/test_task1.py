from datetime import timedelta

from hw5.oop_1 import Homework, Student, Teacher


def test_summoning_student():
    student = Student("Roman", "Petrov")

    assert student.first_name == "Roman"
    assert student.last_name == "Petrov"


def test_summoning_teacher():
    teacher = Teacher("Daniil", "Shadrin")

    assert teacher.first_name == "Daniil"
    assert teacher.last_name == "Shadrin"


def test_summoning_homework():
    the_deadline_is_yesterday = -1
    homework = Homework(
        "Text of the homework", timedelta(days=the_deadline_is_yesterday)
    )

    assert homework.is_active() is False


def test_student_did_homework_in_time():
    teacher = Teacher("Daniil", "Shadrin")
    student = Student("Roman", "Petrov")
    oop_homework = teacher.create_homework("create 2 simple classes", 5)

    assert student.do_homework(oop_homework) == oop_homework


def test_student_mess_with_hw(capsys):
    teacher = Teacher("Daniil", "Shadrin")
    student = Student("Roman", "Petrov")
    oop_homework = teacher.create_homework("create 2 simple classes", 0)

    performed_hw = student.do_homework(oop_homework)
    stdout, err = capsys.readouterr()

    assert performed_hw is None
    assert err == ""
    assert stdout == "You are late\n"
