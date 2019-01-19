from sagas.crmsfa.odoo_facade import odoo, login
import graphene
from odoorpc.fields import Many2many, Many2one, One2many, Unknown
import json

TYPES_TO_FIELDS = {
    'binary': graphene.String,
    'boolean': graphene.Boolean,
    'char': graphene.String,
    'date': graphene.types.datetime.Date,
    'datetime': graphene.types.datetime.DateTime,
    'float': graphene.Float,
    'html': graphene.String,
    'integer': graphene.Int,

    # ⊕ [Graphene-Python](http://docs.graphene-python.org/en/latest/types/scalars/#custom-scalars)
    'many2many': Many2many,
    'many2one': Many2one,
    'one2many': One2many,

    'reference': graphene.String,
    'selection': graphene.String,
    'text': graphene.String,
}


def generate_field(name, data):
    """Generate a well-typed field according to the data dictionary supplied
    (obtained via the `fields_get' method of any models).
    """
    assert 'type' in data
    field = TYPES_TO_FIELDS.get(data['type'], Unknown)()
    return field

def to_camel_case(snake_str):
    components = snake_str.split("_")
    # We capitalize the first letter of each component except the first one
    # with the 'capitalize' method and join them together.
    return "".join(x.capitalize() if x else "_" for x in components[:])

def normalize_class(model):
    cls_name = model.replace('.', '_')
    return to_camel_case(cls_name)


from odoorpc.env import FIELDS_RESERVED
import odoorpc.fields as fields

model = "calendar.event"
attrs = {
    '_name': model,
    '_columns': {},
}

def get_recurrent_fields():
    return ['byday', 'recurrency', 'final_date', 'rrule_type', 'month_by',
            'interval', 'count', 'end_type', 'mo', 'tu', 'we', 'th', 'fr', 'sa',
            'su', 'day', 'week_list']

login()
fields_get = odoo.execute(model, 'fields_get')
for field_name, field_data in fields_get.items():
    field_type = field_data['type']
    if field_name not in FIELDS_RESERVED and \
            field_name not in get_recurrent_fields() and \
            not field_name.startswith("_") and \
            field_type not in ("many2many", "many2one", "one2many"):
        Field = fields.generate_field(field_name, field_data)
        FieldType = generate_field(field_name, field_data)
        attrs['_columns'][field_name] = Field
        attrs[field_name] = FieldType
        print(field_name, type(FieldType))

cls_name = normalize_class(model)
print(".. create class", cls_name)
model_cls = type(cls_name, (graphene.ObjectType,), attrs)

import graphene


def create_with_attrs(model_cls, record):
    inst = model_cls()
    for fld in model_cls._columns.keys():
        val = getattr(record, fld)
        setattr(inst, fld, val)
    return inst


model_name = "calendar.event"
of_type = model_cls


class CalQuery(graphene.ObjectType):
    calendar_event = graphene.List(of_type)

    def resolve_calendar_event(self, info):
        Model = odoo.env[model_name]
        model_ids = Model.search([])
        recordset = []
        for record in Model.browse(model_ids):
            recordset.append(create_with_attrs(of_type, record))
        return recordset


schema = graphene.Schema(query=CalQuery)

default_query = '''
{
  calendarEvent {
    name
    description
    start
    stop
  }
}
'''.strip()

if __name__ == '__main__':
    result = schema.execute(default_query)
    print(json.dumps(result.data, indent=2, ensure_ascii=False))

