import time

from google.cloud import translate
from google.oauth2 import service_account
import html

from langdetect import detect, DetectorFactory


def translate_text(text_to_translate, source_language, target_language):
    tries = 0
    max_tries = 20
    while tries < max_tries:
        try:
            credentials = service_account.Credentials.from_service_account_file(
                "tue translation-79b1ab01f57b.json")
            translate_client = translate.Client(credentials=credentials)
            translated = translate_client.translate(text_to_translate, source_language=source_language, target_language=target_language)
            tries = 20
            # time.sleep(1)

            return html.unescape(translated['translatedText'])

        except Exception as exc:
            print ("An exception occurred while translating your text:", exc)
            tries += 1
            # time.sleep(tries * 4)


def detect_language(text):
    DetectorFactory.seed = 0
    return detect(text)
    # return Detector(text).language

