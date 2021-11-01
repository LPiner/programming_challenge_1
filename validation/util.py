from bs4 import BeautifulSoup

def contains_html(string: str) -> bool:
    return bool(BeautifulSoup(string, "html.parser").find())
