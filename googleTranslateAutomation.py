from selenium import webdriver
from datetime import datetime
import pyperclip
import requests
import time
import sys
import os


def parse_string(text):
    """Replace the following characters in the text"""
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


def check_input_type(text_to_translate=None):
    """
        Check the input type and, if text_to_translate is not None, return its value
    as a string.
    """
    # print message if no text is submitted
    if not text_to_translate:
        print("No text submitted.\nPlease insert a text.\n")

    # if text_to_translate is a link, use the requests library to download it
    elif text_to_translate.startswith("http"):
        text_to_translate = requests.get(text_to_translate).text

    # if text_to_translate is a .txt file, copy its content
    elif text_to_translate.endswith(".txt"):
        with open(text_to_translate, encoding="UTF-8") as file:
            text_to_translate = file.read()

    return text_to_translate


def save_output_as_txt(text, target_language="pt", name=None):
    """Save text as a .txt file.
       Parameters are:
        - text_to_translate(type: str);
        - target_language(type: str; default: "pt");
        - name(type: str or None; default: None)

       Return is None.
    """
    # create subdirectory "./translations", if it doesn't exist
    os.makedirs('translations', exist_ok=True)

    # get the local iso 8601 datetime without microseconds
    current_datetime = datetime.now().replace(microsecond=0)
    current_datetime = current_datetime.isoformat().replace(":", "-")

    # if the name parameter is None, the filename will use the target_language info
    if not name:
        name = target_language

    # create filename
    filename = os.path.join(
        "translations",
        current_datetime + "_" + name + ".txt")

    # create .txt file to save the text
    with open(filename, "w", encoding="UTF-8") as file:
        file.write(text)


def search_google_trans(text_to_translate=None,
                        target_language="pt",
                        source_language="en",
                        input_checked=False,
                        name=None):
    """
        Translate the parameter text_to_translate from the source_language to the
    target_language, by getting this info from the Google Translate site.
        Parameters are:
        - text_to_translate(type: str or None; default: None);
        - target_language(type: str; default: "pt");
        - source_language(type: str; default: "en");
        - input_checked(type: bool; default: False);
        - name(type: str or None; default: None).
        Return is None.
    """

    # Check text_to_translate input type, if input_checked value is False
    if not input_checked:
        text_to_translate = check_input_type(text_to_translate)

    # Exit the function if text_to_translate value is None
    if not text_to_translate:
        return None

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

    # save the translation
    save_output_as_txt(translation, target_language=target_language, name=name)

    # close the browser
    driver.quit()


def translate_any_text(text_to_translate=None, target_language="pt", source_language="en"):
    """
        Allow to translate a +5k character long text in a continuous flow by calling
    search_google_trans on every text chunk. Parameter are:
        - text_to_translate(type: str or None; default: None);
        - target_language(type: str; default: "pt");
        - source_language(type: str; default: "en").

        Return is None.
    """
    # Call check_input_type on the text_to_translate parameter
    text_to_translate = check_input_type(text_to_translate)

    # Exit the function if text_to_translate value is None
    if not text_to_translate:
        return None
    
    # initialize variables
    chunks = []
    chunk = ""

    # split the text in a list with its paragraphs
    paragraphs = text_to_translate.split('\n')

    for paragraph in paragraphs:
        # save paragraph in the chunk str, if condition is True
        if len(chunk + paragraph) < 4000:
            chunk += "\n" + paragraph
        else:
        # append chunk in the chunks list, when its len comes closer to 4k char
            chunks.append(chunk)
            chunk = "\n" + paragraph

    # This coefficent will help to pad zeros in the temporary filenames
    if len(chunks) < 10:
        padding_coef = 1
    elif len(chunks) < 99:
        padding_coef = 2
    elif len(chunks) < 999:
        padding_coef = 3
    else:
        padding_coef = 4

    count = 0
    # for each text chunk:
    for chunk in chunks:
        count += 1
        # create name
        name = "chunk" + (padding_coef - len(str(count))) * "0" + str(count)
        # search Google Translate using this chunk as source text,
        # saving its translation as a .txt file
        search_google_trans(chunk,
                            target_language,
                            source_language,
                            input_checked=True,
                            name=name)

    complete_translation = ""
    # loop over files in ./translations directory
    for file in os.listdir('./translations'):
        # if filename contains "chunk", extract its content and then remove the file
        if "chunk" in file:
            with open(os.path.join('translations', file), encoding="UTF-8") as f:
                complete_translation += f.read()
            os.remove(os.path.join("translations", file))

    # save variable complete_translation as complete.txt
    with open(os.path.join("translations", "complete.txt"), "w", encoding="UTF-8") as file:
        file.write(complete_translation)


if __name__ == "__main__":
    translate_any_text("longerTextToTranslate.txt", "eo", "pt")
    print('\n\nFinished!\n\n')

    ### older version for code as "__main__":

    # languages = ["pt", "es", "eo", "la", "tr", "ko", "ja"]
    # url = "https://raw.githubusercontent.com/fabricius1/Google-Translate-Automation/master/textToTranslate.txt"
    # text_to_translate = url

    # for language in languages:
    #     search_google_trans(text_to_translate, language, "en", input_checked=False)
