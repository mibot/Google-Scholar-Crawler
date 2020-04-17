# coding=utf-8
# python -Qnew
import csv

import re
import requests
import PyPDF2
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument, PDFNoOutlines
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage, LTTextBoxHorizontal
from pdfminer.pdfdevice import PDFDevice
# from unicodeManager import UnicodeReader, UnicodeWriter

import nltk
from nltk import ngrams, FreqDist
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
import pymysql

# from string import maketrans
from io import StringIO
from shutil import move
from collections import Counter
import io
import unicodedata
import os
from languageDetetion import LanguageDetection

# from scholar import generater, languageDetetion
# from scholar.generater import GenerateKeywords
# from _codecs import decode


dataPath = os.path.abspath(os.path.relpath('../data'))
dataPath_2 = os.path.abspath(os.path.relpath('/Volumes/Seagate Expansion Drive/CLPD'))

db = pymysql.connect(host="localhost",  # your host, usually localhost
                     user="root",  # your username
                     passwd="iwJx0EAM",  # your password
                     db="clpd")  # name of the data base

cur = db.cursor()


class Filter():

    def __init__(self):
        pass

    def _updateNumPages(self, id):
        sql = "select id from resolved_query where downloaded = 1 and pdf2text = 1 and english = 1 and head = 1 and tail = 1 and npages is NULL and id = %s" % (
            id)
        # print sql
        try:
            cur.execute(sql)
            res = cur.fetchall()[0][0]
        except:
            res = ""
        if res:
            l = LanguageDetection()
            npages = l._getNumPages(id)
            print("Id: %s. Num pages: %s" % (id, npages))
            sql = "update resolved_query set npages = %s where id = %s" % (npages, id)
            print(sql)
            try:
                cur.execute(sql)
                db.commit()
            except:
                db.rollback()

    def _classify(self, id):
        type = ""
        l = LanguageDetection()

        sql = "select id from resolved_query where downloaded = 1 and pdf2text = 1 and english = 1 and head = 1 and tail = 1 and type is NULL and id = %s" % (
            id)
        # print sql
        try:
            cur.execute(sql)
            res = cur.fetchall()[0][0]
        except:
            res = ""
        if res:
            sql = "select npages from resolved_query where id = %s" % (id)
            # print sql
            try:
                cur.execute(sql)
                npages = cur.fetchall()[0][0]
            except:
                npages = ""
            if npages:

                # ---thesis
                if npages >= 30:
                    text = l._convert(os.path.join(dataPath, 'pdf/tocheck', str(id) + '.pdf'), pages=[0])
                    line = text.lower()
                    line = re.sub("\s", " ", line)
                    print(line)
                    if (
                            "thesis" in line or "ph.d. thesis" in line or "master thesis" in line or "master" in line or "master's" in line or "dissertation" in line or "in partial fulfillment" in line or "submitted for the" in line or "submitted to the" in line):
                        type = "thesis"
                    #                     with open(os.path.join(dataPath, 'txt', str(id) +'_head.txt')) as infile: in partial fulﬁllment
        #                         for text in infile:
        #                             print text
        #                             line = text.lower()
        #     #                     if "report" in line:
        #     #                         type = "report"
        #     #                         break
        #     #                     elif "specification" in line:
        #     #                         type = "specification"
        #     #                         break
        #     #                     elif "proceeding" in str(line).lower():
        #     #                         type = "proceeding"
        #     #                         break
        #                             if ("a thesis" in line or "ph.d. thesis" in line or "master thesis" in line or "dissertation" in line or "in partial fulfillment" in line or "submitted for the" in line or "submitted to the" in line):
        #                                 type = "thesis"
        #                                 break
        # -----papers
        #                 if npages <= 80:
        #                     if self._parse_toc(id) == "non-toc":
        #     #                     with open(os.path.join(dataPath, 'txt', str(id) +'_head.txt')) as infile:
        #     #                         for text in infile:
        #     #                             line = text.lower()
        #     #                             if ("abstract" in line):
        #                             type = "paper"
        #                                 break
        #                     if npages <= 40:
        #                         type = "paper"
        #                                     break

        #     #----proceedings
        #                 if npages > 40:
        #                     #if self._parse_toc(id) == "toc":
        #                     with open(os.path.join(dataPath, 'txt', str(id) +'_head.txt')) as infile:
        #                         for text in infile:
        #                         #print line
        #                             line = text.lower()
        #                             if ("proceedings" in line or "workshop" in line or "conference" in line):
        #                                 type = "proceedings"
        #                                 break

        # ----books
        #                 if npages > 40:
        #                     #if self._parse_toc(id) == "toc":
        #                     with open(os.path.join(dataPath, 'txt', str(id) +'_head.txt')) as infile:
        #                         for text in infile:
        #                         #print line
        #                             line = text.lower()
        #                             if ("book" in line or "chapter" in line or "printed in" in line or "published" in line or "publisher" in line):
        #                                 type = "book"

        #     #----technical report
        #                 if npages > 30:
        #
        #                     with open(os.path.join(dataPath, 'txt', str(id) +'_head.txt')) as infile:
        #                         for text in infile:
        #                         #print line
        #                             line = text.lower()
        #                             if ("technical report" in line or "report" in line):
        #                                 type = "technical report "

        if type:
            # sql = "update resolved_query set type = '%s', npages = %s where id = %s" %(type, npages, id)
            sql = "update resolved_query set type = '%s' where id = %s" % (type, id)
            print(sql)
            try:
                cur.execute(sql)
                db.commit()
            except:
                db.rollback()

    def _getNumPages(self, id):
        sql = 'select npages from resolved_query where downloaded = 1 and pdf2text = 1 and english = 1 and id = %s;' % (
            id)
        cur.execute(sql)
        return cur.fetchall()[0][0]

    def _convert(self, fname, pages=None):

        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        fp = file(fname, 'rb')
        password = ""
        maxpages = 0
        caching = True
        pagenos = set(pages)

        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                      check_extractable=True):
            interpreter.process_page(page)
        fp.close()

        text = retstr.getvalue()

        device.close()
        retstr.close()
        return text

    #     def _cleanBlankLines(self, id):
    # #         for line in io.open(os.path.join(dataPath, 'txt', str(id) +'.txt'), 'r', encoding='utf-8-sig'):
    # #             print(line)
    #
    #
    #         with open(os.path.join(dataPath, 'txt', str(id) +'.txt')) as infile, open(os.path.join(dataPath, 'txt', str(id)+'_cleaned.txt'), 'w') as outfile:
    #             #ligatures = {u"\uFB00": u'ff', u"\uFB00": u'fi'}
    # #             intab = u"\ufb01".encode("utf8")
    # #             outtab = u"fi".encode("utf8")
    # #             ligatures = maketrans(intab, outtab)
    #             for line in infile:
    #
    #
    #                  #if not line.isspace():
    #                  if not re.match(r'^\s*$', line):
    # #                     line = line.lower()
    #                     line = re.sub(r" +", " ", line)
    #                     line = re.sub(r"-\s","", line)
    #                     line = re.sub(r"ﬁ", "fi", line)
    #                     #line = line.translate(ligatures)
    #                     #line = u' '.join((line)).encode('utf-8').strip()
    #                     #line = unicodedata.normalize(line, "fi")
    #
    # #                     line = re.sub(r"(\d+)\. (\n)$", r"\1. ", line)
    #
    #                     #line = line.replace("\d+\. \n\b","\d+\. \b")
    #
    #
    #     #                 if re.findall(r"(\d+\.\s[^A-Z]\w+)", line):
    #     #                     print line
    #                     #line = line.translate(ligatures)
    #
    #                     outfile.write(line)
    #
    #         infile.close()
    #         outfile.close()

    def _saveTXT(self, id, text):
        with open(os.path.join(dataPath, 'txt', str(id) + '_toc.txt'), "w") as file:
            file.write(text)
        file.close()

    def _parse_toc(self, id):
        toc = []

        sql = "select id from resolved_query where downloaded = 1 and pdf2text = 1 and english = 1 and head = 1 and tail = 1 and type is NULL and id = %s" % (
            id)
        # print sql
        try:
            cur.execute(sql)
            res = cur.fetchall()[0][0]
        except:
            res = ""
        if res:
            maxlevel = 2
            filename = os.path.join(dataPath, 'pdf/tocheck', str(id) + '.pdf')

            fp = open(filename, 'rb')
            parser = PDFParser(fp)
            textf = ""
            try:
                doc = PDFDocument(parser)

                outlines = doc.get_outlines()
                text = ""

                for (level, title, dest, a, se) in outlines:
                    if level <= maxlevel:
                        title_words = title \
                            .encode('utf8') \
                            .replace('\n', '') \
                            .split()
                        title = ' '.join(title_words)
                        text = ' ' * level, title
                        # print text
                        textf += title
                        textf += "\n"
            except:
                pass

            if textf:
                return "toc"
            #                 sql = "update resolved_query set toc = 1 where id = %s  " %(id)
            else:
                return "non-toc"

    #                 #self._saveTXT(id, textf)
    #                 #sql = "update resolved_query set toc = 1 where id = %s  " %(id)
    #                 sql = "update resolved_query set type = 'paper' where id = %s  " %(id)
    #                     #print sql
    #             try:
    #                 cur.execute(sql)
    #                 db.commit()
    #             except:
    #                 db.rollback()

    #     def _getSections(self, id):
    #         matches = []
    #
    #         with open(os.path.join(dataPath, 'txt', str(id) +'_cleaned.txt')) as infile:
    #         #with open(os.path.join(dataPath, 'txt', 'test.txt')) as infile:
    #
    #             for line in infile:
    #                 #print line.rstrip("\n")
    #                 #res = re.findall(r"([\s\d+]\.\s[^A-Z]\w+)", line)
    #                 res = re.findall(r"(\d+\.\s[A-Z][^A-Z]\w+)", line)
    #
    # #                 if not res:
    # #                     res = re.findall(r"(\d9?\. [^A-Z]*)", line.rstrip())
    #                 if res:
    #
    #                     matches.append(res)
    #
    #
    # #                 if "references" in line:
    # #                     infile.close()
    # #                     return matches
    #
    #         infile.close()
    #         return matches

    #     def _getHead(self, id, section1, section2):
    #         copy = False
    #
    #         with open(os.path.join(dataPath, 'txt', str(id) +'_cleaned.txt')) as infile, open(os.path.join(dataPath, 'txt', str(id)+'_head.txt'), 'w') as outfile:
    #         #with open(os.path.join(dataPath, 'txt', 'test.txt')) as infile, open(os.path.join(dataPath, 'txt', str(id)+'_head.txt'), 'w') as outfile:
    #             for line in infile:
    #
    #                 if section1 in line.strip():
    #                     outfile.write(line)
    #                     copy = True
    #                 elif section2 in line.strip():
    #                     outfile.write(line)
    #                     copy = False
    #                 elif copy:
    #                     outfile.write(line)
    #
    #         infile.close()
    #         outfile.close()
    #
    #     def _getTail(self, id, lastSection):
    #
    #         copy = False
    #         with open(os.path.join(dataPath, 'txt', str(id) +'_cleaned.txt')) as infile, open(os.path.join(dataPath, 'txt', str(id) +'_tail.txt'), 'w') as outfile:
    #         #with open(os.path.join(dataPath, 'txt', 'test.txt')) as infile, open(os.path.join(dataPath, 'txt', str(id) +'_tail.txt'), 'w') as outfile:
    #             for line in infile:
    #
    #                 if lastSection in line.strip():
    #                     outfile.write(line)
    #                     copy = True
    #                 elif "References" in line.strip():
    #                     outfile.write(line)
    #                     copy = False
    #                 elif copy:
    #                     outfile.write(line)
    #
    #     def ocr_space_file(self, filename, overlay=False, api_key='helloworld', language='eng'):
    #
    #         payload = {'isOverlayRequired': overlay,
    #                    'apikey': 'abbae0ce6088957',
    #                    'language': language,
    #                    }
    #         with open(filename, 'r') as f:
    #             r = requests.post('https://api.ocr.space/parse/image',
    #                               files={filename: f},
    #                               data=payload,
    #                               )
    #         return r.content
    #
    #
    #     def pdf_to_string(self, file_object):
    #         ligatures = {0xFB00: u'ff', 0xFB01: u'fi'}
    #         # creating a pdf file object
    #         pdfFileObj = open(file_object, 'rb')
    #
    #         # creating a pdf reader object
    #         pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    #
    #         # printing number of pages in pdf file
    #         print(pdfReader.numPages)
    #
    #         # creating a page object
    #         pageObj = pdfReader.getPage(7)
    #
    #         # extracting text from page
    #         #print(pageObj.extractText())
    #         #ar=[]
    #
    #
    #         content = ""
    #         for i in range(0, pdfReader.numPages):
    #             pageObj = pdfReader.getPage(i)
    #             text = pageObj.extractText()
    #
    #             content += pdfReader.getPage(i).extractText() + "\n"
    #             #content.append(text)
    #             #content = content.replace("\u0152", "--")
    #
    #         output = os.path.join(dataPath, 'txt', 'out.txt')
    #
    #         os.system(("pdftotext %s %s") %(file_object , output))
    #
    #
    # #         pdf_text = ""
    # #         for line in content:
    # #             line = re.sub(" +", " ", line)
    # #             line = line.replace("-\n","")
    # #             line = line.translate(ligatures)
    # #             pdf_text += line
    # #         try:
    # #             with open(os.path.join(dataPath, 'txt', 'test.txt'), "w") as file:
    # #                 file.write(pdf_text.encode("utf-8"))
    # #         except UnicodeEncodeError:
    # #             pass
    #         #file.close()
    # #         print pdf_text
    #         # closing the pdf file object
    #         pdfFileObj.close()
    #         return content

    def countOccurencies(self, id):

        sql = "select id from resolved_query where downloaded = 1 and pdf2text = 1 and english = 1 and head = 1 and tail = 1 and (type is not NULL and type != 'proceedings') and id = %s" % (
            id)
        # print sql
        try:
            cur.execute(sql)
            res = cur.fetchall()[0][0]
        except:
            res = ""
        if res:
            sql = "select type from resolved_query where downloaded = 1 and pdf2text = 1 and english = 1 and head = 1 and tail = 1 and id = %s" % (
                id)
            #         if typePub == "paper":
            #             sql = "select type from resolved_query where downloaded = 1 and pdf2text = 1 and english = 1 and head = 1 and tail = 1 and (type = 'paper' or type = 'report') and id = %s" %(id)
            #         elif typePub == "thesis":
            #              sql = "select type from resolved_query where downloaded = 1 and pdf2text = 1 and english = 1 and head = 1 and tail = 1 and type = 'thesis' and id = %s" %(id)
            #         elif typePub == "specification":
            #              sql = "select type from resolved_query where downloaded = 1 and pdf2text = 1 and english = 1 and head = 1 and tail = 1 and type = 'specification' and id = %s" %(id)
            #         elif typePub == "book":
            #              sql = "select type from resolved_query where downloaded = 1 and pdf2text = 1 and english = 1 and head = 1 and tail = 1 and type = 'book' and id = %s" %(id)
            #
            # print sql
            try:
                cur.execute(sql)
                type = cur.fetchall()[0][0]
            except:
                type = ""
            if type:
                keywords = ["Cross-language",
                            "Crosslanguage",
                            "Cross-lingual",
                            "Crosslingual",
                            "Cross-linguistic",
                            "Crosslinguistic",
                            "Multi-language",
                            "Multilanguage",
                            "Multi-lingual",
                            "Multilingual",
                            "Multi-linguistic",
                            "Multilinguistic",
                            "Machine-translation",
                            "Copy",
                            "Duplicate",
                            "Plagiarism",
                            "Detection",
                            "Discovery"]
                nkeywords = len(keywords)
                text = ""
                with open(os.path.join(dataPath, 'txt', str(id) + '_head.txt')) as infile:
                    for line in infile:
                        #                     line = line.lower()
                        #                     line = re.sub("cross\slanguage", "cross-language", line)
                        #                     line = re.sub("cross\slingual", "cross-lingual", line)
                        #                     line = re.sub("cross\slinguistic", "cross-linguistic", line)
                        #                     line = re.sub("multi\slanguage", "multi-language", line)
                        #                     line = line.replace("multi\slingual", "multi-lingual")
                        #                     line = line.replace("multi\slinguistic", "multi-linguistic")
                        #                     line = line.replace("machine\stranslation", "machine-translation")
                        #                     line = line.replace("\n",  " ")
                        line = self._processText(line)
                        text += line.decode("utf8")

                # print text
                #             tokens = word_tokenize(text)
                #             print tokens
                #             punctuations = ['(',')',';',':','[',']',',']
                #             stop_words = stopwords.words('english')
                #             words = [word for word in tokens if len(word) > 1]
                #             words = [word for word in words if not word.isnumeric()]
                #             words = [word.lower() for word in words]
                #             words = [word for word in words if word not in stop_words]
                #             print words
                words = self._processNL(text)
                fdist = nltk.FreqDist(words)

                #             r = re.compile("duplicat.*")
                #             newlist = filter(r.match, fdist)
                #             print newlist
                #             print len(newlist)

                i = 0
                while i < nkeywords:
                    # works fine
                    #             for word, frequency in fdist.most_common():
                    #                 if word == str(keywords[i]).lower():
                    #                     print(u'{};{}'.format(word, frequency))
                    #                     sql = "insert into resolved_query_occurrencies values (%s, '%s', '%s', '%s', %s) " %(id, "short", "tail", word, frequency)
                    #                     #print sql
                    #                     try:
                    #                         cur.execute(sql)
                    #                         db.commit()
                    #                     except:
                    #                         db.rollback()

                    if fdist[str(keywords[i]).lower()] > 0:
                        sql = "insert into resolved_query_occurrencies values (%s, '%s', '%s', '%s', %s) " % (
                        id, type, "head", str(keywords[i]).lower(), fdist[str(keywords[i]).lower()])
                        # print sql
                        try:
                            cur.execute(sql)
                            db.commit()
                        except:
                            db.rollback()
                    i += 1
                #### tail    
                text = ""
                with open(os.path.join(dataPath, 'txt', str(id) + '_tail_noreferences.txt')) as infile:
                    for line in infile:
                        #                     text += line.decode("utf8")
                        #
                        #                     text = text.replace("\n",  " ")
                        #                     text = text.replace("cross language", "cross-language")
                        #                     text = text.replace("cross lingual", "cross-lingual")
                        #                     text = text.replace("cross linguistic", "cross-linguistic")
                        #                     text = text.replace("multi language", "multi-language")
                        #                     text = text.replace("multi lingual", "multi-lingual")
                        #                     text = text.replace("multi linguistic", "multi-linguistic")
                        #                     text = text.replace("machine translation", "machine-translation")
                        #                     line = line.lower()
                        #                     line = re.sub("cross\slanguage", "cross-language", line)
                        #                     line = re.sub("cross\slingual", "cross-lingual", line)
                        #                     line = re.sub("cross\slinguistic", "cross-linguistic", line)
                        #                     line = re.sub("multi\slanguage", "multi-language", line)
                        #                     line = re.sub("multi\slingual", "multi-lingual", line)
                        #                     line = re.sub("multi\slinguistic", "multi-linguistic", line)
                        #                     line = re.sub("machine\stranslation", "machine-translation", line)
                        #                     line = re.sub("\n",  " ", line)
                        #                     print line
                        line = self._processText(line)
                        text += line.decode("utf8")

                        #             tokens = word_tokenize(text)
                #             punctuations = ['(',')',';',':','[',']',',']
                #             stop_words = stopwords.words('english')
                #             words = [word for word in tokens if len(word) > 1]
                #             words = [word for word in words if not word.isnumeric()]
                #             words = [word.lower() for word in words]
                #             words = [word for word in words if word not in stop_words]
                words = self._processNL(text)
                fdist = nltk.FreqDist(words)

                i = 0
                while i < nkeywords:
                    # works fine
                    #             for word, frequency in fdist.most_common():
                    #                 if word == str(keywords[i]).lower():
                    #                     print(u'{};{}'.format(word, frequency))
                    #                     sql = "insert into resolved_query_occurrencies values (%s, '%s', '%s', '%s', %s) " %(id, "short", "tail", word, frequency)
                    #                     #print sql
                    #                     try:
                    #                         cur.execute(sql)
                    #                         db.commit()
                    #                     except:
                    #                         db.rollback()
                    if fdist[str(keywords[i]).lower()] > 0:
                        sql = "insert into resolved_query_occurrencies values (%s, '%s', '%s', '%s', %s) " % (
                        id, type, "tail", str(keywords[i]).lower(), fdist[str(keywords[i]).lower()])
                        # print sql
                        try:
                            cur.execute(sql)
                            db.commit()
                        except:
                            db.rollback()
                    i += 1

    def _processText(self, line):
        line = line.lower()

        line = re.sub("cross\slanguage", "cross-language", line)

        line = re.sub("cross\slingual", "cross-lingual", line)

        line = re.sub("cross\slinguistic", "cross-linguistic", line)

        line = re.sub("multi\slanguage", "multi-language", line)

        line = re.sub("multi\slingual", "multi-lingual", line)

        line = re.sub("multi\slinguistic", "multi-linguistic", line)

        line = re.sub("machine\stranslation", "machine-translation", line)
        #             if line.startswith("cop"):
        #                 line = "copy"
        pattern = re.compile("copy.*")
        line = pattern.sub("copy", line)

        pattern = re.compile("duplicat.*")
        # pattern = re.compile(r"duplicat[\w]", re.DOTALL)
        line = pattern.sub("duplicate", line)

        pattern = re.compile("detect.*")
        line = pattern.sub("detection", line)

        pattern = re.compile("discover.*")
        line = pattern.sub("discovery", line)

        #             if line.startswith("detect"):
        #                 line = "detection"
        #             if line.startswith("discover"):
        #                 line = "discovery"
        line = re.sub("-\n", "", line)
        line = re.sub("\n", " ", line)

        return line

    def _processNL(self, text):
        tokens = word_tokenize(text)
        punctuations = ['(', ')', ';', ':', '[', ']', ',']
        stop_words = stopwords.words('english')
        words = [word for word in tokens if len(word) > 1]
        words = [word for word in words if not word.isnumeric()]
        words = [word.lower() for word in words]
        words = [word for word in words if word not in stop_words]
        return words

    def _prepareTail(self, id):
        sql = "select id from resolved_query where downloaded = 1 and pdf2text = 1 and english = 1 and head = 1 and tail = 1 and (type is not NULL and type != 'proceedings') and id = %s" % (
            id)
        # print sql
        try:
            cur.execute(sql)
            res = cur.fetchall()[0][0]
        except:
            res = ""
        if res:
            with open(os.path.join(dataPath, 'txt', str(id) + '_tail.txt')) as infile, open(
                    os.path.join(dataPath, 'txt', str(id) + '_tail_noreferences.txt'), 'w') as outfile:
                text = ""
                for line in infile:
                    text += line
                    if "references" in str(line).lower():
                        # print line
                        outfile.write(text)
                        return

    def _filterPub(self, id, threshold):
        sql = 'select id from resolved_query where downloaded = 1 and pdf2text = 1 and english = 1 and toread = 0 and id = %s;' % (
            id)
        # print sql
        try:
            cur.execute(sql)
            res = cur.fetchall()[0][0]
        except:
            res = ""
        if res:
            k_dflanguage_head = 0
            k_dflanguage_tail = 0
            k_copy_head = 0
            k_copy_tail = 0
            k_detection_head = 0
            k_detection_tail = 0

            diff_language = ["Cross-language",
                             "Crosslanguage",
                             "Cross-lingual",
                             "Crosslingual",
                             "Cross-linguistic",
                             "Crosslinguistic",
                             "Multi-language",
                             "Multilanguage",
                             "Multi-lingual",
                             "Multilingual",
                             "Multi-linguistic",
                             "Multilinguistic",
                             "Machine-translation"]

            copy = ["Copy",
                    "Duplicate"]

            detection = ["Plagiarism",
                         "Detection",
                         "Discovery"]

            sql = "select section, sstring, freq from resolved_query_occurrencies where id = %s" % (id)
            # print sql
            try:
                cur.execute(sql)
                res = cur.fetchall()

            except:
                res = ""
            for row in res:
                i = 0
                while i < len(diff_language):
                    if str(diff_language[i]).lower() == row[1]:
                        if row[0] == "head":
                            k_dflanguage_head += row[2]
                        if row[0] == "tail":
                            k_dflanguage_tail += row[2]
                    i += 1
                i = 0
                while i < len(copy):
                    if str(copy[i]).lower() == row[1]:
                        if row[0] == "head":
                            k_copy_head += row[2]
                        if row[0] == "tail":
                            k_copy_tail += row[2]
                    i += 1
                i = 0
                while i < len(detection):
                    if str(detection[i]).lower() == row[1]:
                        if row[0] == "head":
                            k_detection_head += row[2]
                        if row[0] == "tail":
                            k_detection_tail += row[2]
                    i += 1
            print ("diff_language_head: %s. diff_language_tail: %s" % (k_dflanguage_head, k_dflanguage_tail))
            print ("copy_head: %s. copy_tail: %s" % (k_copy_head, k_copy_tail))
            print ("detection_head: %s. detection_tail: %s" % (k_detection_head, k_detection_tail))

            if (k_dflanguage_head >= threshold and k_dflanguage_tail >= threshold) and (
                    k_detection_head >= threshold and k_detection_tail >= threshold):
                sql = 'select title from resolved_query where id = %s;' % (id)
                try:
                    cur.execute(sql)
                    # res = cur.fetchall()[0][0]
                    res = cur.fetchall()
                except:
                    res = ""
                if res:
                    sql = "update resolved_query set toread = 1 where id = %s" % (id)
                    # print sql
                    try:
                        cur.execute(sql)
                        db.commit()
                    except:
                        db.rollback()

        # query = '"' + results['keywords'][step].get('dl') + '"' + ' +' + results['keywords'][step].get('cp') + ' "' + results['keywords'][step].get('de') + '"'

    def _onlyPapers(self, id):
        sql = 'select id from resolved_query where type = "paper" and toread = 1 and id = %s;' % (id)
        # print sql
        try:
            cur.execute(sql)
            res = cur.fetchall()[0][0]
        except:
            res = ""
        if res:
            move(os.path.join(dataPath, 'pdf/tocheck', str(id) + '.pdf'),
                 os.path.join(dataPath, 'pdf/toread', str(id) + '.pdf'))
            print("Moved!")
