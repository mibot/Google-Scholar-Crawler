import re
import contractions
from googleapiclient.discovery import build

from re import sub

from gensim.utils import simple_preprocess
from nltk import word_tokenize, download
from nltk.corpus import stopwords

download('punkt')  # Download data for tokenizer.
stopwords = stopwords.words('english')


def preprocess(doc):
    doc = contractions.fix(doc)
    doc = sub(r'<img[^<>]+(>|$)', " image_token ", doc)
    regex = r"\[tag: (.*?)\]"
    matches = re.finditer(regex, doc, re.MULTILINE | re.IGNORECASE)
    for matchNum, match in enumerate(matches):
        doc = doc.replace(match.group(0), match.group(1))
    doc = sub(r'<[^<>]+(>|$)', " ", doc)
    doc = sub(r'\[img_assist[^]]*?\]', " ", doc)
    doc = sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', " url_token ", doc)
    # return [token for token in simple_preprocess(doc, min_len=0, max_len=float("inf")) if token not in stopwords]
    return [token for token in simple_preprocess(doc, min_len=0, max_len=float("inf"))]


def getService():
    service = build("customsearch", "v1",
                    developerKey="AIzaSyDmL79yOqAxF45mLTDeou9eUqeZFZAM9aw")

    return service


def main(query):
    # pageLimit = 1
    # nPage = 0
    service = getService()
    startIndex = 1
    response = []

    # for nPage in range(0, pageLimit):
    # print("Reading page number:", nPage + 1)

    response.append(service.cse().list(
        q=query,  # Search words
        cx='006634703934633088082:1oucwztl7qs',  # CSE Key
        lr='lang_en',  # Search language
        start=startIndex
    ).execute())
    # try:
    #     startIndex = response[nPage].get("queries").get("nextPage")[0].get("startIndex")
    # except:
    #     print("None results")
    #     continue
    # results = json.load(response)
    try:
        items = response[0]['items']
        count = 1
        for item in items:
            link = item['link']
            if 'tagged' in link:
                continue

            question_id = re.search('(\d+)', link).groups()[0]
            print(question_id)
            print()
            if count == 5: break
            count += 1
    except:
        print()
        print("None items")

        # with open('data.json', 'w') as outfile:
        #     json.dump(response, outfile)

        # with open('data.json') as data_file:
        #     data = json.load(data_file)[0]
        #     count = 1
        #     for item in data['items']:
        #         # title = item['pagemap']['question'][0]['name']
        #         # body = item['pagemap']['question'][0]['text']
        #         link = item['link']
        #         question_id = re.search('(\d+)', link).groups()[0]
        #         # print(title) #title
        #         # print(body) #body
        #         print(question_id)
        #         print()
        #         if count == 5: break
        #         count += 1


query = preprocess(
    """Good morning friends, I'm programming in [tag: python], with the graphic library [tag: tkinter], my question is this:,Question,How can I do this?,Example""")

# regex = r"\[(.*?)\]"
# matches = re.finditer(regex, query, re.MULTILINE | re.IGNORECASE)
# query = sub(r"\[(.*?)\]",r"(.*?)", query)
query = " ".join(query)
main(query)
