from hw7.hw1 import find_occurrences

# Example tree:
example_tree = {
    "first": ["RED", "BLUE"],
    "second": {
        "simple_key": ["simple", "list", "of", "RED", "valued"],
    },
    "third": {
        "abc": "BLUE",
        "jhl": "RED",
        "complex_key": {
            "key1": "value1",
            "key2": "RED",
            "key3": ["a", "lot", "of", "values", {"nested_key": "RED"}],
        },
    },
    "fourth": "RED",
}


def test_find_occurrence_for_simple_entity():
    assert find_occurrences(example_tree, "RED") == 6


def test_find_occurrence_for_list():
    assert find_occurrences(example_tree, ["RED", "BLUE"]) == 1


def test_find_occurrence_for_complicated_structure():
    assert (
        find_occurrences(example_tree, ["simple", "list", "of", "RED", "valued"]) == 1
    )
