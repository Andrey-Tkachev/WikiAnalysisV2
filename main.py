__author__ = 'Андрей'

import urllib
from urllib import request
import bz2
import os
from xml.etree.ElementTree import iterparse

lang = 'lv'
dump_of_wiki_address = "http://dumps.wikimedia.org/%swiki/latest/%swiki-latest-pages-articles-multistream.xml.bz2" % (lang, lang)


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
    site = request.urlopen(dump_of_wiki_address)
    print('будет загружено', site.info()['Content-Length'], 'байт')
    return bz2.decompress(request.urlopen(dump_of_wiki_address).read())

def update_wiki_dump():
    """ Возвращает название актуального дампа википедии"""
    latest_dump_date = get_date_of_latest_dump()

    try:
        file = open("%s.date" % (lang), 'r')
        if file.readline().rstrip() != latest_dump_date:
            os.remove(lang)
        else:
            return lang + '.xml'
    except:
        pass

    file = open("%s.xml" % (lang), "wb")
    file.write(download_and_decompress_latest_dump())
    file.close()
    lang_info_file = open("%s.date" % (lang), "w")
    print(latest_dump_date, file=lang_info_file)
    lang_info_file.close()

    return lang + '.xml'


def analysis_dump(dump_path):
    articles_of_interest = []
    context = iterparse(dump_path, events=('end',))
    article_title = ""
    num_of_tables = 0
    for event, elem in context:
        if elem.tag[-4:] == 'page':
            if num_of_tables > 20:
                articles_of_interest.append((num_of_tables, article_title))
                print('В результат добавлена новая статья')
        elif elem.tag[-5:] == 'title':
            article_title = elem.text
        elif elem.tag[-4:] == 'text':
            if elem.text != None and article_title[:7] != 'Veidne:':
                num_of_tables = len(elem.text.split('{|')) - 1
        else:
            elem.clear()
    del context
    return articles_of_interest

def create_HTML(num_of_table_and_titles):
    i = 0
    color = ["GhostWhite", "WHITE"]
    color2 = ['WhiteSmoke', 'white']
    with open('Result.html', 'w', encoding='UTF-8') as f:
        print("<html xmlns=\"http://www.w3.org/1999/xhtml\"> "
                   "<head>"
                      "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/>"
                      "<title>Таблицы</title>"
                   "</head>"
                   "<body>"
                       "<table>", file=f)
        for nt in num_of_table_and_titles:
            print("<tr>"
                   "<td bgcolor=\"%s\"><a href=http://%s.wikipedia.org/wiki/%s>%s</a></td>"
                   "<td bgcolor=\"%s\">%s</a></td>"
                   "</tr>" % (color[i], lang, nt[1].replace(' ', '_'), nt[1], color2[i], str(nt[0])), file=f)
            i = (i + 1) % 2

        print("</table>"
              "</body>"
              "</html>", file=f)


def main():
    dump_path = update_wiki_dump()
    articles_of_interest = analysis_dump(dump_path)
    articles_of_interest.sort()
    create_HTML(articles_of_interest)
    return 0


if __name__ == '__main__':
    main()