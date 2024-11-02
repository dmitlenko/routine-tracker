from django_components import Component, register
from django_components.attributes import attributes_to_string

from routine_tracker.core.components.table.table import get_table_data


@register("column-header")
class TableColumnHeaderComponent(Component):
    template = """
    <th scope="col" {{ attrs }}>
        {% slot "content" default %}
            {{ value }}
        {% endslot %}
    </th>
    """

    def get_context_data(self, name: str, sort: bool = False, value: str = "", **kwargs):
        table_data = get_table_data(self)

        if name not in table_data["columns"]:
            raise ValueError(f"Column {name} not found in table columns")

        return {
            "name": name,
            "sort": sort,
            "value": value,
            "attrs": attributes_to_string(kwargs),
        }
