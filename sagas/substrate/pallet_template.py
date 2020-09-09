from datetime import datetime

class PalletTemplate(object):
    def __init__(self):
        self.ctx={'timestamp': datetime.utcnow().isoformat()}

    def bake(self, template_dir, proj_name, type_name, name='pallets'):
        """
        $ python -m sagas.substrate.pallet_template bake simple-map new-map NewMap
        $ python -m sagas.substrate.pallet_template bake plain plain Plain
        $ python -m sagas.substrate.pallet_template bake dataset cookies Cookies
        :param template_dir:
        :param proj_name:
        :param name:
        :return:
        """
        from cookiecutter.main import cookiecutter
        # Create project from the cookiecutter-pypackage/ template
        cookiecutter(name,
                     no_input=True,
                     extra_context={'directory_name': proj_name,
                                    'type_name': type_name,
                                    **self.ctx},
                     directory=template_dir)

def main():
    import fire
    fire.Fire(PalletTemplate)

if __name__ == '__main__':
    main()

