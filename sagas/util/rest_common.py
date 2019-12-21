import requests
from sagas.conf.conf import cf

def query_data_by_url(conf_item, fn_path, data):
    if '://' not in conf_item:
        url=cf.ensure(conf_item)
    else:
        url=conf_item
    # the url format: 'http://localhost:8092/entities'
    response = requests.post(f"{url}/{fn_path}", json=data)
    if response.status_code == 200:
        r=response.json()
        return {'result':'success', 'data':r}
    return {'result':'fail', 'cause':'error response'}

