import discord
import os
import requests
import json
import random
with open('C:\\Users\\102150\\OneDrive - University of Sharjah\Desktop\\abbas games and code and igcse practice\\abbas code\\code abbas\\discord bot\\TOKEN.json') as f:
    config = json.load(f)
TOKEN = config["token"]



DATA_FILE = "data.json"  # File where bot settings are stored

# ✅ Function to Load Data from JSON
def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"responding": True, "encouragements": []}  # Default values

# ✅ Function to Save Data to JSON
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# ✅ Load Existing Data (or Create Default)
data = load_data()

# Enable Discord intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

api_key = "37cfa5072401e8707c90a310b32aa458"

# Word lists
# 😞 List of sad words (Expanded)
sad_words = [
    "sad", "depressed", "unhappy", "angry", "miserable", "depressing", "horrible",
    "lonely", "hopeless", "frustrated", "tired", "stressed", "down", "crying",
    "broken", "heartbroken", "anxious", "worried", "helpless", "lost", "devastated",
    "exhausted", "worthless", "melancholy", "gloomy", "disheartened", "blue",
    "low", "overwhelmed", "empty", "pessimistic", "suffocating", "burnt out"
]

# 🌟 List of encouragement messages (Expanded)
starter_encouragements = [
    "Cheer up!", "Hang in there.", "You are a great person!", "You are amazing!",
    "You are good enough!", "Be Yourself!", "You got this!", "Believe in yourself!",
    "Stay strong!", "Better days are coming!", "You are not alone!", "Never give up!",
    "Your feelings are valid.", "It's okay to feel this way.", "Keep pushing forward!",
    "You matter!", "The sun will shine again.", "This too shall pass.", "You are loved.",
    "Your hard work will pay off!", "Take things one step at a time.", "You're doing great!",
    "Mistakes are just learning opportunities.", "You're stronger than you think!",
    "The world needs you!", "You are capable of amazing things!", "Every day is a new beginning!",
    "Stay hopeful!", "You're braver than you believe!"
]

# 😊 List of gratitude responses (Expanded)
h_replies = [
    "thank you", "thanks", "appreciate it", "that helped", "grateful", "thx", "ty",
    "cheers", "much appreciated", "thanks a ton", "thank you so much", "I owe you one!",
    "big thanks!", "thanks, that means a lot", "I'm grateful", "bless you", "respect!",
    "you're the best!", "I really needed that", "hats off to you!", "a million thanks!"
]

# 🤖 List of bot replies (Expanded)
bot_replies = [
    "You're welcome!", "No problem!", "Glad to help!", "Anytime!", "Happy to assist!",
    "That's what I'm here for!", "You're always welcome!", "Anything for you!",
    "Hope that made your day better!", "Just doing my job!", "Stay awesome!",
    "I'm happy to help!", "It's my pleasure!", "I'm always here if you need me!",
    "Don't mention it!", "You're amazing too!", "No worries!", "Take care!",
    "I got your back!", "Enjoy your day!", "Remember, you're not alone!"
]

dice_roll = ["1", "2", "3", "4", "5", "6"]
coin_flip = ["heads", "tails"]
rps_choices = ["rock", "paper", "scissors"]


# ✅ Fetch a motivational quote
def get_quote():
    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    return json_data[0]['q'] + " -" + json_data[0]['a']
import requests

def get_hadith():
    url = "https://random-hadith-generator.vercel.app/bukhari"
    response = requests.get(url)
    response.raise_for_status()
    json_data_hadith = response.json()
    
    print(json_data_hadith)  # Debug: Print the whole JSON response
    book = json_data_hadith["data"]["refno"]
    narrator = json_data_hadith["data"]["header"]
    hadith = json_data_hadith["data"]["hadith_english"]
    return f"{narrator} - {hadith} - {book} "

# ✅ Fetch the number of Ayahs for each Surah
def get_surah_data():
    url = "https://api.alquran.cloud/v1/surah"
    response = requests.get(url)
    response.raise_for_status()
    json_data = response.json()
    
    # Store the number of Ayahs for each Surah in a dictionary
    return {surah["number"]: surah["numberOfAyahs"] for surah in json_data["data"]}

# ✅ Fetch a truly random Quranic verse with translation
def get_ayah():
    
    # Get correct Ayah counts per Surah
    surah_data = get_surah_data()

    # Pick a random Surah
    random_surah = random.choice(list(surah_data.keys()))  

    # Get the correct Ayah range for the selected Surah
    max_ayahs = surah_data[random_surah]
    random_ayah = random.randint(1, max_ayahs)  

    # API endpoints
    url = f"https://api.alquran.cloud/v1/ayah/{random_surah}:{random_ayah}/en.asad"  # English Translation
    url_arabic = f"https://api.alquran.cloud/v1/ayah/{random_surah}:{random_ayah}"  # Arabic Text

    try:
        response = requests.get(url)
        response.raise_for_status()  
        response_arabic = requests.get(url_arabic)
        response_arabic.raise_for_status()

        json_data_quran = response.json()  
        json_data_arabic = response_arabic.json()

        if json_data_quran["status"] == "OK":
            ayah_text = json_data_quran["data"]["text"]  
            surah_name = json_data_quran["data"]["surah"]["englishName"]  
            ayah_number = json_data_quran["data"]["numberInSurah"]  
            translation = json_data_quran["data"]["edition"]["name"]  

        if json_data_arabic["status"] == "OK":
            ayah_text_arabic = json_data_arabic["data"]["text"]

            return (f"📖 **Quran Verse**\n"
                    f"{ayah_text_arabic}\n"
                    f"{ayah_text}\n\n"
                    f"🔹 {translation} - Surah {surah_name}, Ayah {ayah_number}")

        else:
            return "⚠ Error retrieving Ayah."

    except requests.exceptions.RequestException as e:
        return f"⚠ Error fetching Ayah: {e}"
    except KeyError:
        return "⚠ Unexpected response format from API."


