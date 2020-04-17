# coding=utf-8
import os
from mstranslator import Translator
import PyPDF2
from nltk import FreqDist
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from shutil import move
from collections import Counter

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

dataPath = os.path.abspath(os.path.relpath('../data'))
translator = Translator('KEY')


class LanguageDetection():
    def __init__(self):
        pass

    def _getNumPages(self, id):
        try:
            pdf_file = PyPDF2.PdfFileReader(open(os.path.join(dataPath, 'pdf/tocheck', str(id) + '.pdf'), 'rb'))
            return pdf_file.getNumPages()
        except:
            return ""

    def _convert(self, fname, pages=None):
        try:
            rsrcmgr = PDFResourceManager()
            retstr = StringIO()
            codec = 'utf-8'
            laparams = LAParams()
            device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
            fp = file(fname, 'rb')
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            password = ""
            maxpages = 0
            caching = True
            pagenos = set(pages)

            for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                          check_extractable=True):
                interpreter.process_page(page)

            text = retstr.getvalue()
            fp.close()
            device.close()
            retstr.close()
        except:
            text = ""

        return text

    def _detection(self, id):
        english = 0
        other = 0

        npages = self._getNumPages(id)

        if npages and npages >= 5:
            page = 0

            while page <= npages:
                res = ""
                page_text = self._convert(os.path.join(dataPath, 'pdf/tocheck', str(id) + '.pdf'), pages=[page])
                if page_text:

                    page_text = page_text.replace('\n', ' ').replace('\r', '').replace('-\n', '')

                    try:
                        res = translator.detect_lang([page_text])
                    except:
                        pass

                    if res:
                        if res == 'en':
                            english += 1
                        else:
                            other += 1
                page += 1
            if english > other:
                # move(os.path.join(dataPath, 'pdf/tocheck', str(id)+'.pdf'), os.path.join(dataPath, 'pdf/checked', str(id)+'.pdf'))
                return "English"
            else:
                return "Other"
