import fire
import os

from sagas.ofbiz.services import OfService


class OfTools(object):
    def import_dir(self, dir):
        """
        Usage: $ python -m sagas.ofbiz.tools import_dir ./data/product/
        :param dir: data source directory
        :return: none
        """
        full_path=os.path.abspath(dir)
        ok, result=OfService().entityImportDir(path=full_path)
        if ok:
            for msg in result['messages']:
                print(msg)
        else:
            print("fail to import data files from directory.")
            print(result)

if __name__ == '__main__':
    fire.Fire(OfTools)