# ✅ Get weather from OpenWeather API
async def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()

    if response["cod"] != 200:
        return "⚠ City not found."

    temp = response["main"]["temp"]
    weather_desc = response["weather"][0]["description"].capitalize()
    return f"🌡 Temperature in {city}: {temp}°C / {round(temp * 1.8 + 32, 2)}°F\n☁️ Condition: {weather_desc}.\n"

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print(f"Received message: {message.content}")  # Debugging

    # ✅ Toggle responding state
    if message.content.startswith("$responding "):
        value = message.content.split("$responding ", 1)[1].lower()
        if value in ["true", "on"]:
            data["responding"] = True
            save_data(data)
            await message.channel.send("✅ Responding is now **ON**.")
        elif value in ["false", "off"]:
            data["responding"] = False
            save_data(data)
            await message.channel.send("⛔ Responding is now **OFF**.")
        else:
            await message.channel.send("⚠ Invalid value. Please use `on` or `off`.")
        return

    # ✅ If responding is OFF, ignore all messages except `$responding`
    if not data["responding"]:
        return

    options = starter_encouragements + data["encouragements"]

    # ✅ Rock Paper Scissors Game
    if message.content.startswith("$rps"):
        await start_rps(message)

    # ✅ Show encouragement list
    if message.content.startswith("$list"):
        encouragement_list = "\n".join(data["encouragements"]) or "No encouragement messages found!"
        await message.channel.send(f"**Encouragement Messages:**\n{encouragement_list}")

    # ✅ Send a motivational quote
    if message.content.startswith("$inspire"):
        await message.channel.send(get_quote())

    # ✅ Respond to sad words
    if any(word in message.content.lower().split() for word in sad_words):
        await message.channel.send(random.choice(options))

    # ✅ Respond to gratitude messages
    elif any(word in message.content.lower().split() for word in h_replies):
        await message.channel.send(random.choice(bot_replies))

    # ✅ Fetch weather data
    if message.content.startswith("$weather "):
        city = message.content.split("$weather ", 1)[1]
        weather_info = await get_weather(city)
        await message.channel.send(weather_info)
    
    if message.content.startswith("$hadith"):
        await message.channel.send(get_hadith())
    # ✅ Dice Roll Command
    if message.content.startswith("$roll"):
        roll_result = random.choice(dice_roll)
        await message.channel.send(f"🎲 You rolled a {roll_result}!")
    if message.content.startswith("$quran"):
        await message.channel.send(get_ayah())
    if message.content.startswith("$help"):
        await message.channel.send("```Commands:\n$inspire - Get a motivational quote\n$weather [city] - Get weather data\n$roll - Roll a dice\n$flip - Flip a 			coin\n$rps - Play Rock, Paper, Scissors\n$hadith - Get a Hadith\n$quran - Get a random Quranic verse\n$new - add a new 											encouragement message\n$list - list all encouragement messages\n$responding [on/off] - Toggle bot responses\n$del [index] - 									Delete an encouragement message```")


# ✅ Start Rock Paper Scissors Game
async def start_rps(message):
    await message.channel.send("Would you like to play Rock, Paper, Scissors? Type `y` or `n`.")
    try:
        response = await client.wait_for("message")
        if response.content.lower() == "y":
            await play_rps(message, 0, 0)  # Start with scores at 0
        else:
            await message.channel.send("Goodbye!")
    except:
        await message.channel.send("You took too long! Game canceled.")

# ✅ Play Rock Paper Scissors
async def play_rps(message, player_score, comp_score):
    if player_score == 3:
        await message.channel.send(f"🏆 You win! Final Score: {player_score} - {comp_score}")
        return
    if comp_score == 3:
        await message.channel.send(f"🤖 The Bot wins! Final Score: {player_score} - {comp_score}")
        return

    await message.channel.send("Rock, Paper, or Scissors?")
    try:
        response = await client.wait_for("message", timeout=30.0)
        choice = response.content.lower()
        comp_choice = random.choice(rps_choices)

        await message.channel.send(f"You chose {choice}")
        await message.channel.send(f"Bot chose {comp_choice}")

        if choice == comp_choice:
            await message.channel.send("It's a tie!")
        elif (choice == "rock" and comp_choice == "scissors") or \
             (choice == "paper" and comp_choice == "rock") or \
             (choice == "scissors" and comp_choice == "paper"):
            await message.channel.send("You win this round!")
            player_score += 1
        else:
            await message.channel.send("The Bot wins this round!")
            comp_score += 1
            
        await message.channel.send(f"Score: {player_score} - {comp_score}")
        await play_rps(message, player_score, comp_score)  # Continue game

    except:
        await message.channel.send("You took too long! Game canceled.")

# ✅ Keep bot alive & run it
client.run(TOKEN)
