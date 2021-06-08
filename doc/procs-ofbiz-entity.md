# procs-ofbiz-entity.md
## not null (pk字段非空)
```java
if (field.getIsNotNull() || field.getIsPk()) {
    if (this.datasourceInfo.getAlwaysUseConstraintKeyword()) {
        sqlBuf.append(" CONSTRAINT NOT NULL, ");
    } else {
        sqlBuf.append(" NOT NULL, ");
    }
} else {
    sqlBuf.append(", ");
}
```

## manual
⊕ [通用实体概述-OFBiz Project开放式Wiki-Apache软件基金会](https://cwiki.apache.org/confluence/display/OFBIZ/General+Entity+Overview)

### 可扩展性模式
在OFBiz数据模型中，您经常会看到一种重复的模式，需要进行一些解释。此模式用于使数据模型更灵活，并消除了否则可能必须存在的大量表。它有助于遵循该模式的实体的使用概念化。它还提供了一种使用该模式的实体的运行时可扩展性的方法。

对于给定的实体，有3个或4个相关实体用于实现此模式。这些都是：
    EntityClass（可选），
    EntityType， 
    EntityAttribute，和 
    EntityTypeAttr。
每个Entity实例可以具有一个或多个由EntityType描述的类型。如果一个实体可以具有多种类型，则可以使用EntityClass或Entity Categories实体来实现Entity和EntityType之间的多对多关系。否则，不需要EntityClass，并且Entity将具有一个EntityTypeId字段。

+ 实体类型

EntityType用于描述实体。如果在给定EntityType实例的parentTypeId字段中指定了某个特性，则给定EntityType可以从父EntityType继承功能。如果表与给定的EntityType实例相关联，该实例的名称与EntityTypeId字段值相同，则hasTable字段应具有值“ Y”，否则应具有值“ N”。提供了一个描述字段，用于对EntityType实例的简短描述。

+ 实体属性

EntityAttribute用于存储给定Entity实例的名称-值对属性的实例。可以使用属性代替Entity表上的列，尤其是当该属性不适用于所有类型的Entities时。属性也可以临时用于适用于给定Entity实例的任何名称/值对信息。如果有许多属性应用于给定的EntityType，则最好创建一个单独的实体来保存这些属性，并通过将其命名为与EntityTypeId相同的名称并将hasTable字段设置为'Y'来使该实体与EntityType实例关联。 EntityType实例。这比重复查询给定Entity实例的属性集合要快。
    * If many attributes apply to a given EntityType it may be best to create a separate entity to hold those attributes, and have that entity be associated with the EntityType instance by naming it the same as the entityTypeId and setting the hasTable field to 'Y' on the EntityType instance. This will be faster than repeatedly querying a collection of attributes for a given Entity instance.

* 这里说的的单独实体是指有TypeAttr后辍的实体, 比如AgreementType有专用的扩展实体AgreementTypeAttr;
* 而临时给定的实体属性, 是指有Attribute后辍的实体, 比如BudgetAttribute, 它的字段有attrName, attrValue, attrDescription;

+ EntityTypeAttr

EntityTypeAttr用于指定与给定的EntityTypeId对应的实体实例应存在哪些属性。列出entityTypeId和名称字段组合以指定此名称。例如，EntityTypeId为“ BOX”的EntityType应该始终具有名为“ HEIGHT”，“ WIDTH”，“ DEPTH”和“ COLOR”的属性，因此对于每个这些属性都将存在EntityTypeAttr的实例。

对于某些实体，此模式有所不同，但此说明通常适用于此数据模型。请注意，数据模型的默认类型种子数据位于各种* Data.xml文件中，通常在每个组件的数据目录中。


