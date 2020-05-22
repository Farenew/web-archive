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

# content dirs
scienceDir = "./content/science/"
socialDir = "./content/social/"
newsDir = "./content/news/"

scienceList = list()
socialList = list()
newsList = list()

# 建立content目录和内容的联系
contentDict = dict()
contentDict[scienceDir] = scienceList
contentDict[socialDir] = socialList
contentDict[newsDir] = newsList

# add file entries to content list
for key, value in contentDict.items():
    for subdir, dirs, files in os.walk(key):
        for File in files:
            contentDict[key].append(File)


# 建立static目录和content内容的联系
staticDict = dict()
scienceFiles = "./static/science/"
socialFiles = "./static/social/"
newsFiles = "./static/news/"

staticDict[scienceFiles] = scienceDir
staticDict[socialFiles] = socialDir
staticDict[newsFiles] = newsDir

# 遍历static目录下文件
for key, value in staticDict.items():

    contentDir = staticDict[key]

    for subdir, dirs, files in os.walk(key):
        os.chdir(contentDir)
        contentList = contentDict[contentDir]

        # 如果static目录下文件在content对应目录没有文件，那么在content目录创建文件。
        for File in files:
            # File is XXXXX.html
            title = File.split(".")

            # markdown file Name
            FileName = title[0] + ".md"

            # 如果当前markdown文件在content里没有，那么就创建
            if FileName not in contentList:
                # 构建front matter
                frontMatter = constructFrontMatter(title[0], date, [""], [""])
                link = File.replace(" ", "%20")
                contentPath = contentDir.split("/")

                # 创建文件并写入内容
                with open(FileName, "w", encoding="UTF-8") as f:
                    f.write(frontMatter)
                    f.write('\n')
                    # file content
                    content = "[" + File + "]" + "(/" + str(contentPath[2]) + "/" + link + ")\n"

                    f.write(content)
                    
        os.chdir(iniDir)




        
        


    


