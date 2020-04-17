from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import codecs, sys, itertools, regex

example_sent = "The best method of knowing the true use to be made of wit is, by reading the small number of good works, both in the learned languages, and in our own."

example_sent = regex.sub(r"[^\P{P}-']+", "", example_sent)

stop_words = set(stopwords.words('english'))

word_tokens = word_tokenize(example_sent)

filtered_sentence = [w for w in word_tokens if not w in stop_words]

filtered_sentence = []

for w in word_tokens:
	if w not in stop_words:
		filtered_sentence.append(w)

print(word_tokens)
print(filtered_sentence)

