from sagas.ofbiz.runtime_context import platform

oc=platform.oc

oc.import_package('java.sql.Date')
oc.import_package('java.sql.Time')
oc.import_package('java.net.URL')
oc.import_package('org.apache.ofbiz.base.util.UtilDateTime')

class DateTime(object):
    @classmethod
    def now_timestamp(cls):
        """
        from sagas.ofbiz.date_time import DateTime
        productionRunStartDate=DateTime.now_timestamp()
        :return:
        """
        return oc.j.UtilDateTime.nowTimestamp()
    @classmethod
    def date(cls, date_str):
        """
        date=oc.j.Date.valueOf('2010-12-10')
        :param date_str:
        :return:
        """
        return oc.j.Date.valueOf(date_str)
    @classmethod
    def time(cls, time_str):
        """
        time=oc.j.Time.valueOf('12:12:10')
        :param time_str:
        :return:
        """
        return oc.j.Time.valueOf(time_str)
