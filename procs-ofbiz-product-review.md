# procs-ofbiz-product-review.md
## start
```python
from sagas.ofbiz.services import OfService as s
from sagas.ofbiz.entities import OfEntity as e
import sagas.ofbiz.entities as ee

df=s('meta').createProductReview
df[df['required']=='*'].sort_values(by='mode')
```
