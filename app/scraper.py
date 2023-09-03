import requests
from bs4 import BeautifulSoup, NavigableString
from enum import Enum
from llm_layer import parseHtmlWithGpt


class SOURCE(Enum):
    EventBrite = "EventBrite"
    LuMa = "LuMa"
    SFFunCheap = "SFFunCheap"


urls = {
    SOURCE.EventBrite: "https://www.eventbrite.com/d/ca--san-francisco/events/",
    SOURCE.LuMa: "https://lu.ma/sf",
    SOURCE.SFFunCheap: "https://sf.funcheap.com/events/san-francisco/",
}

def remove_empty_divs(tag):
    if tag.name == 'div':
        children = tag.find_all(recursive=False)
        if not children:
            tag.extract()
            return
        for child in children:
            remove_empty_divs(child)
        children = tag.find_all(recursive=False)
        if not children:
            tag.extract()
    else:
        for child in tag.find_all(recursive=False):
            remove_empty_divs(child)

def compress_divs(tag):
    divs = tag.find_all('div')

    for div in divs:
        if len(div.contents) == 1:
            div.replace_with(div.contents[0])

def getPage(source: SOURCE) -> str:
    url = urls[source]
    if source == SOURCE.LuMa:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        body = soup.find('body')
        section = body.find('div')
        
        for tag in section.find_all(True):  # find_all(True) matches all tags
            del tag["id"]
            del tag["class"]
            del tag["style"]
        
        for script in section(["script", "style", "head", "img", "svg", "footer"]):
            script.extract()

        remove_empty_divs(section)
        compress_divs(section)

        return section.prettify()
    else:
        raise Exception("unimplemented")


if __name__ == "__main__":
    page_html = getPage(SOURCE.LuMa)
    print(page_html)
    gpt_response_obj = parseHtmlWithGpt(page_html)
    # TODO: Add the source to the JSON
    print(gpt_response_obj)
