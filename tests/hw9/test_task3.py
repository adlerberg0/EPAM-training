from hw9.task3 import universal_file_counter


class TestClass:
    def test_cnt_simple_file_without_tokenizer(self, tmp_path):
        amount_of_lines = 100
        with (tmp_path / "new_file1.txt").open("w") as f:
            f.write("\n".join(str(i) for i in range(amount_of_lines)))
        with (tmp_path / "new_file2.txt").open("w") as f:
            f.write("\n".join(str(i) for i in range(amount_of_lines)))

        assert universal_file_counter(tmp_path, ".txt") == amount_of_lines * 2

    def test_cnt_items_in_nested_dir_without_tokenizer(self, tmp_path):
        amount_of_lines = 100
        (tmp_path / "tmp1").mkdir()
        with open(tmp_path / "tmp1/new_file3.txt", "w") as f:
            f.write("\n".join(str(i) for i in range(amount_of_lines)))
        (tmp_path / "tmp2").mkdir()
        with open(tmp_path / "tmp2/new_file4.txt", "w") as f:
            f.write("\n".join(str(i) for i in range(amount_of_lines)))

        assert universal_file_counter(tmp_path, ".txt") == amount_of_lines * 2

    def test_cnt_simple_file_with_tokenizer(self, tmp_path):
        amount_of_lines = 100
        with (tmp_path / "new_file1.txt").open("w") as f:
            f.write("\n".join(f"{i} {i}" for i in range(amount_of_lines)))
        with (tmp_path / "new_file2.txt").open("w") as f:
            f.write("\n".join(f"{i} {i}" for i in range(amount_of_lines)))

        assert (
            universal_file_counter(tmp_path, ".txt", lambda string: string.split())
            == amount_of_lines * 4
        )

    def test_cnt_simple_file_with_unique_tokenizer(self, tmp_path):
        amount_of_lines = 100
        with (tmp_path / "new_file1.txt").open("w") as f:
            f.write("\n".join(f"{i}.{i}" for i in range(amount_of_lines)))
        with (tmp_path / "new_file2.txt").open("w") as f:
            f.write("\n".join(f"{i}.{i}" for i in range(amount_of_lines)))

        assert (
            universal_file_counter(tmp_path, ".txt", lambda string: string.split("."))
            == amount_of_lines * 4
        )

    def test_cnt_file_with_empty_lines(self, tmp_path):
        amount_of_lines = 100
        with (tmp_path / "new_file1.txt").open("w") as f:
            f.write("\n".join("" for _ in range(amount_of_lines)))
        with (tmp_path / "new_file2.txt").open("w") as f:
            f.write("\n".join("" for _ in range(amount_of_lines)))

        assert universal_file_counter(tmp_path, ".txt") == 0
