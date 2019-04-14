from sagas.ofbiz.services import OfService as s, oc, track, MetaService
from sagas.ofbiz.entities import OfEntity as e
from sagas.ofbiz.service_gen import gen_service_stub, proc_special_fields, get_mapping_type
from py4j.java_gateway import get_field
from sagas.util.str_converters import to_camel_case, to_snake_case, to_words
import clipboard

package_header='''import 'package:bloc/bloc.dart';
import 'package:decimal/decimal.dart';
import 'package:meta/meta.dart';
import 'package:sagas_meta/src/common_states.dart';
import 'package:sagas_meta/src/result_api.dart';
import 'package:sagas_meta/src/srv_api.dart';
import 'package:sagas_meta/src/common_events.dart';

import 'package:sagas_meta/src/models_t/gen_models.dart';
'''
class_header='''class {package_name} extends Bloc<ServiceEvent, ServiceState>{{
  final SrvClient client;
  {package_name}({{@required this.client}});
'''
package_footer='''}
'''

events_header='''
  @override
  ServiceState get initialState => ServiceLoading();
  @override
  Stream<ServiceState> mapEventToState(
      ServiceState currentState,
      ServiceEvent event,
      ) async* {
    if (event is SimpleEv){
      print(event.message);
      yield ServiceNotLoaded();
    }'''
events_footer='''  }
'''
event_map='''  Stream<ServiceState> _map%sToState(currentState, ev) async* {
    try {
      final result = await %s(ev);
      yield ServiceLoaded(result);
    } catch (_) {
      yield ServiceNotLoaded();
    }
  }
'''
event_condition='''    else if (event is %s) {
      yield* _map%sToState(currentState, event);
    }'''

cap_first = lambda s: s[:1].upper() + s[1:] if s else ''


def gen_bloc(lines, name):
    ms = MetaService(name)
    evname = cap_first(name) + 'Ev'
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
    params_set = set()

    invoke_ent = "null, "
    define_ent = ""
    if def_ent != "":
        # define_ent = "{} {}, ".format(def_ent, 'ent')
        define_ent = "{} {};".format(def_ent, 'ent')
        invoke_ent = 'ev.ent, '
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
                # wrap entity fields into a entity parameter
                if fldname in ent_fields:
                    pass
                elif fldname in params_set:
                    pass
                else:
                    params_set.add(fldname)
                    # invoke_pars.append("'{fld}': {fld}".format(fld=fldname))
                    invoke_pars.append(fldname)
                    # define_pars.append("{mark}{type} {fld}"
                    define_pars.append("{type} {fld}; // {mark}"
                                       .format(fld=fldname,
                                               mark=require_mark,
                                               type=get_mapping_type(fldtype)))
            if 'OUT' in mode:
                return_pars.append("{fld}[{type}]".format(fld=fldname, type=fldtype))

    lines.append("   * Requires %s" % ', '.join(requires))
    lines.append("   * Returns %s" % ', '.join(return_pars))
    lines.append("   */")

    lines.append("  Future<OfResult> %s(%s ev) =>" % (name, evname))
    # lines.append("      client.invoke('{name}', {ent}{{ {invoke_pars} }});"
    #             .format(name=name, ent=invoke_ent,
    #                     invoke_pars=', '.join(invoke_pars)))
    lines.append("      client.invoke('{name}', {ent}ev.asMap());"
                 .format(name=name, ent=invoke_ent))
    return define_pars, invoke_pars, define_ent


def gen_event_class(lines, name, define_pars, invoke_pars, define_ent):
    evname = cap_first(name) + 'Ev'
    lines.append("class %s extends ServiceEvent {" % evname)
    lines.append("  " + "\n  ".join(define_pars))
    lines.append("  " + define_ent)
    addi_par = []
    if define_ent:
        addi_par = ['ent']
    paras = ['this.' + fld for fld in invoke_pars + addi_par]
    lines.append("  %s({%s})" % (evname, ', '.join(paras)))
    lines.append("      : super([%s]);" % ', '.join(invoke_pars))
    lines.append("\n  @override")
    paras = [fld + ': $' + fld for fld in invoke_pars + addi_par]
    lines.append("  String toString() => '%s { %s }';" % (evname, ', '.join(paras)))
    lines.append("\n  @override")
    lines.append("  Map<String, dynamic> asMap(){")
    paras = ['"' + fld + '": ' + fld for fld in invoke_pars]
    lines.append("    return {%s};" % ', '.join(paras))
    lines.append("  }")
    lines.append("}")


def gen_event_map(lines, name):
    evname = cap_first(name) + 'Ev'
    lines.append(event_map % (evname, name))

def gen_blocs(package_name, services):
    lines = []
    lines.append(package_header)
    lines.append(class_header.format(package_name=to_camel_case(package_name, True)))
    lines.append(events_header)
    for service in services:
        evname = cap_first(service) + 'Ev'
        lines.append(event_condition % (evname, evname))

    lines.append(events_footer)

    for service in services:
        gen_event_map(lines, service)

    event_classes = []
    for service in services:
        define_pars, invoke_pars, define_ent = gen_bloc(lines, service)
        gen_event_class(event_classes, service, define_pars, invoke_pars, define_ent)
        lines.append('')
        event_classes.append('')

    lines.append(package_footer)

    ## add the event class
    lines.append('\n'.join(event_classes))

    print("\n".join(lines))
    clipboard.copy("\n".join(lines))

if __name__ == '__main__':
    package_name = 'common_srv_bloc'
    # services = ["testScv"]
    gen_blocs(package_name, ["testScv", 'createPerson', 'quickAddVariant'])
