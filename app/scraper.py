import requests
from bs4 import BeautifulSoup
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


def getPage(source: SOURCE) -> str:
    url = urls[source]
    if source == SOURCE.LuMa:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        section = soup.find("div", class_="timeline")

        for tag in section.find_all(True):  # find_all(True) matches all tags
            del tag["id"]
            del tag["class"]
            del tag["style"]

        for script in section(["script", "style", "head", "img", "svg"]):
            script.extract()

        return section
    else:
        raise Exception("unimplemented")


if __name__ == "__main__":
    page_html = getPage(SOURCE.LuMa)
    gpt_response_obj = parseHtmlWithGpt(str(page_html))
    # TODO: Add the source to the JSON
    print(gpt_response_obj)
