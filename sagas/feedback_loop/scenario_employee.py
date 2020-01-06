from pprint import pprint

from sagas.misc.utils import to_std_dicts

from .models_employee import Department as DepartmentModel, init_db, db_session
from .models_employee import Employee as EmployeeModel
from .models_employee import Role as RoleModel

import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType


class Department(SQLAlchemyObjectType):
    class Meta:
        model = DepartmentModel
        interfaces = (relay.Node, )


class Employee(SQLAlchemyObjectType):
    class Meta:
        model = EmployeeModel
        interfaces = (relay.Node, )


class Role(SQLAlchemyObjectType):
    class Meta:
        model = RoleModel
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    # Allow only single column sorting
    all_employees = SQLAlchemyConnectionField(
        Employee, sort=Employee.sort_argument())
    # Allows sorting over multiple columns, by default over the primary key
    all_roles = SQLAlchemyConnectionField(Role)
    # Disable sorting over this field
    all_departments = SQLAlchemyConnectionField(Department, sort=None)


schema = graphene.Schema(query=Query, types=[Department, Employee, Role])

class ScenarioEmployee(object):
    def __init__(self, recreate=True):
        if recreate:
            init_db()

    def query(self):
        """
        $ python -m sagas.feedback_loop.scenario_employee query
        :return:
        """
        query = """
        {
          allEmployees(sort: [NAME_ASC, ID_ASC]) {
            edges {
              node {
                id
                name
                department {
                  id
                  name
                }
                role {
                  id
                  name
                }
              }
            }
          }
        }
        """
        result = schema.execute(query, context_value={'session': db_session})
        if not result.errors:
            pprint(to_std_dicts(result.data))

sc_employee=ScenarioEmployee(recreate=False)

if __name__ == '__main__':
    import fire
    fire.Fire(ScenarioEmployee)


