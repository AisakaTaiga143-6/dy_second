---
tasks:
- siamese-uie
- rex-uninlu
- text-classification
- zero-shot-classification
- question-answering
- sentiment-classification
- sentence-similarity
- nli
- token-classification
- named-entity-recognition
- relation-extraction
- universal-information-extraction
model_type:
- bert
domain:
- nlp
frameworks:
- pytorch
backbone:
- transformer
metrics:
- accuracy
license: Apache License 2.0
language: 
- cn
tags:
- 通用信息抽取
- 零样本信息抽取
- 命名实体识别
- 关系抽取
- 事件抽取
- 属性情感抽取
- 指代消解
- 文本分类
- 情感分类
- 自然语言推理
- 机器阅读理解
- 零样本分类
- transformer
- AliceMind
- Alibaba
datasets:
  test:
  - damo/people_daily_ner_1998_tiny
  - damo/absa_aoe
widgets:
  - task: siamese-uie
    model_revision: v1.0
    inputs:
      - type: text #可选值：text|image|video|audio
        name: input #要跟pipeline代码中的input支持的key一致，可省略
        title: #用于前端显示，如果不填会用name来显示
        validator: 
          max_words: 300 
    parameters:
      - name: schema #参数名，要跟pipeline代码中的kwargs支持的key一致
        title: Schema #用于前端显示，如果不写会使用name来显示
        type: string #可选值：enum|string|int，enum需要提供values
    examples:
      - name: 1
        title: 示例2 
        inputs:
          - name: input
            data: '1944年毕业于北大的名古屋铁道会长谷口清太郎等人在日本积极筹资，共筹款2.7亿日元，参加捐款的日本企业有69家。'
        parameters:
          - name: schema
            value: '{"人物": null, "地理位置": null, "组织机构": null}'
      - name: 2
        title: 示例1 
        inputs:
          - name: input
            data: '很满意，音质很好，发货速度快，值得购买'
        parameters:
          - name: schema
            value: '{"属性词": {"情感词": null}}'
      - name: 3
        title: 示例3
        inputs:
          - name: input
            data: '在北京冬奥会自由式中，2月8日上午，滑雪女子大跳台决赛中中国选手谷爱凌以188.25分获得金牌。2月9日上午，滑雪男子大跳台决赛中日本选手小泉次郎以188.25分获得银牌！'
        parameters:
          - name: schema
            value: '{"人物": {"比赛项目(赛事名称)": null, "参赛地点(城市)": null, "获奖时间(时间)": null, "选手国籍(国籍)": null}}'
      - name: 4
        title: 示例3
        inputs:
          - name: input
            data: '7月28日，天津泰达在德比战中以0-1负于天津天海。'
        parameters:
          - name: schema
            value: '{"胜负(事件触发词)": {"时间": null, "败者": null, "胜者": null, "赛事名称": null}}'
      - name: 5
        title: 示例5
        inputs:
          - name: input
            data: '是的,不是|哥哥点了点头。“我这几年苦哇……现在玲玲也大一点了，所以……”他望着妹妹（候选词），脸上显出一副要求她(代词)谅解的表情。'
        parameters:
          - name: schema
            value: '{"在下面的描述中，代词“她”指代的是“妹妹”吗？": null}'
      - name: 6
        title: 示例6
        inputs:
          - name: input
            data: '正向,负向|有点看不下去了，看作者介绍就觉得挺矫情了，文字也弱了点。后来才发现 大家对这本书评价都很低。亏了。'
        parameters:
          - name: schema
            value: '{"情感分类": null}'
      - name: 7
        title: 示例7
        inputs:
          - name: input
            data: '民生故事,文化,娱乐,体育,财经,房产,汽车,教育,科技,军事,旅游,国际,证券股票,农业三农,电竞游戏|学校召开2018届升学及出国深造毕业生座谈会就业指导'
        parameters:
          - name: schema
            value: '{"分类": null}'
      - name: 8
        title: 示例8
        inputs:
          - name: input
            data: '相似,不相似|摄像头区域遮挡屏幕&通话遮挡屏幕黑屏正常'
        parameters:
          - name: schema
            value: '{"文本匹配": null}'
      - name: 9
        title: 示例9
        inputs:
          - name: input
            data: '蕴含,矛盾,中立|段落1：是,但是你比如说像现在这种情况,是不是就是说咱们离它就绝对人类是再也没有任何可能性了；段落2：我对人类可能性有所思考'
        parameters:
          - name: schema
            value: '{"段落2和段落1的关系是：": null}'
      - name: 10
        title: 示例10
        inputs:
          - name: input
            data: '飞机票太贵,时间来不及,坐飞机头晕,飞机票太便宜|A：最近飞机票打折挺多的，你还是坐飞机去吧。B：反正又不是时间来不及，飞机再便宜我也不坐，我一听坐飞机就头晕。'
        parameters:
          - name: schema
            value: '{"B为什么不坐飞机?": null}'
      - name: 11
        title: 示例11
        inputs:
          - name: input
            data: '大莱龙铁路位于山东省北部环渤海地区，西起位于益羊铁路的潍坊大家洼车站，向东经海化、寿光、寒亭、昌邑、平度、莱州、招远、终到龙口，连接山东半岛羊角沟、潍坊、莱州、龙口四个港口，全长175公里，工程建设概算总投资11.42亿元。铁路西与德大铁路、黄大铁路在大家洼站接轨，东与龙烟铁路相连。大莱龙铁路于1997年11月批复立项，2002年12月28日全线铺通，2005年6月建成试运营，是横贯山东省北部的铁路干线德龙烟铁路的重要组成部分，构成山东省北部沿海通道，并成为环渤海铁路网的南部干线。铁路沿线设有大家洼站、寒亭站、昌邑北站、海天站、平度北站、沙河站、莱州站、朱桥站、招远站、龙口西站、龙口北站、龙口港站。大莱龙铁路官方网站'
        parameters:
          - name: schema
            value: '{"大莱龙铁路位于哪里？": null}'
    inferencespec:
      cpu: 2 #CPU数量
      memory: 4000 #单位MB
      gpu: 0 #GPU数量
      gpu_memory: 16000 #单位MB
---
license: Apache License 2.0
---
###### 该模型当前使用的是默认介绍模版，处于“预发布”阶段，页面仅限所有者可见。
###### 请根据[模型贡献文档说明](https://www.modelscope.cn/docs/%E5%A6%82%E4%BD%95%E6%92%B0%E5%86%99%E5%A5%BD%E7%94%A8%E7%9A%84%E6%A8%A1%E5%9E%8B%E5%8D%A1%E7%89%87)，及时完善模型卡片内容。ModelScope平台将在模型卡片完善后展示。谢谢您的理解。

#### Clone with HTTP
```bash
 git clone https://www.modelscope.cn/damo/nlp_deberta_rex-uninlu_chinese-base.git
```
