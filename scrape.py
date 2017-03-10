# !/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import time
import urllib.request

import MySQLdb
from bs4 import BeautifulSoup


def download():
    url = sys.argv[2]
    if len(url) == 0:
        print("URLを入力してください")
        return
    title = "data.html"
    if len(sys.argv) > 3:
        title = sys.argv[3]
    urllib.request.urlretrieve(url, "{0}".format(title))


def getinfo():
    url = sys.argv[2]
    if len(url) == 0:
        print("URLを入力してください")
        return
    parse(url)


def parse(url):
    try:
        html = urllib.request.urlopen(url)
    except:
        print("URL取得に失敗しました")
        return
    soup = BeautifulSoup(html, "html.parser")
    stockTitle = soup.find("span", id="stock_title")
    stockCode = soup.find("span", id="stock_code")
    feature = soup.find("div", class_="tokusyoku")
    feature_ = feature.find("p", class_="fontnormal")
    try:
        featureText = feature_.text.replace("【特色】", "").strip()
    except:
        featureText = ""
    try:
        consolidatedOperations = feature.find("span", class_="fontsmall").text.replace("【連結事業】", "").strip()
    except:
        consolidatedOperations = ""
    params = soup.find("div", class_="gradation_box")
    spans = params.findAll("span")
    webPage = params.findAll("a")[1].get("href")
    kihon = soup.find("div", class_="kihon")

    print("会社名: {0}".format(stockTitle.text))
    print("証券コード: {0}".format(stockCode.text))
    print("特色: {0}".format(featureText))
    print("連結事業: {0}".format(consolidatedOperations))
    print("市場: {0}".format(spans[0].string.strip()))
    print("銘柄: {0}".format(spans[1].string.strip()))
    print("銘柄: {0}".format(spans[3].string.strip()))
    print("会社HP: {0}".format(webPage))

    params = {}
    try:
        th = kihon.findAll("th")
        for elem in th:
            for t in elem.text.split():
                for key in ["上場", "設立", "本社", "従業員", "証券", "銀行"]:
                    if "【{0}】".format(key) in t:
                        params[key] = t.replace("【{0}】".format(key), "").strip()
                        print("{0}: {1}".format(key, t.replace("【{0}】".format(key), "").strip()))
    except:
        print("基本情報の取得に失敗しました")
    try:
        gyoseki = soup.find("table", class_="syuyou")
        records = gyoseki.findAll("tr")
        mainHeaders = []
        for r in records[:-1]:
            headers = r.findAll("th")
            if len(headers) > 1:
                # 表のヘッダー
                mainHeaders = list(map(lambda x: x.text.strip(), headers))[1:]
                # for h in mainHeaders:
                #    print("header:{0}".format(h))
            else:
                # レコードのヘッダー
                for h in headers:
                    print("{0}:".format(h.text.strip()))
                for h, d in zip(mainHeaders, r.findAll("td")):
                    print(h, d.text)
    except:
        print("業績の取得に失敗しました")
    right = soup.find("div", id="tabmenu_right")
    next_num = right.find("a").text

    connector = MySQLdb.connect(host="localhost", db="shikiho_data", user="root", passwd="", charset="utf8")
    cursor = connector.cursor()

    sql = u"insert into company_data values({0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14})".format(
        0,
        "\"{0}\"".format(stockTitle.text),
        int(stockCode.text),
        "\"{0}\"".format(featureText),
        "\"{0}\"".format(consolidatedOperations),
        "\"{0}\"".format(spans[0].string.strip()),
        "\"{0}\"".format(spans[1].string.strip()),
        "\"{0}\"".format(spans[3].string.strip()),
        "\"{0}\"".format(webPage),
        "\"{0}\"".format(params.get("上場", "")),
        "\"{0}\"".format(params.get("設立", "")),
        "\"{0}\"".format(params.get("本社", "")),
        "\"{0}\"".format(params.get("従業員", "")),
        "\"{0}\"".format(params.get("証券", "")),
        "\"{0}\"".format(params.get("銀行", ""))
    )
    print(sql)
    cursor.execute(sql)

    connector.commit()

    cursor.close()
    connector.close()
    return next_num


def crawl(start=3690, end=99999):
    prefix = "https://shikiho.jp/tk/stock/info/"
    next_num = str(start)
    while next_num is not None and int(next_num) <= end:
        next_num = parse(prefix+next_num)
        time.sleep(5)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("コマンドを入れてください")
        exit(1)
    cmd = sys.argv[1]
    if cmd == "download":
        download()
    elif cmd == "getinfo":
        getinfo()
    elif cmd == "crawl":
        crawl()
