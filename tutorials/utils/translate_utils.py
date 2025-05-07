import requests


def translate_text(text, target_lang='en'):
    """
    Übersetzt den übergebenen Text in die angegebene Zielsprache.

    :param text: Der zu übersetzende Text
    :param target_lang: Zielsprachen-Code (z.B. 'en', 'fr', 'de')
    :return: Übersetzter Text oder Fehlermeldung
    """
    url = "https://libretranslate.com/translate"
    payload = {
        "q": text,
        "source": "auto",  # Automatische Spracherkennung
        "target": target_lang,
        "format": "text"
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get('translatedText', "Fehler bei der Übersetzung")
    except requests.exceptions.RequestException as e:
        return f"Fehler bei der Übersetzung: {e}"
