import re


def camel_to_snake(name: str):
    """Transform `name` from CamelCase to snake_case"""
    # cf. https://stackoverflow.com/a/1176023
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()
