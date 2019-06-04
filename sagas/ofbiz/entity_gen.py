from sagas.ofbiz.services import OfService as s, oc, track
from sagas.ofbiz.entities import OfEntity as e, get_package_entities
from sagas.ofbiz.date_time import DateTime
from sagas.util.str_converters import to_camel_case, to_snake_case

type_mappings = {"string": ["object",
                            "id", "id-long", "id-vlong",
                            "indicator", "very-short", "short-varchar", "long-varchar", "very-long",
                            "comment", "description", "name", "value",
                            "credit-card-number", "credit-card-date", "email", "url", "tel-number"],
                 "float": ["currency-amount", "currency-precise", "fixed-point", "floating-point"],
                 "date": ["date-time", "date"],
                 "time": ["time"],
                 "bytes": ["byte-array", "blob"],
                 "int": ["numeric"]}
gl_mappings = {"string": "String",
               "float": "double", "int": "int",
               "date": "DateTime",
               "time": "DateTime",
               "bytes": "Uint8List"
               }
dgraph_mappings = {"string": "string",
               "float": "float",
               "int": "int",
               "date": "datetime",
               "time": "datetime",
               "bytes": "string"
               }

def get_mapping_type(field_type):
    for k, v in type_mappings.items():
        if field_type in v:
            return k
    raise ValueError("Cannot find mapping type for " + field_type)


def get_dart_type(field_type):
    mt = get_mapping_type(field_type)
    return gl_mappings[mt]

def get_dgraph_type(field_type):
    mt = get_mapping_type(field_type)
    return dgraph_mappings[mt]

package_header='''import 'dart:typed_data';
import 'package:meta/meta.dart';
import 'package:sagas_meta/src/entity_base.dart';'''
entity_header='''
/// Entity {entity}, {title}
class {entity} extends EntityBase {{
'''
entity_footer='''    lastUpdatedStamp,
    createdStamp}) : super(entityId, lastUpdatedStamp, createdStamp);

  @override
  String toString() => '%s { id: $entityId }';
'''
entity_to_map='''  @override
  Map<String, dynamic> asMap() {
    return {%s};
  }
'''
end_mark="}"

def gen_bloc_model(lines, entity_name):
    ent = oc.delegator.getModelEntity(entity_name)
    lines.append(entity_header.format(
        entity=entity_name,
        title=ent.getTitle()
    ))
    pk_size=ent.getPksSize()
    if pk_size==1:
        lines.append("  /// this entity has only one pk")
    names = ent.getAllFieldNames()
    field_setters=[]
    field_map=[]
    for field_name in names:
        fld = ent.getField(field_name)
        fix_name = fix_field_name(field_name)
        if not fld.getIsAutoCreatedInternal():
            fldtype=get_dart_type(fld.getType())
            require_mark=""
            comment=""
            if fld.getIsPk():
                require_mark="@required "
                comment=" // pk"
            field_setters.append('%sthis.%s'%(require_mark, fix_name))
            field_map.append("'{name}':{fix_name}".format(name=field_name, fix_name=fix_name))
            lines.append('  final {type} {fix_name};{comment}'.format(
                name=field_name,
                fix_name=fix_name,
                comment=comment,
                type=fldtype))

    lines.append('  %s({entityId,'%entity_name)
    lines.append('    %s,'%', '.join(field_setters))
    lines.append(entity_footer%entity_name)
    lines.append(entity_to_map%', '.join(field_map))
    lines.append(end_mark)

def get_id_list(entity_name):
    ent = oc.delegator.getModelEntity(entity_name)
    names=ent.getPkFieldNames()
    flds=[]
    for pk in names:
        flds.append("'%s'"%pk)
    return(', '.join(flds))

imports='''import 'package:sagas_meta/src/entity_base.dart';
import 'dart:convert';
import 'dart:typed_data';
import 'package:intl/intl.dart';
'''
default_fields='''        lastUpdatedStamp: check_dt(json['lastUpdatedStamp']),
        createdStamp: check_dt(json['createdStamp']));'''
id_field='''        entityId: create_id_from('{entity}', [{id_list}], json),'''

entity_json_header='''  static {entity} extract{entity}(dynamic json) {{
    return {entity}('''
field_def='''        {fix_name}: json['{name}'] as {type},'''
date_time_def='''        {name}: check_dt(json['{name}']),'''
time_def='''        {name}: check_time(json['{name}']),'''
bytes_def='''        {name}: check_b64(json['{name}']),'''
field_setter_mappings={"string":field_def,
                     "float":field_def,
                     "int":field_def,
                     "date":date_time_def,
                     "time":time_def,
                     "bytes":bytes_def
                    }


def fix_field_name(field_name):
    if field_name=="toString":
        return "toStr"
    return field_name

