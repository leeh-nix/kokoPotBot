import logging
import re
import datetime

pattern = re.compile(
    r"""
    \s?
    ((?P<days>\d{1,3})\s*(d(ays?)?)\s)?
    ((?P<hours>\d{1,3})\s*(h(ours?)?(rs?)?)\s)?
    ((?P<minutes>\d{1,3})\s*(m(inutes?)?(ins?)?)\s)?
    ((?P<seconds>\d{1,3})\s*(s(econds?)?(ecs?)?))?
    (?P<msg>.*)
    """,
    re.MULTILINE | re.IGNORECASE | re.VERBOSE | re.DOTALL,
)


def extractReminderDetails(message: str):
    # text = pattern.sub("", message).strip().replace("me to", "", 1).rstrip("in")
    # print(f"text: {text}")
    print(f"message: {message}")
    matchFound = pattern.search(message)
    # print("matchFound: ", matchFound)

    currentTime = datetime.datetime.now().timestamp() // 1
    print("current time: ", currentTime)

    days = int(matchFound.group("days")) if matchFound.group("days") else 0
    hours = int(matchFound.group("hours")) if matchFound.group("hours") else 0
    minutes = int(matchFound.group("minutes")) if matchFound.group("minutes") else 0
    seconds = int(matchFound.group("seconds")) if matchFound.group("seconds") else 0
    text = matchFound.group("msg") if matchFound.group("msg") else ""
    # text = matchFound.group("text")
    # print("grp", days, hours, minutes, seconds, "text", text)

    givenTime = (days * 86400) + (hours * 3600) + (minutes * 60) + seconds

    # print(f"givenTime: {givenTime}")
    # if givenTime == 0:
    #     return "Please specify time correctly"
    # else:
    #     remindTime = currentTime + givenTime
    #     print(f"remind time: {remindTime}")
    #     return {"remindTime": remindTime, "text": text}
    print(f"givenTime: {givenTime}")
    remindTime = currentTime + givenTime
    print(f"remind time: {remindTime}")
    print(f"text: {text}")
    return {"givenTime": givenTime, "remindTime": remindTime, "text": text}

# result = extractReminderDetails(
#     message="5 days 4 hours 3 minutes 2 seconds me to to do me and in you something in "
# )
# print("=================================================")
# print(result)
# result = extractReminderDetails(message="me to to do me and in you something in ")
# print("=================================================")
# print(result)
