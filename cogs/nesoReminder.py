from datetime import datetime, timedelta
from pytz import timezone
from discord.ext import tasks

class NesoReminder():
    def __init__(self, bot) -> None:
        self.bot = bot
        self.timezone_name = "Asia/Kolkata"
        self.tz = timezone(self.timezone_name)

    async def remind_at_midnight(self):
        print("It's midnight! Time for your reminder.")
        # Add your reminder logic here
        print("It's midnight! Time for your reminder.")
        bisskut = 757478713402064996
        kokose = 418364415856082954
        kurkure = 898776433638400041
        channel = 930006459398365214
        # await self.bot.get_channel(channel).send(f"🤓<@{kokose}>")
        await self.bot.get_channel(channel).send(f"so who's gonna record neso this time 🤓 <:kyabola:930005555429384213> <@{bisskut}> <@{kokose}> <@{kurkure}>")

    def start_reminder_loop(self):
        # Calculate the time for the next midnight in the specified time zone
        current_time = datetime.now(self.tz)
        next_midnight = current_time.replace(
            hour=0, minute=0, second=0, microsecond=0
        ) + timedelta(days=1)

        # Calculate the time remaining until the next midnight
        time_to_midnight = (next_midnight - current_time).total_seconds()

        # Start the reminder loop
        self.remind_loop.start(time_to_midnight)

    @tasks.loop(seconds=86400)  # Loop every 24 hours (midnight)
    async def remind_loop(self):
        await self.remind_at_midnight()