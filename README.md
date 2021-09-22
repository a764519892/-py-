# translate-py-annotation
首先安装 ：pip install googletrans==4.0.0-rc1
利用谷歌翻译，翻译py文档注释
主文件 manin.py  。
运行 输入文件地址：类似D:\Study\pythonProject\py注释翻译\-py-   
会自动翻译-py-文件下，所有子文件夹下的.py文件下  #后面的文字 和 ''' ''' 之间的文字为中文。
保留原有的英文在后面，文件出错后，复制后面原有英文替换回去就好。
没有使用多线程，怕请求频率太高，谷歌那封了IP。
