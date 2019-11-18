import odoorpc
import logging
from sagas.conf.conf import cf

logger = logging.getLogger(__name__)

odoo = odoorpc.ODOO(cf.conf['odoo_servant'], port=8069)
logger.info(odoo.db.list())

# def login(db="sagas_odoo", username="samlet@sagas.ai", password="samlet"):
def login(db="odoo12", username="samlet@sagas.ai", password="samlet"):
    odoo.login(db, username, password)
    user = odoo.env.user
    return user

