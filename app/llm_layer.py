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
You are a helpful assistant that will be asked to parse HTML and provide information about each of the events in that HTML. Please retrieve information about each event such as the name, organizer, date, location, ticket price if applicable, a link to the event, and the event type (e.g. volunteer, community). In order to make parsing easier, provide your response as a JSON array of strings like so:

```
{
    response: [
        "Hayes Valley Cleanup, a community cleanup event occuring on Saturday 9/2, and organized by RefuseRefuseSF. Link: https://www.mobilize.us/togethersf/event/413069/",
        ...
    ]
}

You should provide enough data about the event so that somebody could decide whether to go just based on reading your summary.
```
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

    json_resp = json.loads(json_string)

    return json_resp['response']
