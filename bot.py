import os, collections, discord
from groq import Groq

ai = Groq(api_key=os.environ["GROQ_API_KEY"])
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

PERSONA = (
    "You are eKitten, the chaotic-good cat mascot of this Discord server. "
    "You're witty, a little unhinged, and quick with a joke. Keep replies SHORT — "
    "one or two punchy sentences, like a friend texting, never a lecture. "
    "Lean into cat energy (zoomies, naps, knocking things off tables) but don't overdo the 'meow's. "
    "Be playful and tease the humans a bit, but stay good-natured — never mean, cruel, or NSFW. "
    "Match the chat's vibe and read the room using the recent messages."
)

# shortcut: memory is in-RAM and per-channel, resets on restart. Fine for a fun bot.
history = collections.defaultdict(lambda: collections.deque(maxlen=12))

def replying_to_bot(msg):
    ref = msg.reference
    return ref and ref.resolved and getattr(ref.resolved, "author", None) == bot.user

@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        return
    if bot.user not in msg.mentions and not replying_to_bot(msg):
        return

    chan = history[msg.channel.id]
    chan.append({"role": "user", "content": f"{msg.author.display_name}: {msg.content}"})
    reply = ai.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "system", "content": PERSONA}, *chan],
    ).choices[0].message.content
    chan.append({"role": "assistant", "content": reply})
    await msg.reply(reply[:2000])

bot.run(os.environ["DISCORD_TOKEN"])
