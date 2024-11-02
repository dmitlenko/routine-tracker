from typing import Any, List, TypedDict

from django_components import Component, register
from django_components.attributes import attributes_to_string

from routine_tracker.core.utils.components import dep_dict


class RowData(TypedDict):
    object: Any
    index: int


class TableData(TypedDict):
    rows: List[RowData]
    columns: List[str]
    id: str


def get_table_data(self: Component) -> TableData:
    data = self.inject("table_data", None)

    if data is None:
        raise ValueError(f"Component {self.name} should only be used inside a table component")

    return dep_dict(data)


def get_row_data(self: Component) -> RowData:
    data = self.inject("row_data", None)

    if data is None:
        raise ValueError(f"Component {self.name} should only be used inside a table table component")

    return dep_dict(data)


@register("table")
class TableComponent(Component):
    template_name = "table/table.html"

    def get_context_data(self, rows: List[Any], columns: List[str], **kwargs):
        if "id" not in kwargs:
            raise ValueError("Table component requires an id attribute")

        classes = kwargs.pop("class", "")

        table_data: TableData = {
            "rows": [
                {
                    "object": obj,
                    "index": i,
                }
                for i, obj in enumerate(rows)
            ],
            "columns": columns.split(","),
            "id": kwargs["id"],
        }

        return {
            "attrs": attributes_to_string(kwargs),
            "table_data": table_data,
            "classes": classes,
        }

    class Media:
        js = "script.js"