def gen_bloc_jsonifier(lines, entity_name):
    ent = oc.delegator.getModelEntity(entity_name)
    lines.append(entity_json_header.format(entity=entity_name))
    lines.append(id_field.format(entity=entity_name, id_list=get_id_list(entity_name)))
    names = ent.getAllFieldNames()
    field_setters=[]
    for field_name in names:
        fld = ent.getField(field_name)
        if not fld.getIsAutoCreatedInternal():
            fldtype=get_dart_type(fld.getType())
            mapping_type=get_mapping_type(fld.getType())
            setter=field_setter_mappings[mapping_type]
            # print()
            lines.append(setter.format(name=field_name,
                                       fix_name=fix_field_name(field_name),
                                       type=fldtype))
    lines.append(default_fields)
    lines.append('  }\n')


## +add map support, at 2019.2.25
entity_map_header='''  static {entity} overrides{entity}(Map<String, dynamic> map) {{
    return {entity}('''
field_map_def='''        {fix_name}: map['{name}'],'''
default_map_fields='''        lastUpdatedStamp: map['lastUpdatedStamp'],
        createdStamp: map['createdStamp']);'''
id_map_field='''        entityId: create_id_from('{entity}', [{id_list}], map),'''

def gen_map_overrides(lines, entity_name):
    ent = oc.delegator.getModelEntity(entity_name)
    lines.append(entity_map_header.format(entity=entity_name))
    # id field setter
    lines.append(id_map_field.format(entity=entity_name, id_list=get_id_list(entity_name)))
    names = ent.getAllFieldNames()
    for field_name in names:
        fld = ent.getField(field_name)
        if not fld.getIsAutoCreatedInternal():
            # print()
            lines.append(field_map_def.format(name=field_name,
                                       fix_name=fix_field_name(field_name)
                                       ))
    # default fields setters
    lines.append(default_map_fields)
    lines.append('  }\n')

def norm_package(pkg):
    if pkg.startswith('com.'):
        return pkg[4:].replace('.','_')
    else:
        return pkg.replace('org.apache.ofbiz.', '').replace('org.ofbiz.','').replace('.','_')

class EntityGenerator(object):
    def gen_samples(self):
        import clipboard
        lines = []
        lines.append(package_header)
        entities = ['Testing', 'TestingType', 'TestFieldType', 'Person']
        for entity_name in entities:
            # entity_name='TestFieldType'
            gen_bloc_model(lines, entity_name)

        print("\n".join(lines))
        clipboard.copy("\n".join(lines))

    def gen_sample_jsonifiers(self):
        import clipboard
        package_name = 'testing'
        lines = []
        lines.append(imports)
        lines.append('class %sEntityJsonifier{' % to_camel_case(package_name, True))

        entities = ['Testing', 'TestingType', 'TestFieldType', 'Person']
        for entity in entities:
            gen_bloc_jsonifier(lines, entity)
            gen_map_overrides(lines, entity)

        # end package
        lines.append('}')
        print("\n".join(lines))
        clipboard.copy("\n".join(lines))

    def gen_package(self, pkg, target_dir):
        import io_utils
        entities=get_package_entities(pkg)
        if len(entities)>0:
            pkg_file=norm_package(pkg)+".dart"
            target_file=target_dir+'/'+pkg_file

            lines = []
            lines.append(package_header)
            for entity_name in entities:
                print('.. generate', entity_name)
                # entity_name='TestFieldType'
                gen_bloc_model(lines, entity_name)

            cnt=("\n".join(lines))

            io_utils.write_to_file(target_file, cnt)
            print('done.')
        else:
            print("package %s doesn't has entities.")

    def gen_packages(self, target_dir):
        model_reader = oc.delegator.getModelReader()
        tree_map = model_reader.getEntitiesByPackage(None, None)
        print('total packages:', len(tree_map))
        for k, v in tree_map.items():
            print(norm_package(k), '➼', k)
            self.gen_package(k, target_dir)

    def gen_jsonifier(self, pkg, target_dir):
        import io_utils
        entities=get_package_entities(pkg)
        if len(entities)>0:
            norm_pkg=norm_package(pkg)
            pkg_file=norm_pkg+"_jsonifiers.dart"
            target_file=target_dir+'/'+pkg_file

            package_name = to_camel_case(norm_pkg, True)
            lines = []
            # import 'package:sagas_meta/src/models/product_subscription.dart';
            lines.append("import 'package:sagas_meta/src/models/%s.dart';"%norm_pkg)
            lines.append(imports)

            lines.append('class %sJsonifier{' % package_name)

            for entity_name in entities:
                print('.. generate', entity_name)
                gen_bloc_jsonifier(lines, entity_name)
                gen_map_overrides(lines, entity_name)

            lines.append('}')
            cnt=("\n".join(lines))

            io_utils.write_to_file(target_file, cnt)
            print('done.')
        else:
            print("package %s doesn't has entities.")

    def gen_jsonifiers(self, target_dir):
        model_reader = oc.delegator.getModelReader()
        tree_map = model_reader.getEntitiesByPackage(None, None)
        print('total packages:', len(tree_map))
        for k, v in tree_map.items():
            print(norm_package(k), '➼', k)
            self.gen_jsonifier(k, target_dir)

if __name__ == '__main__':
    import fire
    fire.Fire(EntityGenerator)



