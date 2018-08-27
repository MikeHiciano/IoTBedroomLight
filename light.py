import sqlite3 , time , datetime, telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
import RPi.GPIO as GPIO

#setting up the raspberry pi GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT) 

#setting up the conection to the database 
#pd: always put the check_same_thread = False , if you dont wanna have a 
#headache XD
conn = sqlite3.connect('registry.db', check_same_thread= False)
c = conn.cursor()

#function that creates the table ... of course xD
def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS registro(numero INTEGER PRIMARY KEY, user TEXT, accion TEXT, fecha TEXT)')

#function to put the information in the database
def data_entry(user, accion):
    
    numero = time.time()
    fecha = str(datetime.datetime.fromtimestamp(numero).strftime('%y-%m-%d %H:%M:%S'))
    c.execute("INSERT INTO registro (user,accion,fecha) VALUES(?,?,?)",(user,accion,fecha))
    conn.commit()

#well , actually this is a feature dressed like a bug XD, its in process
def read_db(chat_id):
    c.execute("SELECT * FROM registro")
    for row in c.fetchall():
        bot.sendMessage(chat_id,row)

#this is the function that contains the bot
def message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print('Chat Message:', content_type, chat_type, chat_id)

    if content_type == 'text':
        #msg['text'] = the text you send to the bot
        #if you send a word with a slash in the start , its a command
        #usually /start is the first command you send to all bots
        if msg['text'] == '/start':
            data_entry(chat_id,"Start")
            bot.sendMessage(chat_id, 'Bienvenido\r\n utiliza el comando /key para iniciar')

        #this command start the keys
        if msg['text'] == '/key':
            data_entry(chat_id,"Start Key")
            bot.sendMessage(chat_id, 'testing custom keyboard',
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[
                        [KeyboardButton(text="On"), KeyboardButton(text="Off")]
                                ]
            ))
        
        #well , with that you can turn on wathever you have in the GPIO
        if msg['text'] == 'On':
            data_entry(chat_id,"Turn on")
            GPIO.output(17,GPIO.HIGH)
            bot.sendMessage(chat_id,"turning lights on!")
            time.sleep(5)

        #aaaand , with that , you can turn off the GPIO
        if msg['text'] == 'Off':
            data_entry(chat_id,"Turn Off")
            GPIO.output(17,GPIO.LOW)
            bot.sendMessage(chat_id,"turning lights off!")
            time.sleep(5)

        if msg['text'] == '/toogle':
            for i in range(0,3):
                GPIO.output(17,GPIO.HIGH)
                time.sleep(0.3)
                GPIO.output(17,GPIO.LOW)
                time.sleep(0.3)

if __name__ == '__main__':

    bot = telepot.Bot('') #put the telegram bot key here!
    create_table()
    print('Listening ...')
    bot.message_loop({'chat': message}, run_forever=True)