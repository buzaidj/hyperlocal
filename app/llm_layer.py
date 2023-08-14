import os
import openai
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()


def getDate():
    now = datetime.now()
    day_name = now.strftime("%A")
    month_name = now.strftime("%B")
    day = now.day
    return f"{day_name}, {month_name} {day}"


openai.api_key = os.environ.get("OPENAI_API_KEY")
# print(openai.Model.retrieve("gpt-3.5-turbo"))

SYSTEM_PROMPT = """
You are a helpful assistant that will be asked to parse HTML and provide structured output as specified.

I will provide you with an HTML file that contains information about events in San Francisco. Each event should have an id or link representing it (could be an href) tag, and some other info. Each event should also have a date. Dates may be relative in the HTML, so for context today's date is (#TODO Add date) Please try not to hallucinate. Your responses should look like this:
```
{
    "events": [
        {
            "link": "/sample_link",
            "other_info": "other relevant info such as Foo Bar Dinner, organized by Baz and FooBar, at location Y, tickets cost $x, the event has a waitlist, and more"
        }
        ...
    ]
}
```
You should only return valid JSON, that is your whole response should just be valid JSON. Let's begin!
"""


def parseHtmlWithGpt(htmlSource: str):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {"role": "user", "content": htmlSource},
        ],
    )

    ai_response = response.choices[0].message.content

    start_index = ai_response.find("{")
    end_index = ai_response.rfind("}") + 1  # +1 to include the closing brace
    json_string = ai_response[start_index:end_index]

    return json.loads(json_string)
