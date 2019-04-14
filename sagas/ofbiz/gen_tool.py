import re
import json

class GenProp(object):
    def __init__(self, prop_type, prop_name):
        self.prop_type=prop_type
        self.prop_name=prop_name
class GenCollection(object):
    def __init__(self, collection_type, element_type, prop_name):
        self.prop_name=prop_name
        self.collection_type=collection_type
        self.element_type=element_type
class GenMeta(object):
    def __init__(self):
        self.class_name=''
        self.base_name=''
        self.attributes=[]


def analyse(code):
    meta = GenMeta()
    for line in code.splitlines():
        # print(line)
        match_obj = re.match(r'class (.*) extends (.*) {', line, re.M | re.I)
        if match_obj:
            print("@class", match_obj.group(1), "*", match_obj.group(2))
            meta.class_name = match_obj.group(1)
            meta.base_name = match_obj.group(2)
        else:
            pass

        match_obj = re.match(r'\s*([a-zA-Z_][a-zA-Z_0-9]*)\s*([a-zA-Z_][a-zA-Z_0-9]*)\s*=(.*);', line, re.M | re.I)
        # match_obj=re.search(r'([a-zA-Z_]+) ([a-zA-Z_]+) = ([a-zA-Z_]+);', line)
        if match_obj:
            print("@prop", match_obj.group(1), '*', match_obj.group(2))
            meta.attributes.append(GenProp(match_obj.group(1), match_obj.group(2)))
        else:
            pass

        # process collections
        match_obj = re.match(r'\s*([a-zA-Z_][a-zA-Z_0-9]*)<(.*)>\s*([a-zA-Z_][a-zA-Z_0-9]*)\s*=(.*);', line, re.M | re.I)
        if match_obj:
            print("@collection", match_obj.group(1), "-", match_obj.group(2), match_obj.group(3))
            meta.attributes.append(GenCollection(match_obj.group(1), match_obj.group(2), match_obj.group(3)))
        else:
            pass
    return meta

from json import JSONEncoder
class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

def dump(meta):
    jd = json.dumps(meta, cls=MyEncoder, indent=2)
    print(jd)

def gen_constructor(meta):
    lines=[]
    lines.append('  %s({'%meta.class_name)
    attr_defs=[]
    attr_equals=[]
    for attr in meta.attributes:
        attr_defs.append('this.%s'%attr.prop_name)
        attr_equals.append(attr.prop_name)
    lines.append('    '+', '.join(attr_defs))
    lines.append('  }) : super([')
    lines.append('    '+', '.join(attr_equals))
    lines.append('  ]);')
    return ('\n'.join(lines))

def gen_overrides(meta):
    lines = []
    lines.append('  static %s overrides%s(Map<String, dynamic> map) {' % (meta.class_name, meta.class_name))
    lines.append('    return %s(' % meta.class_name)
    setters = []
    for attr in meta.attributes:
        setters.append("        %s: map['%s']" % (attr.prop_name, attr.prop_name))
    lines.append(",\n".join(setters))
    lines.append('    );')
    lines.append('  }')
    return('\n'.join(lines))

def gen_as_map(meta):
    lines = []
    lines.append('  Map<String, dynamic> asMap() {')
    setters = []
    for attr in meta.attributes:
        setters.append("'%s':%s" % (attr.prop_name, attr.prop_name))
    lines.append("    return {%s};" % (', '.join(setters)))
    lines.append('  }')
    return('\n'.join(lines))

## generate dss model
def analyse_dss_class(code):
    meta = GenMeta()
    prefix = "Dss"
    for line in code.splitlines():
        # print(line)
        match_obj = re.match(r'class (.*) {', line, re.M | re.I)
        if match_obj:
            print("@class", match_obj.group(1))
            meta.class_name = prefix + match_obj.group(1)
        else:
            pass

        match_obj = re.match(r'\s*(var|final)?\s*([a-zA-Z_][a-zA-Z_0-9]*)\s*([a-zA-Z_][a-zA-Z_0-9]*)\s*(.*);', line,
                             re.M | re.I)
        # match_obj=re.search(r'([a-zA-Z_]+) ([a-zA-Z_]+) = ([a-zA-Z_]+);', line)
        if match_obj:
            print("@prop", match_obj.group(2), '*', match_obj.group(3))
            meta.attributes.append(GenProp(match_obj.group(2), match_obj.group(3)))
        else:
            pass

        # process collections
        match_obj = re.match(r'\s*([a-zA-Z_][a-zA-Z_0-9]*)<(.*)>\s*([a-zA-Z_][a-zA-Z_0-9]*)\s*=(.*);', line,
                             re.M | re.I)
        if match_obj:
            print("@collection", match_obj.group(1), "-", match_obj.group(2), match_obj.group(3))
            meta.attributes.append(GenCollection(match_obj.group(1), match_obj.group(2), match_obj.group(3)))
        else:
            pass
    return meta

