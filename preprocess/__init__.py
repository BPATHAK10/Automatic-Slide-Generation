from newspaper import Article
import datetime
import docx2txt

def parseUrl(url):
    article = Article(url)
    article.download()
    article.parse()
    
    # print (article.)
    document = {
        'title': article.title,
        'author': article.authors,
        'date': article.publish_date,
        'text': article.text,
        'bgimage': article.top_image, 
        'images': article.images,
        'html': article.html,
        'summary': {},
    }

    return document

def parseText(text):
    document = {
        'title': 'Title Page',
        'author': 'Aagat Pokhrel',
        'date': datetime.utcnow().date().isoformat(),
        'text': text,
        'bgimage': None, 
        'images': [],
        'html': None,
        'summary': {},
    }
    return document

def parseUpload(upload):

    # combine all the text of the upload dict in one string
    upload = ' '.join(upload.values())

    document = {
        'title': 'Title Page',
        'author': 'Aagat Pokhrel',
        # 'date': datetime.utcnow().date().isoformat(),
        'text': upload,
        'bgimage': None, 
        'images': [],
        'html': None,
        'summary': {},
    }
    return document