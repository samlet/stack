class CustInspectors(object):
    def __init__(self):
        import json_utils
        import os
        from sagas.nlu.rules_lang_spec import class_from_module_path

        self.cls_map = {}

        reg_file='./assets/inspectors.json'
        if os.path.exists(reg_file):
            regs=json_utils.read_json_file(reg_file)

            for k,v in regs.items():
                print(k,v)
                c=class_from_module_path(v)
                self.cls_map[k]=c

    def __getattr__(self, clz):
        if clz in self.cls_map:
            return self.cls_map[clz]
        else:
            raise ValueError(f"Cannot find such class item {clz}")


ci=CustInspectors()

