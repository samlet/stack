import numpy as np
import pandas as pd
import pyarrow as pa
from sagas.ofbiz.entities import OfEntity as e

def gen_ordinal_sales():
    rng = pd.date_range('1/1/2007 00:00', periods=10, freq='Y')
    ts = pd.Series(np.random.randint(1, 100, size=10), rng)
    # 将时间日期索引转化为时间阶段索引
    ps = ts.to_period()
    return ps

def gen_xml_data(ps, entity_name, id_col, index_col, val_col):
    lines = []
    data_header = '''<?xml version="1.0" encoding="UTF-8"?>
    <entity-engine-xml>'''
    data_footer = '''</entity-engine-xml>'''
    data_item = '''    <{entity} {id_col}="{id}" {index_col}="{index}" {val_col}="{val}"/>'''
    lines.append(data_header)
    for it in ps.items():
        period = it[0]
        # print(period.start_time	, period.freq)
        lines.append(data_item.format(entity=entity_name,
                                      id_col=id_col,
                                      index_col=index_col,
                                      val_col=val_col,
                                      id=str(period.start_time),
                                      index=str(period),
                                      val=it[1]))
    lines.append(data_footer)
    cnt = '\n'.join(lines)
    return cnt

def gen_sample_dss_data():
    import io_utils
    import os
    import sagas.ofbiz

    root_dir = os.path.dirname(sagas.ofbiz.__file__).replace("sagas/ofbiz", "")

    entity_name = "DssOrdinalSales"
    id_col = "dssOrdinalSalesId"
    index_col = 'year'
    val_col = 'sales'

    ps = gen_ordinal_sales()
    cnt = gen_xml_data(ps, entity_name, id_col, index_col, val_col)
    target=root_dir + 'data/dss/' + entity_name + "GenData.xml"
    io_utils.write_to_file(target, cnt)

    print('write to', target,"ok.")

if __name__ == '__main__':
    gen_sample_dss_data()


