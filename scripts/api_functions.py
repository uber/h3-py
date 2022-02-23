from pathlib import Path
from typing import List

from h3.api.basic_int import basic_int

APIS = ["basic_int", "basic_str", "memview_int", "numpy_int"]

SEPARATOR_TEXT = """\
###############################
# Automatically generated API
# Do not edit below these lines
###############################
"""


def create_api_binding(api_name: str) -> List[str]:
    """Formulate API bindings to paste into API files

    Args:
        api_name: should be one of 'basic_int', 'basic_str', 'memview_int', 'numpy_int'

    Returns:

        List of lines to create public API bindings, i.e.:

            string_to_h3 = basic_int.string_to_h3
    """
    # Use introspection in the basic_int instance of _API_FUNCTIONS
    public_method_names = sorted(
        [name for name in dir(basic_int) if not name.startswith("_")]
    )

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
    for api_name in APIS:
        api_path = h3_root / f"src/h3/api/{api_name}.py"
        api_binding = create_api_binding(api_name)
        write_api(api_path=api_path, api_binding=api_binding)


if __name__ == "__main__":
    main()
