import webbrowser


def parse_string(text):
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
            ("|", "%7C")
        )

    for pair in special_characters:
        text = text.replace(*pair)    

    return text


# variables to be used in the url:
# source language
sl = "en"
# target language
tl = "pt"
# operation
operation = "translate"

# Romeo and Juliet's Prologue
# (extracted from http://shakespeare.mit.edu/romeo_juliet/full.html) 
text = """
Two households, both alike in dignity,
In fair Verona, where we lay our scene,
From ancient grudge break to new mutiny,
Where civil blood makes civil hands unclean.
From forth the fatal loins of these two foes
A pair of star-cross'd lovers take their life;
Whose misadventured piteous overthrows
Do with their death bury their parents' strife.
The fearful passage of their death-mark'd love,
And the continuance of their parents' rage,
Which, but their children's end, nought could remove,
Is now the two hours' traffic of our stage;
The which if you with patient ears attend,
What here shall miss, our toil shall strive to mend."""

text = parse_string(text)

# f-string with variables:
link = f"https://translate.google.com/?sl={sl}&tl={tl}&text={text}&op={operation}"

# This function, from the webbrowser module, opens a link in the default browser
webbrowser.open(link)
