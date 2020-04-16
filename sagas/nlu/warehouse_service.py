from sagas.nlu.warehouse_intf import AnalResource

class AnalService(AnalResource):
    def __repr__(self):
        return f"service {self.name}"



