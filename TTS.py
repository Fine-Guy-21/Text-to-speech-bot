from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup 
from edge_tts import VoicesManager
import time, re , edge_tts


bot = Client("TTS Bot",api_id=21832338, 
              api_hash="3d11dad763458ea9b7ab106d6fc5e7ce",
              bot_token="7018791817:AAEmSO0Y9JmwFsFwjKXFUFZbBras4K0II0Y")


botusers = {}

class User:
    Inst = []
    def __init__(self,userid,username):
        self.userid = userid
        self.username = username
        self.wordsleft = 500
        self.premium_status = False
        self.selectedvoice = "en-US-SteffanNeural"
        User.Inst.append(self)

    def ChangeVoice(self,voice):
        self.selectedvoice = voice

    def is_premium(self):
        return self.premium_status

    def ChangePremium(self,value):
        self.premium_status = value 

    def get_user(obj):
        return obj


Language_menu = [   
                    ['English','Spanish','French'],
                    ['Mandarin', 'Russian', 'Arabic'],
                    ['Amharic','More languages']             
                ]
Amh_lang_menu = [ ['Ameha','Mekdes'] ]




# Functions 

async def TTS(bot,message):
    await message.reply("processing")
    voices = await VoicesManager.create()
    user = User.get_user(botusers.get(message.from_user.id))
    voice= user.selectedvoice
    communicate = edge_tts.Communicate(message.text, voice)
    await communicate.save('voice.mp3') 
    await bot.send_voice(message.chat.id,"voice.mp3",caption=f'{voice}') 


# Triggers

@bot.on_message(filters.private & (filters.command("start") or filters.command("Start")))
def Greetuser(bot,message):    
    id = message.from_user.id
    try:
         name = message.from_user.first_name + ' ' +message.from_user.last_name
    except:
         try:
              name = message.from_user.first_name
         except:
              name = 'User'+ str(id)
    
    if id in botusers:        
        user = User.get_user(botusers.get(id))         
        match = re.findall(r'-(\w+)Neural', user.selectedvoice)
        message.reply(f"Dear {user.username} Welcome \n Is premium : {user.premium_status} \n selected voice : {match[0]}")
    else :
        message.reply("Welcome")
        botusers[id] = User(id,name)
        print(botusers)

@bot.on_message(filters.private & (filters.command("lang") | filters.command("language")))
def ChangeLanguage(bot,message):
    text = "Select your prefered language."
    Lang_Menu = ReplyKeyboardMarkup(Language_menu,one_time_keyboard=True, resize_keyboard=True,placeholder="Choose Language")
    message.reply(text=text, reply_markup = Lang_Menu )

@bot.on_message(filters.private & filters.regex('Amharic'))
def AmharicMenu(bot,message):
    text = "Ok Now, select your prefered voice"
    Amh_Menu =ReplyKeyboardMarkup(Amh_lang_menu,one_time_keyboard=True, resize_keyboard=True,placeholder="Choose Voice")
    message.reply(text=text, reply_markup = Amh_Menu )

@bot.on_message(filters.private & filters.regex('Ameha'))
def setameha(bot,message):
    user = User.get_user(botusers.get(message.from_user.id))         
    user.ChangeVoice("am-ET-AmehaNeural")
    message.reply("Language Succesfully changed")
    
@bot.on_message(filters.private & filters.regex('Mekdes'))
def setmekdes(bot,message):    
    user = User.get_user(botusers.get(message.from_user.id))         
    user.ChangeVoice("am-ET-MekdesNeural")
    message.reply("Language Succesfully changed")

@bot.on_message(filters.private & filters.text)
async def TextToSpeech(bot,message):
    
    await TTS(bot,message)




#     if message.reply_to_message:
#         text = message.reply_to_message.text
#     else:
#         text = message.text[5:]

       






print("tts running")
bot.run()


