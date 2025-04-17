import discord
from discord.ext import commands
from youtube_transcript_api import YouTubeTranscriptApi
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.text_rank import TextRankSummarizer  # TextRank Summarizer
import re
import asyncio
import concurrent.futures
from dotenv import load_dotenv

load_dotenv()

bot_key = os.getenv("Bot_Key")
# Setup intents and bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Extract video ID from URL
def extract_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else None

# Fetch transcript
def fetch_transcript(video_url):
    video_id = extract_video_id(video_url)
    if not video_id:
        return None, "Could not extract video ID."
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([entry['text'] for entry in transcript])
        return full_text, None
    except Exception as e:
        return None, str(e)

# Summarization helper using Sumy
def summarize_text(text, max_summary_sentences=5):
    # Check if the text is empty or None
    if not text:
        return "❌ Error: No transcript available to summarize."
    
    # Ensure text is properly formatted (trim leading/trailing spaces)
    text = text.strip()

    if not text:
        return "❌ Error: The transcript is empty or could not be processed."
    
    try:
        # Log the first 300 characters to verify text validity
        print("Text to summarize: ", text[:300])

        # Use sumy PlaintextParser without the tokenizer argument (it handles text input)
        parser = PlaintextParser.from_string(text, tokenizer=None)

        # Log the document object to see if it's parsed correctly
        print("Parser Document: ", parser.document)

        # Use TextRank Summarizer
        summarizer = TextRankSummarizer()

        # Create the summary (adjust the number of sentences)
        summary = summarizer(parser.document, sentences_count=max_summary_sentences)

        # Join the sentences and return as summary
        summary_text = " ".join(str(sentence) for sentence in summary)
        print(f"Generated Summary: {summary_text}")  # Log the generated summary for debugging
        return summary_text
    
    except Exception as e:
        return f"❌ Summarization failed: {str(e)}"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def summarize(ctx, url: str):
    if not re.match(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.*', url):
        await ctx.send("Please provide a valid YouTube URL!")
        return

    await ctx.send("📜 Fetching transcript...")

    transcript, error = fetch_transcript(url)
    if error or not transcript:
        await ctx.send(f"❌ Error getting transcript: {error}")
        return

    await ctx.send(f"✅ Transcript fetched. Summarizing...")

    loop = asyncio.get_event_loop()
    try:
        with concurrent.futures.ThreadPoolExecutor() as pool:
            summary = await loop.run_in_executor(pool, summarize_text, transcript)

        await ctx.send(f"🧠 Summary:\n```{summary}```")
    except Exception as e:
        await ctx.send(f"❌ Summarization failed: {e}")

# Run the bot
bot.run('')