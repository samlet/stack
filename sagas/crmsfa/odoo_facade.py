import odoorpc
import logging

logger = logging.getLogger(__name__)

odoo = odoorpc.ODOO('localhost', port=8069)
logger.info(odoo.db.list())

def login(db="sagas_odoo", username="samlet@sagas.ai", password="samlet"):
    odoo.login(db, username, password)
    user = odoo.env.user
    return user

