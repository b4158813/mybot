# mybot

该机器人原理是：基于 酷Q + Python + nonebot异步QQ机器人框架

当然这个repo里面没有酷Q，具体可以到[酷Q版本发布](https://cqp.cc/b/news)查看更新和下载

附上几个有用的链接：

- 没学过异步IO的，参考[廖雪峰大神的官网](https://www.liaoxuefeng.com/wiki/1016959663602400/1017959540289152)

- [nonebot 官方文档](https://nonebot.cqp.moe/)
- [酷Q应用发布社区](https://cqp.cc/b/app)
- [CQHTTP插件文档](https://cqhttp.cc/docs/4.15/#/)

### 项目内容

由于酷Q本身没有python的SDK（软件开发工具包）可用，因此出现了**Nonebot**这个东西，它采用异步I/O，利用WebSocket进行通信，效率很高

这东西底层是基于[python-aiocqhttp库](https://github.com/cqmoe/python-aiocqhttp)的，这个库其实就是个python的SDK了，只不过Nonebot又封装了一些网络交互功能

使用之前得先下载酷Q以及CQHTTP插件，然后pip安装库

```python
pip install nonebot
```

---

然而这个repo下面就只是我自己写得一个机器人脚本罢了（大部分都是爬虫+用户交互函数）

更多功能敬请期待。。。QAQ