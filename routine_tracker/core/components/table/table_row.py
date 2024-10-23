from django.template import Context
from django.template.base import Template
from django_components import Component, register
from django_components.attributes import attributes_to_string

from routine_tracker.core.components.table.table import get_row_data, get_table_data


@register('table-row')
class TableRowComponent(Component):

    def get_template(self, context: Context) -> str | Template | None:
        """
        This shitload of code is workaround for slot error:  Slot tag kwarg 'name' is...

        Instead of using the html template and using for loop inside the template, we are generating the template
        dynamically here.
        """

        table_data = get_table_data(self)
        columns = table_data['columns']
        attrs = context['attrs']
        last = context['last']

        slots = ''.join(map(lambda column: self.get_cell(context, column), columns))

        return f"<tr {attrs} {{% if forloop.last %}}{last}{{% endif %}}>{slots}</tr>"

    def get_cell(self, context: Context, column: str) -> str:
        col_attrs = context.get('col_attrs', {})
        cell_attrs = self.get_cell_attributes(col_attrs, column)
        cell_attrs_str = attributes_to_string(cell_attrs)

        return f"<td {cell_attrs_str}>{{% slot '{column}' ...row %}}{{% endslot %}}</td>"

    def get_cell_attributes(self, column_attributes: dict, column: str) -> dict:
        return {key[len(column) + 1 :]: value for key, value in column_attributes.items() if key.startswith(column)}

    def get_context_data(self, **kwargs):
        row_data = get_row_data(self)
        table_data = get_table_data(self)
        col_attrs = kwargs.pop('col', {})
        last_row_attrs = kwargs.pop('last', {})

        return {
            'row': row_data,
            'columns': table_data['columns'],
            'attrs': attributes_to_string(kwargs),
            'last': attributes_to_string(last_row_attrs),
            'col_attrs': col_attrs,
        }
