# 简介
抓取互联网上最新热映的电影名称及票房信息（默认8小时更新一次数据）

数据源地址： http://58921.com/ 

# 安装
放入 <config directory>/custom_components/ 目录

# 配置
**Example configuration.yaml:**
```yaml
sensor:
  - platform: hotmovies
    name: 热映电影
```


# 前台界面
原始的界面是这样的，只能看到数量

![avatar](https://github.com/aalavender/HotMovies/blob/master/1.PNG)

建议采用[list-card](https://github.com/custom-cards/list-card)进行展示，效果是这样的

![avatar](https://github.com/aalavender/HotMovies/blob/master/2.PNG)
