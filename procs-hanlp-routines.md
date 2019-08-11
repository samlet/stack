# procs-hanlp-routines.md
## start
```python
from sagas.bots.hanlp_procs import Hanlp, hanlp, hanlp_c
for info in hanlp.helper.getHanlpInfo():
    print(info)

## viz
from sagas.bots.hanlp_viz import HanlpProtoViz
HanlpProtoViz().analyse('我要找一本英语书')
HanlpProtoViz(verbose=False).analyse('徐先生还具体帮助他确定了把画雄鹰、松鼠和麻雀作为主攻目标。')    
```

