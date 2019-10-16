import io_utils
from sagas.ofbiz.services import OfService as s, MetaService
from sagas.ofbiz.entities import OfEntity as e, oc, finder, MetaEntity
import sagas.ofbiz.entities as ee
from sagas.util.str_converters import to_camel_case, to_snake_case
from py4j.java_gateway import get_field
from sagas.ofbiz.util import norm_loc

known_in_types={'String':'String',
                'java.sql.Date':'DateTime',
                'java.lang.String':'String',
                'java.sql.Time':'Duration',
                'java.sql.Timestamp':'DateTime',
                'Integer':'int',
                'Boolean':'bool',
                'java.lang.Boolean':'bool',
                'java.util.TimeZone':'String',
                'GenericPK':'Map<String,dynamic>',
                'Timestamp':'DateTime',
                 # 'java.nio.ByteBuffer',
                'java.math.BigDecimal':'Decimal',
                'byte[]':'Uint8List',
                'java.lang.Integer':'int',
                'GenericEntity':'Map<String,dynamic>',
                'GenericValue':'Map<String,dynamic>',
                'java.util.Locale':'String',
                'java.net.URL':'String',
                'BigDecimal':'Decimal',
                'Double':'double',
                'Long':'int',
                'org.apache.ofbiz.entity.GenericValue':'Map<String,dynamic>',

                # others types
                'java.io.File':'String',
                'java.util.Collection':'List<dynamic>',
                'java.util.List':'List<dynamic>',
                'List':'List<dynamic>',
                'java.util.Map':'Map<String,dynamic>'
               }

def get_mapping_type(par_type):
    if par_type in known_in_types:
        return known_in_types[par_type]
    raise ValueError('Cannot support parameter type '+par_type)

def is_regular_service(name):
    serv_model=oc.service_model(name)
    params=serv_model.getModelParamList()
    is_regular=True
    for param in params:
        internal = get_field(param, "internal")
        p_name = get_field(param, "name")
        # print(p_name, internal)
        if internal:
            pass
        elif get_field(param, 'mode')!='OUT':
            param_type=get_field(param, 'type')
            if param_type=='java.nio.ByteBuffer':
                print("service {} parameter {}'s type is ByteBuffer"
                     .format(name, p_name))
                is_regular=False
                break
            elif param_type not in known_in_types:
                is_regular=False
                break
    return is_regular

def get_all_regular_services(save_it=True):
    from ruamel.yaml import YAML
    yaml = YAML()

    services=oc.all_service_names()
    regular_services=[]
    for name in services:
        if is_regular_service(name):
            regular_services.append(name)

    if save_it:
        with open('.services.yml', 'w') as outfile:
            yaml.dump(services, outfile)
    return regular_services

def load_regular_services():
    from ruamel.yaml import YAML
    yaml = YAML()
    with open('.services.yml') as fp:
        str_data = fp.read()
    data = yaml.load(str_data)
    return data

package_header='''import 'package:decimal/decimal.dart';
import 'package:meta/meta.dart';
import 'package:sagas_meta/src/result_api.dart';
import 'package:sagas_meta/src/srv_api.dart';

class {package_name}{{
  final SrvClient client;
  {package_name}(this.client);
'''
package_footer="}"

def proc_special_fields(field_name):
    # login.username, login.password
    if field_name=="login.username":
        return "loginUserName"
    elif field_name=="login.password":
        return "loginPassword"
    return field_name

