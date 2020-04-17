from bs4 import BeautifulSoup
import requests

url = "https://words.bighugelabs.com/error"
word = "error"

total_items = 0

response = requests.get(url)
data = response.text
soup = BeautifulSoup(data, "html.parser")
# items = soup.find_all('div', {'id': 'results'})
for ultag in soup.find_all('ul', {'class': 'words'}):
    for litag in ultag.find_all('li'):
        print (litag.text)


# for noun in nouns:
#     # title = item.find('h3').text.title()
#     # author = item.find('div', {'class': 'gs_a'}).text.title()
#     # link = item.find('a').get('href')
#     # print('Paper title:', title, '\nAuthor(s):', author, '\nlink:', link, '\n---')
#     # total_items += 1
#     resul.append(noun.find('a').text)

print("Total paper(s):", total_items)