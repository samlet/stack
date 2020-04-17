from cached_property import cached_property
from sagas.nlu.warehouse_intf import AnalResource
from sagas.ofbiz.services import MetaService, create_service_data_frame


class AnalService(AnalResource):
    def __repr__(self):
        return f"service {self.name}"

    @cached_property
    def meta(self):
        return MetaService(self.name)

    @property
    def meta_df(self):
        return create_service_data_frame(self.name)

