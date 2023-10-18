from flask import jsonify
import json
import requests
import chardet
import re 
import os
from bs4 import BeautifulSoup
# http://www.godcom.net/lingxiu/
OLD_TESTAMENT_LINKS = [
("http://www.godcom.net/lingxiu/OT01genesis/OT01ge_", "创世记", 50),
("http://www.godcom.net/lingxiu/OT02exodus/OT02ex_", "出埃及记", 40),
("http://www.godcom.net/lingxiu/OT03leviticus/OT03lev_", "利未记",27),
("http://www.godcom.net/lingxiu/OT04numbers/OT04nu_", "民数记",30 ),
("http://www.godcom.net/lingxiu/OT05deuteronomy/OT05dt_", "申命记", 30),
("http://www.godcom.net/lingxiu/OT06joshua/OT06jos_", "约书亚记",24),
("http://www.godcom.net/lingxiu/OT07judges/OT07jdg_", "士师记",21),
("http://www.godcom.net/lingxiu/OT08ruth/OT08ru_", "路得记",4),
("http://www.godcom.net/lingxiu/OT091samuel/OT091sa_", "撒母耳记上",31),
("http://www.godcom.net/lingxiu/OT102samuel/OT102sa_", "撒母耳记下",24),
("http://www.godcom.net/lingxiu/OT111kings/OT111ki_", "列王纪上",22),
("http://www.godcom.net/lingxiu/OT122kings/OT122ki_", "列王纪下",25),
("http://www.godcom.net/lingxiu/OT131chronicles/OT131ch_", "历代志上",29),
("http://www.godcom.net/lingxiu/OT142chronicles/OT142ch_", "历代志下",36),
("http://www.godcom.net/lingxiu/OT15ezra/OT15ezr_", "以斯拉记",10),
("http://www.godcom.net/lingxiu/OT16nehemiah/OT16ne_", "尼希米记",13),
("http://www.godcom.net/lingxiu/OT17esther/OT17est_", "以斯帖记",10),
("http://www.godcom.net/lingxiu/OT18job/OT18job_", "约伯记",42),
("http://www.godcom.net/lingxiu/OT19psalms/OT19ps_", "诗篇",150),
("http://www.godcom.net/lingxiu/OT20proverbs/OT20pr_", "箴言",30),
("http://www.godcom.net/lingxiu/OT21ecclesiastes/OT21ecc_", "传道书",12),
("http://www.godcom.net/lingxiu/OT22songofsongs/OT22ss_", "雅歌",8),
("http://www.godcom.net/lingxiu/OT23isaiah/OT23isa_", "以赛亚书",66),
("http://www.godcom.net/lingxiu/OT24jeremiah/OT24jer_", "耶利米书",52),
("http://www.godcom.net/lingxiu/OT25lamentations/OT25la_", "耶利米哀歌",5),
("http://www.godcom.net/lingxiu/OT26ezekiel/OT26eze_", "以西结书",48),
("http://www.godcom.net/lingxiu/OT27daniel/OT27da_", "但以理书",12),
("http://www.godcom.net/lingxiu/OT28hosea/OT28hos_", "何西阿书",14),
("http://www.godcom.net/lingxiu/OT29joel/OT29joel_", "约珥书",3),
("http://www.godcom.net/lingxiu/OT30amos/OT30am_", "阿摩司书",9),
("http://www.godcom.net/lingxiu/OT31obadiah/OT31ob_", "俄巴底亚书",1),
("http://www.godcom.net/lingxiu/OT32jonah/OT32jnh_", "约拿书",4),
("http://www.godcom.net/lingxiu/OT33micah/OT33mic_", "弥迦书",7),
("http://www.godcom.net/lingxiu/OT34nahum/OT34na_", "那鸿书",3),
("http://www.godcom.net/lingxiu/OT35habakkuk/OT35hab_", "哈巴谷书",3),
("http://www.godcom.net/lingxiu/OT36zephaniah/OT36zep_", "西番雅书",3),
("http://www.godcom.net/lingxiu/OT37haggai/OT37hag_", "哈该书",2),
("http://www.godcom.net/lingxiu/OT38zechariah/OT38zec_", "撒迦利亚书",14),
("http://www.godcom.net/lingxiu/OT39malachi/OT39mal_", "玛拉基书",4),
]


NEW_TESTAMENT_LINKS = []

# enum Old Testament and New Testament
class BibleParts:
    OLD_TESTAMENT = 1
    NEW_TESTAMENT = 2
    ALL = 3


# def get_bible_parts(theBibleParts):
#     if theBibleParts == BibleParts.OLD_TESTAMENT:
#         json_data = [{"link": link, "title": title} for link, title in OLD_TESTAMENT_LINKS]
#     elif theBibleParts == BibleParts.NEW_TESTAMENT:
#         json_data = [{"link": link, "title": title} for link, title in NEW_TESTAMENT_LINKS]
#     else:
#         return ""
#     json_string = json.dumps(json_data, ensure_ascii=False, indent=4)
#     return json_string


