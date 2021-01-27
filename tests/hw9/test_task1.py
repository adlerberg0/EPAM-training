import pytest

from hw9.task1 import merge_sorted_files


class TestClass:
    # scope=class doesn't work ¯\_(ツ)_/¯, also I can't use tmp_dir with scope=class because of scope conflict
    @pytest.fixture(scope="function", autouse=True)
    def create_instance(self, tmpdir_factory):
        tmp_path = tmpdir_factory.getbasetemp()
        self.amount_of_lines = 100
        self.file1_path = tmp_path / "new_file1.txt"
        self.file2_path = tmp_path / "new_file2.txt"
        # create 2 files with nums from X = {x ∈ N: 1≤x≤100 }
        with (tmp_path / "new_file1.txt").open("w") as f:
            f.write(
                "\n".join(
                    str(i) for i in range(self.amount_of_lines, 0, -1) if i % 2 == 0
                )
            )
        with (tmp_path / "new_file2.txt").open("w") as f:
            f.write(
                "\n".join(
                    str(i) for i in range(self.amount_of_lines, 0, -1) if i % 2 != 0
                )
            )

    def test_merge_func(self):
        # check whether result list is sorted and contains nums from X = {x ∈ N: 1≤x≤100 }
        assert list(merge_sorted_files([self.file1_path, self.file2_path])) == list(
            i for i in range(1, self.amount_of_lines + 1)
        )
