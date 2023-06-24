import re
import datetime

def reminderTime(message: str):
    # print("message ", message)
    pattern = re.compile(
        (
            r"(((?P<days>\d{1,3})\s?(d(ays?)?)\s)?((?P<hours>\d{1,3})\s?(h(ours?)?)\s)?((?P<minutes>\d{1,3})\s?(m(inutes?)?(ins?)?)\s)?((?P<seconds>\d{1,3})\s?(s(econds?)?(ecs?)?)\s)?)(?P<text>.*)"
        ),
        re.MULTILINE | re.IGNORECASE,
    )

    matchFound = pattern.search(message)

    currentTime = datetime.datetime.now().timestamp() // 1
    print("current time: ",currentTime)

    days = int(matchFound.group("days")) if matchFound.group("days") else 0
    hours = int(matchFound.group("hours")) if matchFound.group("hours") else 0
    minutes = int(matchFound.group("minutes")) if matchFound.group("minutes") else 0
    seconds = int(matchFound.group("seconds")) if matchFound.group("seconds") else 0
    text = matchFound.group("text")
    print("grp", days, hours, minutes, seconds, "text", text)

    givenTime = (days * 86400) + (hours * 3600) + (minutes * 60) + seconds
    remindTime = currentTime + givenTime
    # print(text, type(text))
    print("remind time :", remindTime)
    return remindTime, text


# result = remind(message="2 seconds to get inside")