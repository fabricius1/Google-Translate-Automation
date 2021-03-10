from selenium import webdriver
from datetime import datetime
import pyperclip
import requests
import time
import os


def parse_string(text):
    """Replace the following characteres in the text"""
    special_characters = (
            ("%", "%25"),
            (" ", "%20"),
            (",", "%2C"),
            ("?", "%3F"),
            ("\n", "%0A"),
            ('\"', "%22"),
            ("<", "%3C"),
            (">", "%3E"),
            ("#", "%23"),
            ("|", "%7C"),
            ("&", "%26"),
            ("=", "%3D"),
            ("@", "%40"),
            ("#", "%23"),
            ("$", "%24"),
            ("^", "%5E"),
            ("`", "%60"),
            ("+", "%2B"),
            ("\'", "%27"),
            ("{", "%7B"),
            ("}", "%7D"),
            ("[", "%5B"),
            ("]", "%5D"),
            ("/", "%2F"),
            ("\\", "%5C"),
            (":", "%3A"),
            (";", "%3B")
        )

    for pair in special_characters:
        text = text.replace(*pair)    

    return text


def open_google_trans(source_language="en", target_language="pt", text_to_translate=None):
    """
        Translate the text from the source_language to the target_language, by opening the
    Google Translate site with this info.
        Parameters are all strings.
        Return is None
    """

    # exit the function if no text is submitted
    if not text_to_translate:
        print("No text submitted to translation.\nPlease insert a text.\n")
        return None

    if text_to_translate.startswith("http"):
        text_to_translate = requests.get(text_to_translate).text

    elif text_to_translate.endswith(".txt"):
        with open(text_to_translate, encoding="UTF-8") as file:
            text_to_translate = file.read()

    # variables to be used in the url:
    # source language
    sl = source_language
    # target language
    tl = target_language
    # operation
    operation = "translate"
    
    text_to_translate = parse_string(text_to_translate)

    # f-string with variables:
    link = f"https://translate.google.com/?sl={sl}&tl={tl}&text={text_to_translate}&op={operation}"

    # create an instance of the Chrome browser
    # (remember to adapt the executable_path to your machine environment)
    driver = webdriver.Chrome(executable_path=r"C:\Users\Fabricio\Desktop\chromedriver.exe")
    
    # open the link in the browser
    driver.get(link)

    # wait for 15 seconds to page to load
    time.sleep(15)

    # find the copy translation button and click on it
    driver.find_element_by_xpath(f'//*[text()="content_copy"]').click()
    
    # paste the translation saved in the clipboard to a variable
    translation = pyperclip.paste()

    # create subdirectory "./translations", if it doesn't exist
    os.makedirs('translations', exist_ok=True)

    # get the local iso 8601 datetime without microseconds
    current_datetime = datetime.now().replace(microsecond=0)
    current_datetime = current_datetime.isoformat().replace(":", "-")

    # create filename
    filename = os.path.join(
        "translations", 
        current_datetime + "_" + target_language + ".txt")

    # create .txt file to save the translation
    with open(filename, "w", encoding="UTF-8") as file:
        file.write(translation)

    # close the browser
    driver.quit()
    

if __name__ == "__main__":
    languages = ["pt", "es", "eo", "la", "tr", "ko", "ja"]
    url = "https://raw.githubusercontent.com/fabricius1/Google-Translate-Automation/master/textToTranslate.txt"
    text_to_translate = url

    for language in languages:
        open_google_trans("en", language, text_to_translate)
