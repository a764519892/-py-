# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re
#from pygtrans import Translate
from googletrans import Translator
import os
translator =Translator(service_urls=['translate.google.cn'])
def dizhi(wenjian_dizhi):
    for root, dirs, files in os.walk(wenjian_dizhi, topdown=True):
        for item in files:
            dandu = item.split('.')[-1]
            if dandu == 'py':
                print("文件名   ={}\{}".format(root, item))
                di=root+'\\'+item
                del_zs(di)

        for item in dirs:
            dandu = item.split('.')[-1]
            if dandu == 'py':
                print("文件名   ={}\{}".format(root, item))
                di = root + '\\' + item
                del_zs(di)
def del_zs(wen_ming):
    with open(wen_ming, "r",encoding='utf-8') as file:
        file_read = file.read()
        en_content = re.findall('#.*?\n', file_read, re.S)
        new_file_read = file_read
        print(en_content)
        for i in en_content:
            with open(wen_ming, "w+", encoding='UTF-8') as new_file:
                new_file.write(new_file_read)
                new_file_read = new_file_read.replace(i, '#'+fanyi(i.replace('\n', '')).strip()+i)
                #new_file_read = new_file_read.replace(i, '#\n')

    with open(wen_ming, "r",encoding='utf-8') as file:
        file_read = file.read()
        en_content = re.findall('""".*?"""', file_read, re.S)
        new_file_read = file_read
        print(en_content)
        for i in en_content:
            with open(wen_ming, "w+", encoding='UTF-8') as new_file:
                new_file_read = new_file_read.replace(i, '"""\n' + fanyi(i.replace('\n', '')).strip().strip(
                    "“”") + '\n"""'+i)
                new_file.write(new_file_read)
        #return en_content

def fanyi(neirong):
    #client= Translate()
    #fanyi =client.translate(neirong)
    translation =translator.translate(neirong,'zh-CN')
    #print(fanyi.translatedText)
    #print(translation.text)
    return translation.text
    #return fanyi
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #del_zs()
    #fanyi('hello')
    t= input('请输入总文件夹地址,剩下交给天意，自动机翻，可能翻译不准确，但保留英文，可能出错，提前备份好文件。\n地址：')   #类似 D:\Study\pythonProject\py注释翻译\template
    dizhi(t)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
