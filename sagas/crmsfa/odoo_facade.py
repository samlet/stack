import odoorpc

class OdooFacade(object):
    def __init__(self):
        self.odoo = odoorpc.ODOO('localhost', port=8069)

facade=OdooFacade()

