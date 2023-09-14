async def chatko(ctx):
    if ctx.author.voice and ctx.author.voice.channel:
        voice_channel = ctx.author.voice.channel
        for member in voice_channel.members:
            await member.move_to(None)