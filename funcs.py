import calendar
from datetime import datetime as dt

def convert_int_to_month_name(month_int: int) -> str:
    return calendar.month_name[month_int]

def use_existing_or_interpolate(df_row):
    if dt.now().month == df_row.month:
        return "hooray"
    else:
        return "mehhh"

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