def get_bible_book_link_by_name(theBookName):
    for link, title, _ in OLD_TESTAMENT_LINKS:
        if title == theBookName:
            return link
    for link, title in NEW_TESTAMENT_LINKS:
        if title == theBookName:
            return link
    return ""


def get_bible_charpter_link(theBookName, theCharpterIndex):
    theBookLink = get_bible_book_link_by_name(theBookName)
    if theBookLink == "":
        return ""
    theCharpterLink = theBookLink + "chapter" + str(theCharpterIndex) + ".htm"
    print(theCharpterLink)
    return theCharpterLink

def get_bible_charpter_note_link(theBookName, theCharpterIndex):
    pass

def get_bible_charpter_content_and_note_link(theBookName, theCharpterIndex):
    chapterUrl = get_bible_charpter_link(theBookName, theCharpterIndex)
    # <frameset rows="200,*">
    # 	<frame src="Chapter/OT01ge_42.htm" tppabs="OT01genesis/Chapter/OT01ge_42.htm" name="OT01ge42">
    # 	<frame src="Note/42_OT01ge.htm" tppabs="OT01genesis/Note/42_OT01ge.htm" name="42_OT01ge">
    # </frameset>
    htmlContent = requests.get(chapterUrl).text
    soup = BeautifulSoup(htmlContent, 'html.parser')
    frameset = soup.find('frameset')
    frames = frameset.find_all('frame')
    contentFrame = frames[0]
    contentLink = contentFrame['src']
    noteFrame = frames[1]
    noteLink = noteFrame['src']
    # get http://www.godcom.net/lingxiu/OT01genesis/ from http://www.godcom.net/lingxiu/OT01genesis/OT01ge_ 
     # Split the string by "/" from the right, once, and take the first part
    linkbase = chapterUrl.rsplit('/', 1)[0]

    return linkbase + "/" + contentLink, linkbase + "/" + noteLink


def get_bible_charpter_content_and_note(theBookName, theCharpterIndex):
    jsonString = read_bible_charpter_content_and_note(theBookName, theCharpterIndex)
    if jsonString == "":
        jsonString = get_bible_charpter_content_and_note_from_web(theBookName, theCharpterIndex)
        save_bible_charpter_content_and_note(theBookName, theCharpterIndex, jsonString)
    return jsonString

# def get_bible_charpter_content_and_note_from_web(theBookName, theCharpterIndex):
#     contentUrl, noteUrl = get_bible_charpter_content_and_note_link(theBookName, theCharpterIndex)
#     content_response = requests.get(contentUrl)
#     note_response = requests.get(noteUrl)

#     # 使用chardet检测编码
#     content_encoding = chardet.detect(content_response.content)['encoding']
#     note_encoding = chardet.detect(note_response.content)['encoding']

#     content = content_response.content.decode(content_encoding)
#     note = note_response.content.decode(note_encoding)

#     # 使用BeautifulSoup解析HTML内容
#     soup_content = BeautifulSoup(content, 'html.parser')
#     soup_note = BeautifulSoup(note, 'html.parser')

#     # 查找HTML中的经文内容
#     verses = []
#     content_rows = soup_content.find_all('tr')
#     for row in content_rows:
#         cols = row.find_all('td')
#         if cols:
#             verse_number = cols[0].get_text(strip=True)
#             verse_text = cols[1].get_text(strip=True)
#             verses.append({"chapter": verse_number, "content": verse_text})

#     # 正则表达式，用于匹配章节号及其后的内容
#     pattern = re.compile(r'^(\d+:\d+(-\d+)?)(.*)')  # 第一个分组为章节号，第二个分组为随后的文本

#     # 解析注释并与经文内容关联
#     notes = {}
#     text_lines = soup_note.get_text("\n", strip=True).split("\n")
#     for line in text_lines:
#         match = pattern.match(line)
#         if match:  # 如果这一行匹配我们的模式
#             chapter_number = match.group(1)  # 章节号
#             text = match.group(3).strip()  # 章节号后的文本，移除首尾的空白字符
#             notes[chapter_number] = text

#     # 将注释与相应的经文关联
#     for verse in verses:
#         chapter_number = verse["chapter"]
#         if chapter_number in notes:
#             verse["note"] = notes[chapter_number]  # 添加注释到对应的经文
#         else:
#             verse["note"] = ""  # 如果没有对应的注释，就添加空字符串

#     # 组织JSON数据
#     json_data = {
#         "book": theBookName,
#         "chapter": str(theCharpterIndex),
#         "verses": verses  # 经文的列表，每个经文包括章节、内容和注释
#     }

#     # 将数据转换为JSON字符串，确保编码正确并格式化输出
#     json_string = json.dumps(json_data, ensure_ascii=False, indent=4)
#     return json_string


def try_decode(theResponse):
    # 使用chardet检测编码
    encoding = chardet.detect(theResponse.content)['encoding']
    try:
        content = theResponse.content.decode(encoding)
    except UnicodeDecodeError:
        # try utf-8, gbk, gb2312, big5, hz
        try:
            content = theResponse.content.decode('utf-8')
        except UnicodeDecodeError:
            try:
                content = theResponse.content.decode('gbk')
            except UnicodeDecodeError:
                try:
                    content = theResponse.content.decode('big5')
                except UnicodeDecodeError:
                    try:
                        content = theResponse.content.decode('hz')
                    except UnicodeDecodeError:
                        content = theResponse.content.decode('gb2312', errors='ignore')
    return content