type_mappings = {"String": "description",
                 "int":"numeric",
                 "double":"floating-point",
                 "DateTime":"date-time",
                 "Uint8List":"byte-array"}

def get_mapping_type(field_type):
    if field_type not in type_mappings:
        raise ValueError("Cannot find mapping type for " + field_type)
    return type_mappings[field_type]

lower_first = lambda s: s[:1].lower() + s[1:] if s else ''
def gen_dss_entity(meta):
    from sagas.util.str_converters import to_snake_case, to_words
    # print(to_words(to_snake_case('LinearSales'), True))
    lines = []
    entity_title = to_words(to_snake_case(meta.class_name), True)
    lines.append('    <entity entity-name="{name}" package-name="com.sagas.dss" title="{title}">'.format(
        name=meta.class_name, title=entity_title))
    for attr in meta.attributes:
        lines.append('      <field name="%s" type="%s"></field>' % (attr.prop_name, get_mapping_type(attr.prop_type)))
    # add the primary key
    prim = lower_first(meta.class_name) + "Id"
    lines.append('      <field name="%s" type="id"></field>' % prim)
    lines.append('      <prim-key field="%s"/>' % prim)
    lines.append('    </entity>')

    return('\n'.join(lines))

class GenTool(object):
    def gen_model_cls(self):
        """
        Code format:
        ```
        class Schedule extends Equatable {
          DateTime fromDate= DateTime.now();
          TimeOfDay fromTime = const TimeOfDay(hour: 7, minute: 28);
          DateTime toDate = DateTime.now();
          TimeOfDay toTime = const TimeOfDay(hour: 7, minute: 28);
          // final List<String> allActivities = <String>['hiking', 'swimming', 'boating', 'fishing'];
          List<String> allActivities= <String>['hiking', 'swimming'];
          String activity = 'fishing';
        ```

        Generate result:
        ```
          Schedule({
            this.fromDate, this.fromTime, this.toDate, this.toTime, this.allActivities, this.activity
          }) : super([
            fromDate, fromTime, toDate, toTime, allActivities, activity
          ]);

          static Schedule overridesSchedule(Map<String, dynamic> map) {
            return Schedule(
                fromDate: map['fromDate'],
                fromTime: map['fromTime'],
                toDate: map['toDate'],
                toTime: map['toTime'],
                allActivities: map['allActivities'],
                activity: map['activity']
            );
          }

          Map<String, dynamic> asMap() {
            return {'fromDate':fromDate, 'fromTime':fromTime, 'toDate':toDate, 'toTime':toTime, 'allActivities':allActivities, 'activity':activity};
          }
        ```
        :return:
        """
        import clipboard
        sett = clipboard.paste()
        meta=analyse(sett)
        lines=[]
        lines.append(gen_constructor(meta))
        lines.append(gen_overrides(meta))
        lines.append(gen_as_map(meta))
        cnt='\n\n'.join(lines)
        print('---------------------- ✁')
        print(cnt)
        clipboard.copy(cnt)
        print('done.')

    def gen_dss_model(self):
        """
        Process clipboard code:
        ```
        class LinearSales {
          final int year;
          final int sales;
        ```

        Generate result:
        ```xml
        <entity entity-name="DssOrdinalSales" package-name="com.sagas.dss" title="Dss Ordinal Sales">
            <field name="year" type="description"></field>
            <field name="sales" type="numeric"></field>
            <field name="dssOrdinalSalesId" type="id"></field>
            <prim-key field="dssOrdinalSalesId"/>
        </entity>
        ```
        :return:
        """
        import clipboard
        sett = clipboard.paste()
        meta = analyse_dss_class(sett)
        cnt=gen_dss_entity(meta)
        print(cnt)
        clipboard.copy(cnt)
        print('done.')

if __name__ == '__main__':
    import fire
    fire.Fire(GenTool)

