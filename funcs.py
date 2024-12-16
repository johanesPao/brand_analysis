def in_sql_concatenation(values: str | int | list[str] | list[int]):
    match values:
        case list() as lst:
            if all(isinstance(item, str) for item in lst):
                return f"({','.join(f"'{value}'" for value in values)})"
            else:
                return f"({','.join(f"{value}" for value in values)})"
        case str():
            return f"('{values}')"
        case int():
            return f"({values})"
        case _:
            return "Uh oh errors!"