def get_bible_charpter_content_and_note_from_web(theBookName, theCharpterIndex):
    contentUrl, noteUrl = get_bible_charpter_content_and_note_link(theBookName, theCharpterIndex)
    content_response = requests.get(contentUrl)
    note_response = requests.get(noteUrl)

    content = try_decode(content_response)
    note = try_decode(note_response)

    # 使用BeautifulSoup解析HTML内容
    soup_content = BeautifulSoup(content, 'html.parser')
    soup_note = BeautifulSoup(note, 'html.parser')

    # 查找HTML中的经文内容
    verses = []
    content_rows = soup_content.find_all('tr')
    for row in content_rows:
        cols = row.find_all('td')
        if cols:
            verse_number = cols[0].get_text(strip=True)
            verse_text = cols[1].get_text(strip=True)
            verses.append({"chapter": verse_number, "content": verse_text})

    # 正则表达式，用于匹配章节号及其后的内容
    pattern = re.compile(r'^(\d+:\d+)(-\d+)?(.*)')  # 第一个分组为章节号，第二个分组为可能的范围，第三个分组为随后的文本

    # 解析注释并与经文内容关联
    notes = {}
    text_lines = soup_note.get_text("\n", strip=True).split("\n")
    for line in text_lines:
        match = pattern.match(line)
        if match:  # 如果这一行匹配我们的模式
            start_chapter_number = match.group(1)  # 起始章节号
            range_part = match.group(2)  # 可能的范围部分
            text = match.group(3).strip()  # 章节号后的文本，移除首尾的空白字符

            if range_part:  # 如果存在范围
                start_chapter, start_verse = map(int, start_chapter_number.split(':'))
                end_verse = int(range_part[1:])  # 提取范围的结束部分并转换为整数

                # # 对范围内的所有经文应用相同的注释
                # for verse_num in range(start_verse, end_verse + 1):
                #     chapter_verse_key = f"{start_chapter}:{verse_num}"
                #     notes[chapter_verse_key] = text
                ## 对范围内最后一条经文应用注释
                chapter_verse_key = f"{start_chapter}:{end_verse}"
                notes[chapter_verse_key] = text

            else:
                notes[start_chapter_number] = text

    # 将注释与相应的经文关联
    for verse in verses:
        chapter_number = verse["chapter"]
        if chapter_number in notes:
            verse["note"] = notes[chapter_number]  # 添加注释到对应的经文
        else:
            verse["note"] = ""  # 如果没有对应的注释，就添加空字符串

    # 组织JSON数据
    json_data = {
        "book": theBookName,
        "chapter": str(theCharpterIndex),
        "verses": verses  # 经文的列表，每个经文包括章节、内容和注释
    }

    # 将数据转换为JSON字符串，确保编码正确并格式化输出
    json_string = json.dumps(json_data, ensure_ascii=False, indent=4)
    return json_string


    
def get_save_full_path_of_charpter(theBookName, theCharpterIndex):
    exeFolder = os.path.dirname(os.path.abspath(__file__))
    bookDirectory = os.path.join(exeFolder, os.path.join("DATA",theBookName))
    if not os.path.exists(bookDirectory):
        os.makedirs(bookDirectory)
    return os.path.join(bookDirectory, str(theCharpterIndex) + ".json")

def save_bible_charpter_content_and_note(theBookName, theCharpterIndex, theJsonString):
    fullPath = get_save_full_path_of_charpter(theBookName, theCharpterIndex)
    with open(fullPath, 'w') as file:
        file.write(theJsonString)
        file.close()

def read_bible_charpter_content_and_note(theBookName, theCharpterIndex):
    fullPath = get_save_full_path_of_charpter(theBookName, theCharpterIndex)
    if not os.path.exists(fullPath):
        return ""
    with open(fullPath, 'r') as file:
        json_string = file.read()
        file.close()
    return json_string

def get_save_full_path_of_status():
    exeFolder = os.path.dirname(os.path.abspath(__file__))
    dataFolder = os.path.join(exeFolder, "DATA")
    if not os.path.exists(dataFolder):
        os.makedirs(dataFolder)
    return os.path.join(dataFolder, "status.json")

def save_status(theBookName, theCharpterIndex):
    fullPath = get_save_full_path_of_status()
    dataJson = {
        "bookName": theBookName,
        "charpterIndex": theCharpterIndex
    }
    with open(fullPath, 'w') as file:
        file.write(json.dumps(dataJson, ensure_ascii=False, indent=4))
        file.close()

def get_status():
    fullPath = get_save_full_path_of_status()
    if not os.path.exists(fullPath):
        return {
        "bookName": "创世纪",
        "charpterIndex": "1"
    }
    with open(fullPath, 'r') as file:
        dataJson = json.loads(file.read())
        file.close()
    return dataJson
    


          