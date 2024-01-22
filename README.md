# WeChatMsg mini extension

### 前言：

注意：这并不是**WeChatMsg（留痕）**官方，只是一个对微信年度报告感兴趣的人写的一个小脚本😊

这个扩展程序可以让你生成你自己的微信年度报告，包括你的聊天总数，亲密关系排行，聊天内容分析，聊天时间分布，等等，还可以生成一些统计数据，让你更加了解你的微信生活👍

我一眼就被WeChatMsg这个项目迷住了，作为一个无比期待看各种软件年度报告的人，微信的年度报告简直是我梦寐以求的，然而可能碍于隐私，微信官方并未开发此功能😔；

在使用了WeChatMsg后，里面有好多厉害的功能都没有开放，于是按耐不住就自己做了一个😎

这个小脚本是赶时间草草写出来的，可能有一些未知的Bug，不过代码也比较简单易懂，可以自己改改，问题也不大🙌

如果你有更好的想法，可以联系我：NarratorCMH@aliyun.coms



### 功能介绍：

该脚本能根据**WeChatMsg（留痕）**导出的全局CSV数据生成一份微信使用报告（是统计了能查询到的所有记录哦，并不止局限于一年的数据，数据量越大，报告的准确率就越高）

该程序统计了你的有效联系人个数和群聊个数，使用微信聊天的时间月份频率分布，你发送的消息类型分布，金钱交易密切的联系人统计...

![3](.\Pictures\3.png)

![2](.\Pictures\2.png)

![4](.\Pictures\4.png)

![5](.\Pictures\5.png)

![1](.\Pictures\1.png)



### 使用方法：

由于该程序只是一个脚本文件，所以执行起来比较简单，只需要电脑有python环境和pandas库就可以了

```shell
#安装pandas库
pip install pandas	
```

首先需要微信数据库数据，使用**WeChatMsg（留痕）**的导出全部聊天记录，将导出的csv文件放在任意位置均可

![6](.\Pictures\6.png)

下载并打开该库中的`mingwechat.py`文件，将第九行的地址改为你的csv文件地址

运行此py文件并稍等一会儿即可在csv文件同目录下生成一个名为微信使用报告的HTML文件，用浏览器打开即可
