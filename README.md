# 项目介绍
这是一个mqtt转发到kafka的中间件，_将订阅的mqtt消息转发到相同主题的kafka中_

# 项目背景
为了照顾会接mqtt，但不会接kafka的同学~ 属于一种填补内部技术差异的需求

# 项目使用
1. 打包项目

```bash
cd .\mqtt2kafka
pyinstaller -F .\main.py -n  mqtt2kafka
```

2. 配置使用
config.yaml为本项目的配置文件，配置对应的mqtt topic，mqtt broker 地址；kafka集群地址
# 其他
正好自己完善下python中间件的开发范式