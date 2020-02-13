import logging

from sagas.tool import init_logger
from sagas.util.loader import class_from_module_path

logger = logging.getLogger(__name__)

class Startup(object):
    def __init__(self):
        self.mods=[]

    def start(self):
        import json
        import glob
        import os
        import sys
        from sagas.conf import resource_files, resource_path
        mod_files=[resource_path(f) for f in resource_files('startups_*.json')]
        if os.path.exists('./assets'):
            mod_files.extend(glob.glob('./assets/startups_*.json'))
            sys.path.append(os.path.abspath('.'))

        for mod_file in mod_files:
            logger.info(f'.. load startup {mod_file}')
            with open(mod_file) as f:
                cfg=json.load(f)
                classes=[class_from_module_path(c) for c in cfg]
                for c in classes:
                    ci=c()
                    self.mods.append(ci)
                    ci.start()

startup=Startup()


