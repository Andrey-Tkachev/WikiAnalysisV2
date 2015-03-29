__author__ = 'Андрей'

from urllib import request
import bz2


lang = 'lv'
dump_of_wiki_address = "http://dumps.wikimedia.org/%swiki/latest/%swiki-latest-pages-articles-multistream.xml.bz2" % (lang, lang)


class XmlParser(object):
    def __init__(self):
        self.page_data = []
    def start(self, tag, attrib):
        self.is_title = True if tag == 'Title' else False
    def end(self, tag):
        pass
    def data(self, data):
        if self.is_title:
            self.text.append(data.encode('utf-8'))
    def close(self):
        return self.text



def get_html_from_url(url):
    try:
        conn = request.urlopen(url)
        html = (conn.read()).decode('UTF-8')
    except Exception:
        return ""
    return html

def get_date_of_latest_dump():
    dumps_page = get_html_from_url('http://dumps.wikimedia.org/%swiki/' % (lang))

    latest_dump_date = dumps_page.split('</a>')
    latest_dump_date = (latest_dump_date[-1].split('</pre>')[-2]).rstrip()
    latest_dump_date = latest_dump_date.replace(':', '')
    latest_dump_date = latest_dump_date.replace(' ', '')[:-1]

    return latest_dump_date


def download_and_decompress_latest_dump():
     return bz2.decompress(request.urlopen(dump_of_wiki_address).read())

def update_wiki_dump():
    """ Возвращает название актуального дампа википедии"""
    latest_dump_date = get_date_of_latest_dump()

    try:
        file = open('ini.txt', 'r')
        date_of_last_processed_dump = file.readline().rstrip()

        if date_of_last_processed_dump == latest_dump_date:
            return date_of_last_processed_dump

    except:
        pass

    file = open("%s.xml" % (latest_dump_date), "wb")
    file.write(download_and_decompress_latest_dump())
    file.close()

    ini_file = open("ini.txt", "w")
    ini_file.write(latest_dump_date)
    ini_file.close()
    return latest_dump_date


def analysis_dump(dump_path):
    

def main():
    update_wiki_dump()
    return 0


if __name__ == '__main__':
    main()