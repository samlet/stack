# procs-ofbiz-gen.md
```sh
$ python -m sagas.ofbiz.entity_gen
$ python -m sagas.ofbiz.service_gen

# generate samples
$ python -m sagas.ofbiz.entity_gen gen-sample-jsonifiers

$ python -m sagas.ofbiz.entity_gen gen_package org.apache.ofbiz.product.feature /Users/xiaofeiwu/jcloud/assets/langs/workspace/flutter/sagas_meta/lib/src/models
$ python -m sagas.ofbiz.entity_gen gen_package org.apache.ofbiz.product.subscription /Users/xiaofeiwu/jcloud/assets/langs/workspace/flutter/sagas_meta/lib/src/models

# generate all entities
$ python -m sagas.ofbiz.entity_gen gen_packages /Users/xiaofeiwu/jcloud/assets/langs/workspace/flutter/sagas_meta/lib/src/models

$ python -m sagas.ofbiz.entity_gen gen_jsonifier org.apache.ofbiz.product.subscription /Users/xiaofeiwu/jcloud/assets/langs/workspace/flutter/sagas_meta/lib/src/jsonifiers

# generate all jsonifiers
$ python -m sagas.ofbiz.entity_gen gen_jsonifiers /Users/xiaofeiwu/jcloud/assets/langs/workspace/flutter/sagas_meta/lib/src/jsonifiers
```

```sh
python -m sagas.ofbiz.service_gen gen_samples
python -m sagas.ofbiz.service_gen gen_sample_group humanres_services_position /Users/xiaofeiwu/jcloud/assets/langs/workspace/flutter/sagas_meta/lib/src/services

# generate all services
python -m sagas.ofbiz.service_gen gen_sample_groups /Users/xiaofeiwu/jcloud/assets/langs/workspace/flutter/sagas_meta/lib/src/services
```

## generate flutter sections
```sh
$ python -m sagas.ofbiz.gen_section gen Loc
```





