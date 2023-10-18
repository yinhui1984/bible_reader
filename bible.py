
import data_source


# 是否在初始化时下载完整书籍内容
IS_DOWNLOAD_FULL_BOOK_WHEN_INIT = False

def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance


# 圣经章节，比如创世记第一章
class BibleCharpter:
    def __init__(self, bookName, charpterIndex):
        self.bookName = bookName
        self.charpterIndex = charpterIndex
        self.content= data_source.get_bible_charpter_content_and_note(self.bookName, self.charpterIndex) if IS_DOWNLOAD_FULL_BOOK_WHEN_INIT else ""
        
    def get_content(self):
        if self.content == "":
            self.content = data_source.get_bible_charpter_content_and_note(self.bookName, self.charpterIndex)
        data_source.save_status(self.bookName, self.charpterIndex)
        return self.content

    def to_dict(self):
        return {
            "charpterIndex": self.charpterIndex,
            "bookName": self.bookName
        }

# 圣经书，比如创世记，出埃及记
class BibleBook:
    def __init__(self, link, bookName, maxCharpterIndex):
        self.link = link
        self.bookName = bookName
        self.maxCharpterIndex = maxCharpterIndex
        self.charpters = []
        for i in range(1, maxCharpterIndex + 1):
            self.charpters.append(BibleCharpter(bookName, i))
    
    def to_dict(self):
        charptersDict = []
        for charpter in self.charpters:
            charptersDict.append(charpter.to_dict())
        return {
            "link": self.link,
            "bookName": self.bookName,
            "maxCharpterIndex": self.maxCharpterIndex,
            "charpters": charptersDict
        }

# 圣经卷，比如旧约，新约
class BiblePart:
    def __init__(self, links):
        self.name = "旧约"
        self.books = []
        for link, bookName, maxCharpterIndex in links:
            self.books.append(BibleBook(link, bookName, maxCharpterIndex))
    def to_dict(self):
        booksDict = []
        for book in self.books:
            booksDict.append(book.to_dict())
        return {
            "name": self.name,
            "books": booksDict
        }


@singleton
class Bible:
    def __init__(self):
        self.OLD_TESTAMENT = BiblePart(data_source.OLD_TESTAMENT_LINKS)
        # self.NEW_TESTAMENT = BiblePart(data_source.NEW_TESTAMENT_LINKS)
    
    def get_charpter_content(self, bookName, charpterIndex):
        for book in self.OLD_TESTAMENT.books:
            if book.bookName == bookName:
                return book.charpters[charpterIndex - 1].get_content()
    
    def to_dict(self):
        dicts = []
        for book in self.OLD_TESTAMENT.books:
            dicts.append(book.to_dict())
        # for book in self.NEW_TESTAMENT.books:
        #     dicts[book.bookName] = book.to_dict()
        return {
            "books": dicts,
        }
    

BIBLE_INSTNACE = Bible()


