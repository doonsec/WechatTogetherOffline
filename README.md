# WechatTogetherOffline
微信聚合在线演示 http://wechat.doonsec.com

![gif动态使用效果图](/img/licecap.gif)


## 当前版本信息

- V.0.1.2 Beta


## 介绍

当我们看过一篇公众号文章忘记收藏，那天想找的时候可能已经忘了是那个公众号的那篇历史文章了。

**洞见微信聚合**是一个收录安全圈公众号历史文章链接的工具。帮助使用者根据关键字快速找到公众号的历史文章。解决微信`搜一搜`搜索信息不全面的困扰。


- **数据全**：目前整理数据已有10W+，每月数据增量大约5000篇。
- **速度快**：检索结果1s出现，更有多种查询语法，可根据源码魔改查询方式。
- **轻安装**：使用python开发，安装简便，docker一步搞定，可在`win`+`mac`+`linux`平台快速部署

数据库信息的不足肯定会成为一个诟病的地方。前期数据的收录相对局限，需要多人提交维护一个相对全面的公众号列表。


## 部署

本项目提供较大的数据源，故源码与数据分离。部署时候需要分别下载这两部分内容。

**本地安装**

语言选择:
 - python 3.5+

步骤：
1. 下载源码

```
https://github.com/doonsec/WechatTogetherOffline.git
```
2. 下载文章数据库--`wechat.db`

```
链接：https://pan.baidu.com/s/1YHpyqgYCS6asiCy8t0U17w 
提取码：doon
```

3. 移动下载的数据库`wechat.db`至目录`src/db`下


4. 安装python第三方库

```
cd src
pip install -r requirements.txt
```
5. 运行

```
cd src
python app.py
```
6. 打开浏览器，访问`127.0.0.1:8000`

部署完成。

**docker部署**

*方法一*

步骤：
1. 下载源码

```
https://github.com/doonsec/WechatTogetherOffline.git
```
2. 下载文章数据库--`wechat.db`

```
见上
```

3. 移动下载的数据库`wechat.db`至目录`src/db`下

4. 部署docker
    生成镜像
    ```
    docker build -t 'wechattogether' .
    ```
    运行容器

    ```
    docker run  -name doonsec_wechat -p 8000:8000 wechattogether -d
    ```
6. 打开浏览器，访问`127.0.0.1:8000`

部署完成。

*方法二*

步骤：
1. 下载源码

```
https://github.com/doonsec/WechatTogetherOffline.git
```
2. 下载文章数据库--`wechat.db`

```
见上
```

3. 移动下载的数据库`wechat.db`至目录`src/db`下

4. 执行docker-compose.yml文件
```
docker-compose up -d
```
5. 打开浏览器，访问`127.0.0.1:8000`

部署完成。



## 界面展示

**首页展示**

![](/img/index.jpg)

**单个公众号文章列表**

![](/img/account_article_list.jpg)

**关键字索引**
支持`|`、`&`语法索引
![](/img/search.jpg)

**公众号展示**
![](/img/account.jpg)


## 版本迭代

- v.0.1.2 修复公众号展示错误
- v.0.1.1 修复公众号展示错误
- v.0.1.0 初始化项目

## 贡献
you don`t

![](img/donate.png)


