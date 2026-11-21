import os, discord
from groq import Groq

ai = Groq(api_key=os.environ["GROQ_API_KEY"])
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

PERSONA = "You are eKitten, a playful, cute cat-like chatbot. Keep replies short and friendly."

@bot.event
async def on_message(msg):
    if msg.author == bot.user or bot.user not in msg.mentions:
        return
    reply = ai.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "system", "content": PERSONA},
                  {"role": "user", "content": msg.content}],
    ).choices[0].message.content
    await msg.reply(reply[:2000])

bot.run(os.environ["DISCORD_TOKEN"])
