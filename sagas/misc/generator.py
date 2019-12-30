#!/usr/bin/env python
import fire
import io
import clipboard
from io import StringIO
from mako.template import Template
from mako.lookup import TemplateLookup
from mako.runtime import Context

# The contents within the ${} tag are evaluated by Python directly, so full expressions are OK:
def render_template(file, ctx, buf):
    mylookup = TemplateLookup(directories=['./'], output_encoding='utf-8', encoding_errors='replace')
    mytemplate = Template(filename='./templates/'+file, module_directory='/tmp/mako_modules', lookup=mylookup)
    mytemplate.render_context(ctx)
    return (buf.getvalue())

class Generator(object):
    ## ./generator.py gen_dart_c crmsfa CrmsfaProcs
    def gen_dart_c(self, package_name, service_name):
        buf = StringIO()
        ctx = Context(buf, package_name="crmsfa", service_name="CrmsfaProcs")
        allcnt=render_template('grpc_client_dart.mako', ctx, buf)
        clipboard.copy(allcnt)
        print(allcnt)

    ## ./generator.py gen_nlp_provider hanlp Hanlp NlpProcs
    ## ./generator.py gen_nlp_provider cabocha Cabocha CabochaNlpProcs
    def gen_nlp_provider(self, component_name, class_name, service_name):
        buf = StringIO()
        ctx = Context(buf, package_name="nlpserv", 
                      file_name=component_name+"_utils",
                      class_name=class_name,
                      component_name=component_name,
                      service_name=service_name,
                      slots=["some_slot", "some_other_slot"])
        allcnt=render_template('nlu_utils.mako', ctx, buf)
        clipboard.copy(allcnt)
        print(allcnt)

if __name__ == '__main__':
    fire.Fire(Generator)

