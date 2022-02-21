import re
from pathlib import Path
from typing import List

APIS = ["basic_int", "basic_str", "memview_int", "numpy_int"]

SEPARATOR_TEXT = """\
###############################
# Automatically generated API
# Do not edit below these lines
###############################
"""


def read_api(api_template_path: Path) -> List[str]:
    """Read public API from _api_template.py"""
    with open(api_template_path) as f:
        lines = f.readlines()

    # Methods within _API_FUNCTIONS class
    method_lines = [line for line in lines if line.startswith("    def")]

    # Names of methods (strip `def`)
    method_names = []
    for line in method_lines:
        match = re.match(r"    def (\w+)\(", line)
        assert match, "Could not match function definition"
        method_names.append(match.group(1))

    # Public methods (remove `__init__`)
    public_method_names = [name for name in method_names if not name.startswith("_")]

    return public_method_names


def create_api_binding(api_name: str, public_method_names: List[str]) -> List[str]:
    """Formulate API bindings to paste into API files

    Args:
        api_name: should be one of 'basic_int', 'basic_str', 'memview_int', 'numpy_int'
        public_method_names: list of method names to export

    Returns:

        List of lines to create public API bindings, i.e.:

            string_to_h3 = basic_int.string_to_h3
    """
    return [
        f"{method_name} = {api_name}.{method_name}"
        for method_name in public_method_names
    ]


def find_separator_text(lines: List[str]) -> int:
    separator_lines = SEPARATOR_TEXT.splitlines()
    n_separator_lines = len(separator_lines)

    for i in range(len(lines)):
        if lines[i : i + n_separator_lines] == separator_lines:
            return i + n_separator_lines

    raise ValueError("Did not find separator text")


def write_api(api_path: Path, api_binding: List[str]) -> None:
    """Write API binding to file"""

    with open(api_path) as f:
        lines = [line.rstrip() for line in f.readlines()]

    start_api_line_num = find_separator_text(lines)
    full_lines = lines[:start_api_line_num] + [""] + api_binding
    full_text = "\n".join([line.rstrip() for line in full_lines]) + "\n"

    with open(api_path, "w") as f:
        f.write(full_text)


def main(h3_root: Path = Path(".")) -> None:
    api_template_path = h3_root / "src/h3/api/_api_template.py"
    public_method_names = read_api(api_template_path)

    for api_name in APIS:
        api_path = h3_root / f"src/h3/api/{api_name}.py"
        api_binding = create_api_binding(api_name, public_method_names)
        write_api(api_path=api_path, api_binding=api_binding)


if __name__ == "__main__":
    main()
