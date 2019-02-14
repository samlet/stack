import fire
import os

from sagas.ofbiz.services import OfService as s

class OfTools(object):
    def import_dir(self, dir):
        """
        Usage: $ python -m sagas.ofbiz.tools import_dir ./data/product/
        :param dir: data source directory
        :return: none
        """
        full_path=os.path.abspath(dir)
        ok, result=s().entityImportDir(path=full_path)
        if ok:
            for msg in result['messages']:
                print(msg)
        else:
            print("fail to import data files from directory.")
            print(result)

    def service_logs(self):
        from sagas.ofbiz.entities import OfEntity as e, oc
        oc.import_package('org.apache.ofbiz.service.ServiceDispatcher')
        log = oc.j.ServiceDispatcher.getServiceLogMap()
        for rs, value in log.items():
            print(oc.get(rs.getModelService(), 'name'), rs.getLocalName(), rs.getMode(), rs.getStartStamp(),
                  rs.getEndStamp())

    def ping(self):
        ok, ret=s().testScv(defaultValue=5.5, message="hello world")
        print(ok, ret)

    def users(self):
        from sagas.ofbiz.entities import OfEntity as e, oc
        rs=e().allUserLogin()
        for r in rs:
            print(r['userLoginId'])

    def convert_minilang_from_clip(self):
        """
        Will convert the xml content in clipboard:
        <set field="serviceCtx.currencyUomId" value="USD"/>
        <set field="serviceCtx.costComponentTypePrefix" value="EST_STD"/>
        :return:
        """
        import xml.etree.ElementTree as ET
        import clipboard
        sett = clipboard.paste()
        root = ET.fromstring('<routine>' + sett + '</routine>')
        # print('root', root.tag)
        result = []
        for setter in root.findall('set'):
            field = setter.get('field')
            type = setter.get('type')
            value = setter.get('value')
            if '.' in field:
            # if field.startswith("serviceCtx.") or field.startswith("searchParams."):
                if type == 'BigDecimal':
                    value = 'oc.j.BigDecimal(' + value + ')'
                elif type == 'Timestamp':
                    value = "oc.j.Timestamp.valueOf('" + value + "')"
                elif type == 'Integer':
                    pass
                elif type == 'Boolean':
                    value="True" if value=="true" else "False"
                else:
                    value = "'" + value + "'"
                line = "{}={}".format(field.split('.')[1], value)
                result.append(line)

        text = ",\n".join(result)
        print(text)
        clipboard.copy(text)

if __name__ == '__main__':
    fire.Fire(OfTools)
