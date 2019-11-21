from grakn.client import GraknClient

class GraknProcs(object):
    def query_phone_calls(self):
        """
        $ python -m sagas.tests.grakn.grakn_procs query_phone_calls
        :return:
        """
        with GraknClient(uri="sagas:48555") as client:
            with client.session(keyspace="phone_calls") as session:
                with session.transaction().read() as transaction:
                    query = [
                        'match',
                        '  $customer isa person, has phone-number $phone-number;',
                        '  $company isa company, has name "Telecom";',
                        '  (customer: $customer, provider: $company) isa contract;',
                        '  $target isa person, has phone-number "+86 921 547 9004";',
                        '  (caller: $customer, callee: $target) isa call, has started-at $started-at;',
                        '  $min-date == 2018-09-14T17:18:49; $started-at > $min-date;',
                        'get $phone-number;'
                    ]

                    print("\nQuery:\n", "\n".join(query))
                    query = "".join(query)

                    iterator = transaction.query(query)
                    answers = iterator.collect_concepts()
                    result = [answer.value() for answer in answers]

                    print("\nResult:\n", result)

if __name__ == '__main__':
    import fire
    fire.Fire(GraknProcs)
