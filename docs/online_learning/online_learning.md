### Online Learning

#### 概述

推荐网络模型更新的实时性要求较高，online learning的方式可有效特性推荐网络模型更新实时性， 提高模型精度与点击通过率。

在线训练与离线训练主要区别：

1. 在线学习训练数据为流式数据、无确定的dataset size、epoch，离线训练训练数据有确定的data set size、epoch。
2. 在线学习为服务，持续训练，离线训练训练完离线数据集后退出。
3. 在线训练需要收集并存储训练数据，收集到固定数量的数据或者经过一定时间窗口后驱动训练流程。



#### 整体架构

用户的流式训练数据推送的 kafka 中，MindPandas 从 kafka 读取数据并进行特征工程转换，然后写入分布式计算引擎中，MindData 从分布式计算引擎中读取数据作为训练数据进行训练，MindSpore 进程作为服务常驻，有数据接入就进行训练，并定期导出 ckpt，整体流程见下图1

图1  在线训推一体化 E2E部署视图

![image.png](https://foruda.gitee.com/images/1665653730199149252/d77df81a_7356746.png)



#### 新增API

```python
RecModel.online_train(self, train_dataset, callbacks=None, dataset_sink_mode=True, sink_size=1)
```

| 参数名称          | 描述                                                                                       | 默认值 |
| ----------------- | ------------------------------------------------------------------------------------------ | ------ |
| train_dataset     | (Dataset) 在线训练数据集，包含训练数据和label，该数据集无边界，dataset_size == sys.maxsize | 无     |
| callbacks         | (Optional[list[Callback], Callback]) 训练过程中执行的callbacks                             | None   |
| dataset_sink_mode | (bool) 是否开启数据下沉，如果开启，数据将通过dataset channel发送到device queue中           | True   |
| sink_size         | ( int)控制一次下沉多少个batch的数据                                                        | 1      |


使用前先安装mindspore_rec推荐套件，安装方式见[ReadMe](../../README.md)

example：
```
from mindspore_rec import RecModel as Model
#model定义同mindspore.model
...
model.online_train(self, train_dataset, callbacks=None, dataset_sink_mode=True)

```



#### 使用约束

- online learning数据模块依赖MindPandas，MindPandas最低支持Python版本为Python3.8，所以online learning需要使用3.8以上的Python版本，对应于MindSpore及recommender套件都使用Python3.8版本。

- 目前支持 GPU后端、静态图模式、Linux平台
- 暂不支持fullbatch
- 训练侧新增接口（位于recommender仓），sink_size入参目前仅支持1，默认值也为1:

```
RecModel.online_train(self, train_dataset, callbacks=None, dataset_sink_mode=True, sink_size=1)
```



#### Python包依赖

mindpandas  v0.1.0

mindspore_rec  v0.2.0

kafka-python v2.0.2



#### 使用样例

下面以Criteo数据集训练Wide&Deep为例，介绍一下整个online learning流程，样例代码位于[examples/online_learning](../../examples/online_learning)

1. 启动kafka

2. 启动分布式计算引擎

   ```bash
   yrctl start --master  --address $MASTER_HOST_IP  
   
   # 参数说明
   --master： 表示当前host为master节点，非master节点不用指定‘--master’参数
   --address： master节点的ip
   ```

3. 启动数据producer

   producer 用于模拟在线训练场景，将本地的criteo数据集写入到kafka，供consumer使用

   ```bash
   python producer.py
   ```

4. consumer

   ```bash
   python consumer.py  --num_shards=$DEVICE_NUM  --address=$LOCAL_HOST_IP  --max_dict=$PATH_TO_VAL_MAX_DICT  --min_dict=$PATH_TO_CAT_TO_ID_DICT  --map_dict=$PATH_TO_VAL_MAP_DICT
   
   #参数说明
   --num_shards：对应训练侧的device 卡数，单卡训练则设置为1，8卡训练设置为8
   ```

   consumer为criteo数据集进行特征工程需要3个数据集相关文件: `all_val_max_dict.pkl`, `all_val_min_dict.pkl`, `cat2id_dict.pkl`, `$PATH_TO_VAL_MAX_DICT`, `$PATH_TO_CAT_TO_ID_DICT`, `$PATH_TO_VAL_MAP_DICT` 分别为这些文件在环境上的绝对路径。这3个pkl文件具体生产方法可以参考[process_data.py](../../datasets/criteo_1tb/process_data.py)，对原始criteo数据集做转换生产对应的.pkl文件。

5. 启动训练

   config采用yaml的形式，见[default_config.yaml](../../examples/online_learning/default_config.yaml)

   单卡训练：

   ```bash
   python online_train.py --address=$LOCAL_HOST_IP   --dataset_name=criteo 
   
   #参数说明：
   --address： 本机host ip，从MindPandas接收训练数据需要配置
   --dataset_name： 数据集名字，和consumer模块保持一致
   ```

   多卡训练MPI方式启动：

   ```bash
   bash mpirun_dist_online_train.sh [$RANK_SIZE] [$LOCAL_HOST_IP]
   
   #参数说明：
   RANK_SIZE：多卡训练卡数量
   LOCAL_HOST_IP：本机host ip，用于MindPandas戎接收训练数据
   ```

   动态组网方式启动多卡训练：

   ```bash
   bash run_dist_online_train.sh [$WORKER_NUM] [$SHED_HOST] [$SCHED_PORT] [$LOCAL_HOST_IP]
   
   #参数说明：
   WORKER_NUM：多卡训练卡数量
   SHED_HOST：MindSpore动态组网需要的Scheduler 角色的IP
   SCHED_PORT：MindSpore动态组网需要的Scheduler 角色的Port
   LOCAL_HOST_IP：本机host ip，从MindPandas接收训练数据需要配置
   ```
