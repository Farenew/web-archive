import os
import re
from datetime import datetime

# function to construct front matter
def constructFrontMatter(title, date, tags, categories):
    frontMatter = dict()
    frontMatter["title"] = "\"" + title + "\""
    frontMatter["date"] = date
    frontMatter["tags"] = tags
    frontMatter["categories"] = categories
    returnString = "---\n"
    for key, value in frontMatter.items():
        returnString += str(key) + ": " + str(value) + "\n"
    returnString += "---\n"
    return returnString

# 初始目录
iniDir = os.getcwd()

# current date and time
date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + "+08:00"


# 构建关于content文件夹的内容列表，按照字典形式存储，字典key是文件夹名称，value是文件夹内容（包括子文件夹内容）
contentDir = "./content"
contentDict = dict()

for subdir, dirs, files in os.walk(contentDir):
    key = subdir.replace(contentDir + '/', '')
    # 如果key不是contentDir目录，且key不是二级子目录（如果是的话，那么其中一定有/）
    if key != '' and key.find('/') == -1:
        contentDict[key] = []

        # 遍历字目录，并且把字目录里的文件加到列表中
        for root, d, filenames in os.walk(subdir):
            for f in filenames:
                contentDict[key].append(f)



# 同样的方法组织staticDir的内容
staticDir = "./static"
staticDict = dict()

# 在黑名单中的文件夹也不会被列入，像是image等文件夹
blackList = ['image']

for subdir, dirs, files in os.walk(staticDir):
    key = subdir.replace(staticDir + '/', '')
    # 如果key不是staticDir目录，且key不是二级子目录（如果是的话，那么其中一定有/）
    if key != '' and key.find('/') == -1 and key not in blackList:
        staticDict[key] = []

        # 遍历子目录，并且把字目录里的文件加到列表中
        for root, d, filenames in os.walk(subdir):
            for f in filenames:
                staticDict[key].append(f)



for key in staticDict:
    curDir = contentDir + '/' + key
    if key not in contentDict.keys():
        contentDict[key] = list()
        os.mkdir(curDir)

    os.chdir(curDir)

    for item in staticDict[key]:

        # 文件名字叫XXXX.html，按照.进行分割
        title = item.split(".")

        # markdown file Name
        FileName = title[0] + ".md"

        if FileName not in contentDict[key]:
            # 构建front matter
            frontMatter = constructFrontMatter(title[0], date, [""], [key])

            link = item.replace(" ", "%20")

            # 创建文件并写入内容
            with open(FileName, "w", encoding="UTF-8") as f:
                f.write(frontMatter)
                f.write('\n')

                # file content
                content = "[" + title[0] + "]" + "(/" + str(key) + "/" + link + ")\n"

                f.write(content)

    os.chdir(iniDir)
    

