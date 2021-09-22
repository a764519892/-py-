import os
'''
文件目录位置
D://test/a.txt
D://test/1
D://test/1/1_1
D://test/1/1_1/1_2
D://test/1/1_1/1_2_2
D://test/1/1_1/1_2.txt
D://test/1/1_1/1_2_2/1_2_2.txt
D://test/1/1_1/1_2/1_3
D://test/1/1_1/1_2/1_3.txt
'''
# print("-----------------------------------------------topdown=False")
# for root, dirs, files in os.walk(r"E:\python_project\remi-app-template", topdown=False):
#     for item in files:
#         print("文件名   =", item)
#     for item in dirs:
#         print("文件夹名 =", item)
# print("-----------------------------------------------topdown=True")
for root, dirs, files in os.walk(r"E:\python_project\remi-app-template", topdown=True):
    for item in files:
        dandu=item.split('.')[-1]
        if  dandu == 'py':

            print("文件名   ={}\{}".format(root,item))
    for item in dirs:
        dandu = item.split('.')[-1]
        if dandu == 'py' :
            print("文件名   ={}\{}".format(root,item))