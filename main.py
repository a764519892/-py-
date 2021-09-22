# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re
from pygtrans import Translate
from googletrans import Translator

translator =Translator(service_urls=['translate.google.cn'])
def del_zs():
    with open(r"webapp.py", "r") as file:
        file_read = file.read()
        en_content = re.findall('#.*?\n', file_read, re.S)
        new_file_read = file_read
        print(en_content)
        for i in en_content:
            with open(r"webapp_1.py", "w+", encoding='UTF-8') as new_file:
                new_file.write(new_file_read)
                new_file_read = new_file_read.replace(i, '#'+fanyi(i.replace('\n', '')).strip()+i)
                #new_file_read = new_file_read.replace(i, '#\n')

    with open(r"globals.py", "r") as file:
        file_read = file.read()
        en_content = re.findall('""".*?"""', file_read, re.S)
        new_file_read = file_read
        print(en_content)
        for i in en_content:
            with open(r"globals_1.py", "w+", encoding='UTF-8') as new_file:
                new_file_read = new_file_read.replace(i, '"""\n' + fanyi(i.replace('\n', '')).strip().strip(
                    "“”") + '\n"""')
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
    del_zs()
    #fanyi('hello')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
