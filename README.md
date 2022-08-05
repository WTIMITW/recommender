# recommender

### 介绍

recommender仓旨在提供主流推荐网络模型高效训练的解决方案及流程指导，训练方案结合了昇思MindSpore自动并行、图算融合及多级Embedding Cache等能力；我们提供了开箱即用的数据集下载与转换工具、模型训练样例、BenchMark复现，降低开发者入门门槛。

### 仓库结构 

```bash

└── recommender
    ├── benchmarks            // 推荐网络训练性能benchmarks
    ├── datasets              // 数据集下载与转换工具
    │   └── criteo_1tb
    └── rec                   // 典型推荐网络模型端到端训练指导
        └── models
```

### 模型库

模型逐步迁移中，目前[models](rec/models)目录包含Wide&Deep、Deep&Cross Network(DCN)模型的端到端训练流程使用指导。


### 使用说明

recommender无需编译安装，只需将代码clone到本地，训练不同模型会有少量的Python依赖包需要安装，详见各个模型目录中的requirements.txt

**克隆代码**

```bash
git clone https://gitee.com/mindspore/recommender.git
cd recommender
```

### 社区
#### 治理
查看MindSpore如何进行[开放治理](https://gitee.com/mindspore/community/blob/master/governance.md)。

### 参与贡献

欢迎参与贡献。更多详情，请参阅我们的[贡献者Wiki](https://gitee.com/mindspore/mindspore/blob/master/CONTRIBUTING.md)。

### 许可证
[Apache License 2.0](https://gitee.com/mindspore/recommender/blob/master/LICENSE)