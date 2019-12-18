from py4j.java_gateway import java_import, get_field

class DroolsProcs(object):
    def __init__(self):
        from py4j.java_gateway import JavaGateway, JavaObject, GatewayParameters

        host = "localhost"
        port = 4333
        callback_port = 4334
        self.gateway = JavaGateway(python_proxy_port=callback_port,
                              gateway_parameters=GatewayParameters(address=host, port=port, auto_field=True))
        self.j = self.gateway.new_jvm_view()
        java_import(self.j, 'org.kie.api.*')

    def stack_procs(self):
        stack = self.gateway.entry_point.getStack()
        stack.push('one')
        print(stack.pop())

    def rule_procs(self):
        """
        * preqs: sagas/projs/ruleprocs, ./startup.run servant
        :return:
        """
        ks = self.j.KieServices.get()
        kc = ks.getKieClasspathContainer()
        java_import(self.j, 'org.drools.examples.helloworld.*')
        self.j.HelloWorldExample.execute(ks, kc)

if __name__ == '__main__':
    import fire
    fire.Fire(DroolsProcs)




