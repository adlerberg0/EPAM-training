"""
please create your own git repository on github.
setup pre-commit hook with black and isort formatting for the repo
initialize .gitignore in the repository root (you can use this sample)
create a homework1 directory in the repo
then copy the hw1 into the directory.
fix all bugs in the hw1 code
write an extra test for each found bug
Note: as we said, any hw, which does not pass
 isort --profile black --check and black --check, will be rejected
"""


def check_power_of_2(a: int) -> bool:
    return not (bool(a & (a - 1))) and a != 0
