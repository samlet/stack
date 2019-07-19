#!/usr/bin/env python
import odoorpc

# Prepare the connection to the server
odoo = odoorpc.ODOO('localhost', port=8069)

def test_sales():
    # Check available databases
    print(odoo.db.list())

    # Login
    # db="sagas_odoo"
    db="odoo12"
    username="samlet@sagas.ai"
    password="samlet"
    # odoo.login('db_name', 'user', 'passwd')
    odoo.login(db, username, password)

    # Current user
    user = odoo.env.user
    print(user.name)            # name of the user connected
    print(user.company_id.name) # the name of its company

    # Simple 'raw' query
    user_data = odoo.execute('res.users', 'read', [user.id])
    print(user_data)

    # Use all methods of a model
    if 'sale.order' in odoo.env:
        Order = odoo.env['sale.order']
        order_ids = Order.search([])
        for order in Order.browse(order_ids):
            print(order.name)
            products = [line.product_id.name for line in order.order_line]
            print(products)

    # Update data through a record
    # user.name = "Brian Jones"

if __name__ == '__main__':
    test_sales()
    