# !/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib.request
from bs4 import BeautifulSoup
import sys


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
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    stockTitle = soup.find("span", id="stock_title")
    stockCode = soup.find("span", id="stock_code")
    feature = soup.find("div", class_="tokusyoku")
    feature_ = feature.find("p", class_="fontnormal")
    consolidatedOperations = feature.find("span", class_="fontsmall")
    params = soup.find("div", class_="gradation_box")
    spans = params.findAll("span")
    webPage = params.findAll("a")[1].get("href")
    kihon = soup.find("div", class_="kihon")

    print("会社名: {0}".format(stockTitle.text))
    print("証券コード: {0}".format(stockCode.text))
    print("特色: {0}".format(feature_.text.replace("【特色】", "").strip()))
    print("連結事業: {0}".format(consolidatedOperations.text.replace("【連結事業】", "").strip()))
    print("市場: {0}".format(spans[0].string.strip()))
    print("銘柄: {0}".format(spans[1].string.strip()))
    print("銘柄: {0}".format(spans[3].string.strip()))
    print("会社HP: {0}".format(webPage))
    th = kihon.findAll("th")
    for elem in th:
        for t in elem.text.split():
            if "【上場】" in t:
                print("上場: {0}".format(t.replace("【上場】", "").strip()))
            elif "【設立】" in t:
                print("設立: {0}".format(t.replace("【設立】", "").strip()))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("コマンドを入れてください")
        exit(1)
    cmd = sys.argv[1]
    if cmd == "download":
        download()
    elif cmd == "getinfo":
        getinfo()
