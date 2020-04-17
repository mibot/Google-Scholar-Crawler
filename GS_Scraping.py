import re
import time
from random import randint
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import requests
# from GenerateKeywords import keywords
from user_agent_list import get_random_ua
from proxy_list_gen import get_random_proxy
import pandas as pd
import unicodedata

requests.packages.urllib3.disable_warnings()

# k = keywords()

keywords = pd.read_csv('keywords.csv', sep="\t", encoding="utf-8")

SCHOLARS_BASE_URL = 'https://scholar.google.com'

# since = 2017
# to = 2017

# index = 12
# year_s = 2017


# query = '"' + k[0] + '"' + ' +' + k[1] + ' +' + k[2]

# for index, row in keywords.iterrows():
for index in range(11, 12):

    year_s = 2019

    papers = []

    row = keywords.iloc[index]

    query = '"' + row[0] + '"' + ' +' + row[1] + ' +' + row[2]

    params = urlencode(
        {'q': query.lower()},
        "UTF-8")

    # url = SCHOLARS_BASE_URL + "/scholar?hl=en&as_sdt=1%2C5&as_ylo=2017&as_vis=1&" + params

    # url = SCHOLARS_BASE_URL + "/scholar?hl=en&as_sdt=1%2C5&as_ylo=2017&as_yhi=2017&as_vis=1&" + params
    # url = SCHOLARS_BASE_URL + "/scholar?hl=en&as_sdt=1%2C5&as_ylo=2018&as_vis=1&" + params

    # url = SCHOLARS_BASE_URL + "/scholar?hl=en&as_sdt=1%2C5&as_ylo=2017&as_yhi=2017&as_vis=1&" + params
    # url = SCHOLARS_BASE_URL + "/scholar?hl=en&as_sdt=1%2C5&as_ylo=2018&as_yhi=2018&as_vis=1&" + params
    url = SCHOLARS_BASE_URL + "/scholar?hl=en&as_sdt=1%2C5&as_ylo=2019&as_vis=1&" + params

    print(url)

    total_items = 0
    while True:
        ua = str(get_random_ua())
        print(ua)
        # headers = {
        #     'User-Agent': ua
        # }
        proxy = str(get_random_proxy())
        print(proxy)
        # proxies = {
        #     "http": "http://%s" % proxy,
        # }
        try:
            response = requests.get(
                url,
                headers={
                    'User-Agent': ua
                },
                proxies={
                    "http": "http://%s" % proxy,
                }
                # ,
                # verify=False
            )
        except:
            print("Connection refused")
            time.sleep(5)
            continue

        print(response.status_code)
        if response.status_code == 200:

            data = response.text
            soup = BeautifulSoup(data, "html.parser")

            items = soup.find_all('div', {'class': 'gs_r gs_or gs_scl'})

            if items:

                # items = soup.find_all('div', {'class': 'gs_ri'})
                for item in items:
                    title = ""
                    author = ""
                    source = ""
                    main_link = ""
                    direct_link = ""

                    link = item.find('h3', class_='gs_rt')
                    author = item.find('div', class_='gs_a')
                    try:
                        pdf = item.find('div', class_='gs_ggs gs_fl')
                    except:
                        pdf = ""


                    titulo = item.find('h3',class_='gs_rt')

                    title = (re.sub(".*\\]", "", link.text)).lstrip()

                    # remove ... in author

                    author = author.text.replace("… ", " ").replace(' …', '').replace(' … ', ' ')
                    author = unicodedata.normalize("NFKD", author)

                    year = ""
                    if len(author.split(" - ")) == 3:
                        year = author.split(" - ")[1]
                        source = author.split(" - ")[2]
                        if len(year.split(",")) == 2:
                            year = year.split(",")[1]
                            # year = re.findall(r"\b\d+\b", year)
                            # year = map(int, year)
                            year = str(year).strip("[]").strip("''").strip()
                    else:
                        source = author.split(" - ")[1]

                    author = author.split(" - ")[0]

                    url_pdf = ""
                    if pdf:
                        url_pdf = pdf.find('a')['href']
                        direct_link = pdf.find('a')['href']

                    if link.find('a'):
                        main_link = link.find('a')['href']

                    # if url_pdf:
                    #     source = url_pdf.split("/")[0] + "//" + url_pdf.split("/")[2]

                    other = item.find('div', class_='gs_ri').find('div', class_='gs_fl')

                    other_text = other.text.strip()
                    cited = ""
                    if 'Cited' in other_text:
                        cited = re.findall('[A-Z][^A-Z]*', other_text)[0].strip()
                        cited = re.findall(r"\b\d+\b", cited)[0]

                    related_links = ""
                    all_version_links = ""
                    for row in [a['href'] for a in other.find_all('a')]:
                        if not related_links:
                            if 'related' in row:
                                related_links = row
                                continue
                        if not all_version_links:
                            if 'cluster' in row:
                                all_version_links = row
                                continue

                    print('Query:', index + 1, #0
                          '\nPaper title:', title, #1
                          '\nAuthor(s):', author, #2
                          '\nYear:', year, #3
                          '\nSource:', source, #4
                          '\nMain link:', main_link, #5
                          '\nCited:', cited, #6
                          '\nRelated:', related_links, #7
                          '\nAll Versions:', all_version_links, #8
                          '\nDirect link:', direct_link, #9
                          '\n---')

                    papers.append(
                        (index + 1, title, author, year, source, main_link, cited, related_links, all_version_links,
                         direct_link))

                    total_items += 1

                try:
                    url_item = soup.find('td', {'align': 'left'})
                    url = SCHOLARS_BASE_URL + url_item.find('a').get('href')

                    print(url)
                except:
                    break
                time.sleep(randint(1, 6))
            else:

                captcha = soup.find_all('div', {'id': 'gs_captcha_ccl'})

                if not captcha:
                    break
        else:
            time.sleep(30)

    print("Total paper(s):", total_items)
    df = pd.DataFrame(papers,
                      columns=['query_id', 'title', 'author', 'year', 'source', 'main_link', 'cited', 'related_links',
                               'all_version_links', 'direct_link'])
    # df.to_csv("data/csv/unresolved_papers_%s.csv" % (index + 1), index=None, encoding='utf-8', sep="\t")
    df.to_csv("data/csv/unresolved_papers_%s_%s.csv" % (index + 1, year_s), index=None, encoding='utf-8', sep="\t")
