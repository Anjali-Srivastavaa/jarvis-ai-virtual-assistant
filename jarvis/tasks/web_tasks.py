import webbrowser
import urllib.parse

def open_website(url):
    """Opens a website in the default browser."""
    if not url.startswith('http'):
        url = 'https://' + url
    webbrowser.open(url)
    return f"Opening {url}"

def search_google(query):
    """Searches Google for the query."""
    url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
    webbrowser.open(url)
    return f"Searching Google for {query}"

def search_youtube(query):
    """Searches YouTube for the query."""
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
    webbrowser.open(url)
    return f"Searching YouTube for {query}"

def search_wikipedia(query):
    """Searches Wikipedia."""
    url = f"https://en.wikipedia.org/wiki/Special:Search?search={urllib.parse.quote(query)}"
    webbrowser.open(url)
    return f"Searching Wikipedia for {query}"
