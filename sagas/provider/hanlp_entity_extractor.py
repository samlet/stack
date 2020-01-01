from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import typing
from typing import Any
from typing import Dict
from typing import List
from typing import Text

from rasa.nlu.extractors import EntityExtractor
from rasa.nlu.training_data import Message

# nz-其他专名: 除人名、国名、地名、团体、机构、组织以外的其他专有名词都标以nz。满族/nz，俄罗斯族/nz，汉语/nz，罗马利亚语/nz， 捷克语/nz，中文/nz， 英文/nz， 满人/nz， 哈萨克人/nz， 诺贝尔奖/nz， 茅盾奖/nz， 1.包含专有名称（或简称）的交通线，标以nz；短语型的，标为NZ。津浦路/nz， 石太线/nz， [京/j 九/j 铁路/n]NZ， [京/j 津/j 高速/b 公路/n]NZ， 2. 历史上重要事件、运动等专有名称一般是短语型的，按短语型专有名称处理，标以NZ。[卢沟桥/ns 事件/n]NZ， [西安/ns 事变/n]NZ，[五四/t 运动/n]NZ， [明治/nz 维新/n]NZ，[甲午/t 战争/n]NZ，3.专有名称后接多音节的名词，如“语言”、“文学”、“文化”、“方式”、“精神”等，失去专指性，则应分开。欧洲/ns 语言/n， 法国/ns 文学/n， 西方/ns 文化/n， 贝多芬/nr 交响乐/n， 雷锋/nr 精神/n， 美国/ns 方式/n，日本/ns 料理/n， 宋朝/t 古董/n 4. 商标（包括专名及后接的“牌”、“型”等）是专指的，标以nz，但其后所接的商品仍标以普通名词n。康师傅/nr 方便面/n， 中华牌/nz 香烟/n， 牡丹III型/nz 电视机/n， 联想/nz 电脑/n， 鳄鱼/nz 衬衣/n， 耐克/nz 鞋/n5. 以序号命名的名称一般不认为是专有名称。2/m 号/q 国道/n ，十一/m 届/q 三中全会/j如果前面有专名，合起来作为短语型专名。[中国/ns 101/m 国道/n]NZ， [中共/j 十一/m 届/q 三中全会/j]NZ，6. 书、报、杂志、文档、报告、协议、合同等的名称通常有书名号加以标识，不作为专有名词。由于这些名字往往较长，名字本身按常规处理。《/w 宁波/ns 日报/n 》/w ，《/w 鲁迅/nr 全集/n 》/w，中华/nz 读书/vn 报/n， 杜甫/nr 诗选/n，少数书名、报刊名等专有名称，则不切分。红楼梦/nz， 人民日报/nz，儒林外史/nz 7. 当有些专名无法分辨它们是人名还是地名或机构名时，暂标以nz。[巴黎/ns 贝尔希/nz 体育馆/n]NT，其中“贝尔希”只好暂标为nz。
mappings={"ns":"location",
          "nr": "person",
          "nt": "organization",
          "nz":"proper",
          "nx":"foreign",
          "s":"space",
          "t":"time",
          "mq":"amount",
          "m":"numeral",
          "nf":"food"
         }

def normalize_entity(t):
    kind = t.entity
    if t.entity in mappings:
        kind = mappings.get(kind)
    return kind

class HanlpEntityExtractor(EntityExtractor):
    # name = "ner_hanlp"
    name="sagas.provider.hanlp_entity_extractor.HanlpEntityExtractor"

    provides = ["entities"]

    requires = ["hanlp"]

    def process(self, message, **kwargs):
        # type: (Message, **Any) -> None
        filters = mappings.keys()
        extracted = self.add_extractor_name(self.extract_entities(message.get("hanlp_doc"), filters))
        message.set("entities",
                    message.get("entities", []) + extracted,
                    add_to_output=True)

    @staticmethod
    def extract_entities(msg_tokens, filters):
        entities = []
        for token in msg_tokens.entities:
            if token.entity in filters:
                entities.append({
                    "entity": normalize_entity(token),
                    "value": token.value,
                    "start": token.start,
                    "confidence": None,
                    "end": token.end
                })
        return entities

