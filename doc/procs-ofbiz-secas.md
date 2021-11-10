# procs-ofbiz-secas.md
⊕ [ofbiz总结——OFBiz中有两种类型的ECA规则：SECAs和EECAs_xiaozaq的博客-CSDN博客](https://blog.csdn.net/xiaozaq/article/details/78421464)
    .. 对于SECA，触发器(事件)是一个将调用的服务。一个条件可能是如果一个参数等于某个值(条件是可选的)，动作是调用另一个服务。
    更普遍的，SECA在commit或return上触发；然而，在服务生命周期中的下面任何阶段事件都是可能的：
        ·   auth——认证之前
        ·   in-validate——IN参数检查之前
        ·   out-validate——OUT参数检查之前
        ·   invoke——服务调用之前
        ·   commit——事务提交之前
        ·   return——服务返回之前
        ·   global-commit
        ·   global-rollback

    变量 global-commit和 global-rollback有一点不同。如果服务是一个事务的一部分，它们仅在回滚后或者提交的两个阶段(JTA实现)间运行。
    也有两个值默认为false的特殊属性：
    ·   run-on-failure
    ·   run-on-error

    如果你想在尽管失败或者错误时SECA运行，可以设置为true。失败与错误是相同的事物，除了它不代表需要回滚的情况。
    需要注意的是，如果需要，传递到触发服务的参数对动作服务是有效的。触发服务OUT参数对动作服务也是有效的。

⊕ [SECAs and Error and Failure Management - OFBiz Project Open Wiki - Apache Software Foundation](https://cwiki.apache.org/confluence/display/OFBIZ/SECAs+and+Error+and+Failure+Management)
    .. For a Sync service, the service chain runs as follows:

        auth action
        check
        auth event
        in-validate action
        check
        validate event (skipped if any admitted errors or failures so far)
        invoke action
        check
        actual service run (skipped if any admitted errors or failures so far)
        check
        out-validate action
        validate event
        commit action
        check
        global-commit-post-run action
        release locks, end transactions, commit unless there has been an error, in which case rollback
        return action

    .. For an Async service, the service chain is:

        auth action
        auth event
        in-validate action
        check
        validate event (skipped if any admitted errors or failures so far)
        submit service to JobManager (skipped if any admitted errors or failures so far)


⊕ [SECAs | ScipioERP](https://www.scipioerp.com/community/developer/events-actions/secas/)

⊕ [Service Engine Guide - OFBiz Project Open Wiki - Apache Software Foundation](https://cwiki.apache.org/confluence/display/OFBIZ/Service+Engine+Guide#ServiceEngineGuide-ServiceEngineGuide-ecas)

* ECA（事件条件动作）很像触发器。调用服务时，将执行查找以查看是否为此事件定义了任何 ECA。事件包括认证之前、IN 参数验证之前、实际服务调用之前、OUT 参数验证之前、事务提交之前或服务返回之前。接下来评估 ECA 定义中的每个条件，如果所有条件都为真，则执行每个操作。操作只是一个服务，必须定义它才能使用服务上下文中已有的参数。每个 ECA 可以定义的条件或操作的数量没有限制。

```xml
<service-eca>
    <eca service="testScv" event="commit">
        <condition field-name="message" operator="equals" value="12345"/>
        <action service="testBsh" mode="sync"/>
    </eca>
</service-eca>
```

提示：请注意，您可以使用 set 操作重命名触发服务的参数或插入值，例如...

```xml
<eca service="setCustRequestStatus" event="commit">
    <condition field-name="oldStatusId" operator="not-equals" value="CRQ_ACCEPTED"/>
    <condition field-name="statusId" operator="equals" value="CRQ_ACCEPTED"/>
    <set field-name="bodyParameters.custRequestId" env-name="custRequestId"/>
    <set field-name="bodyParameters.custRequestName" env-name="custRequestName"/>
    <set field-name="partyIdTo" env-name="fromPartyId"/>
    <set field-name="emailTemplateSettingId" value="CUST_REQ_ACCEPTED"/>
    <action service="sendMailFromTemplateSetting" mode="sync" />
</eca>
```

## eecas
该ECA确保一旦Product记录上的任何创建或更新操作碑提交，只要该字段的autoCreateKeywords字段不是N，indexProductKeywords服务将自动同步调用。
操作可以是下面任何自我说明的操作：
·   create
·   store
·   remove
·   find
·   create-store (create or store/update)
·   create-remove
·   store-remove
·   create-store-remove
·   any

return事件是至此EECA使用最多的事件。但也存在 validate, run, cache-check,cache-put 和 cache-clear事件。也有run-on-error属性。
在组件中使用EECA之前，组件必须知道eca 实体资源的位置：
<entity-resource type="eca" loader="main" location="entitydef/eecas.xml"/>
必须在ofbiz-component.xml文件的既存<entity-resource>元素的下面添加这一行。
 
注意：ECA常常公开发现人们在说谎(catch people out)。因为在代码中触发器服务中没有显式的流程，它们可能很难调试。调试时常看看日志。当一个ECA触发了，日志中就会添加一条来通知这个触发和动作。

## 服务组
服务组是一组在调用初始服务时应该运行的服务。您使用组服务引擎定义服务，并包含组中所有服务所需的所有参数/属性。groupservices 不需要位置属性，invoke 属性定义要运行的组的名称。调用此服务时，将调用组，并按定义调用组中定义的服务。

组定义非常简单，它包含一个组元素以及 1 个或多个服务元素。group 元素包含一个 name 属性和一个 mode 属性，用于定义组将如何运作。service 元素很像 ECA 中的 action 元素，区别在于结果到上下文的默认值。

```xml
<service-group>
    <group name="testGroup" send-mode="all">
        <invoke name="testScv" mode="sync"/>
        <invoke name="testBsh" mode="sync"/>
    </group>
</service-group>
```