def gen_service_stub(lines, name):
    ms = MetaService(name)
    model = ms.model
    def_ent = get_field(model, 'defaultEntityName')
    ent_fields = []
    if def_ent != "":
        ent = oc.delegator.getModelEntity(def_ent)
        ent_fields = ent.getAllFieldNames()
    lines.append('  /**')
    lines.append('   * %s - %s' % (get_field(model, 'description'), def_ent))
    lines.append('   *')
    params = model.getModelParamList()

    invoke_pars = []
    return_pars = []
    define_pars = []
    requires = []
    params_set=set()

    # add schema as return value
    schema={'requires':[], 'returns':[], 'parameters':[]}

    invoke_ent = "null, "
    define_ent = ""
    if def_ent != "":
        define_ent = "{} {}, ".format(def_ent, 'ent')
        invoke_ent = 'ent, '
        schema['parameters'].append({'name': 'ent', 'type':def_ent})
    for param in params:
        mode = get_field(param, "mode")
        fldname = proc_special_fields(get_field(param, "name"))
        fldtype = get_field(param, "type")
        if not get_field(param, "internal"):
            if 'IN' in mode:
                required = not get_field(param, "optional")
                require_mark = ""
                if required:
                    requires.append(fldname)
                    require_mark = "@required "
                    schema['requires'].append({'name':fldname, 'type':get_mapping_type(fldtype)})
                # wrap entity fields into a entity parameter
                if fldname in ent_fields:
                    pass
                elif fldname in params_set:
                    pass
                else:
                    params_set.add(fldname)
                    invoke_pars.append("'{fld}': {fld}".format(fld=fldname))
                    fldtype_cast=get_mapping_type(fldtype)
                    define_pars.append("{mark}{type} {fld}"
                                       .format(fld=fldname,
                                               mark=require_mark,
                                               type=fldtype_cast))
                    schema['parameters'].append({'name': fldname, 'mark':require_mark, 'type':fldtype_cast})
            if 'OUT' in mode:
                return_pars.append("{fld}[{type}]".format(fld=fldname, type=fldtype))
                schema['returns'].append({'name':fldname, 'type':get_mapping_type(fldtype)})

    lines.append("   * Requires %s" % ', '.join(requires))
    lines.append("   * Returns %s" % ', '.join(return_pars))
    lines.append("   */")
    if len(define_pars)==0:
        lines.append("  Future<OfResult> %s(%s) =>" % (name, define_ent))
    else:
        lines.append("  Future<OfResult> %s(%s{%s}) =>" % (name, define_ent, ', '.join(define_pars)))
    lines.append("      client.invoke('{name}', {ent}{{ {invoke_pars} }});"
                 .format(name=name, ent=invoke_ent,
                         invoke_pars=', '.join(invoke_pars)))
    # lines.append('\n')
    return schema

def get_service_package(srv):
    serv_model = oc.service_model(srv)
    def_loc = get_field(serv_model, 'definitionLocation')
    return norm_loc(def_loc)

def get_service_groups():
    service_groups = {}
    services=load_regular_services()
    for srv in services:
        pkg = get_service_package(srv)
        if pkg in service_groups:
            grp = service_groups[pkg]
            grp.append(srv)
        else:
            service_groups[pkg] = [srv]
    return service_groups

def get_entity_package_def(entity_name):
    from sagas.ofbiz.entity_gen import norm_package
    model = oc.delegator.getModelEntity(entity_name)
    return norm_package(model.getPackageName())

def proc_service_refs(serv_name, deps):
    model_serv = oc.service_model(serv_name)
    def_ent = get_field(model_serv, 'defaultEntityName')
    if def_ent != "":
        ent_pkg=get_entity_package_def(def_ent)
        deps.add(ent_pkg)

def gen_services(group_name, srvs, target_file):
    deps = set()
    for srv in srvs:
        proc_service_refs(srv, deps)

    lines = []
    for dep in deps:
        lines.append("import 'package:sagas_meta/src/models/%s.dart';" % dep)

    lines.append(package_header.format(package_name=to_camel_case(group_name, True)))

    for service in srvs:
        gen_service_stub(lines, service)
        lines.append('')

    lines.append(package_footer)
    cnt = "\n".join(lines)
    io_utils.write_to_file(target_file, cnt)

class ServiceGenerator(object):
    def gen_samples(self):
        import clipboard

        package_name = 'common_srv'
        lines = []
        lines.append(package_header.format(package_name=to_camel_case(package_name, True)))

        services = ["testScv", 'createPerson', 'quickAddVariant']
        for service in services:
            gen_service_stub(lines, service)
            lines.append('')

        lines.append(package_footer)

        print("\n".join(lines))
        clipboard.copy("\n".join(lines))

    def gen_sample_group(self, group_name, target_dir):
        pkg_file = group_name + ".dart"
        target_file = target_dir + '/' + pkg_file

        service_groups=get_service_groups()
        srvs = service_groups[group_name]
        gen_services(group_name, srvs, target_file)

    def gen_sample_groups(self, target_dir):
        service_groups = get_service_groups()
        for group_name,srvs in service_groups.items():
            print('proc group', group_name)
            pkg_file = group_name + ".dart"
            target_file = target_dir + '/' + pkg_file
            gen_services(group_name, srvs, target_file)

if __name__ == '__main__':
    import fire
    fire.Fire(ServiceGenerator)
