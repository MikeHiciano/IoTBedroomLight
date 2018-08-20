import sqlite3 , time , datetime, telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

conn = sqlite3.connect('registry.db', check_same_thread= False)
c = conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS registro(numero INTEGER PRIMARY KEY, user TEXT, accion TEXT, fecha TEXT)')

def data_entry(user, accion):
    
    numero = time.time()
    fecha = str(datetime.datetime.fromtimestamp(numero).strftime('%y-%m-%d %H:%M:%S'))
    c.execute("INSERT INTO registro (user,accion,fecha) VALUES(?,?,?)",(user,accion,fecha))
    conn.commit()

def read_db(chat_id):
    c.execute("SELECT * FROM registro")
    for row in c.fetchall():
        bot.sendMessage(chat_id,row)

def message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print('Chat Message:', content_type, chat_type, chat_id)

    if content_type == 'text':
        if msg['text'] == '/start':
            data_entry(chat_id,"Start")
            bot.sendMessage(chat_id, 'Bienvenido\r\n utiliza el comando /key para iniciar')

        if msg['text'] == '/key':
            data_entry(chat_id,"Start Key")
            bot.sendMessage(chat_id, 'testing custom keyboard',
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[
                        [KeyboardButton(text="On"), KeyboardButton(text="Off")]
                                ]
            ))
        
        if msg['text'] == 'On':
            data_entry(chat_id,"Turn on")
            bot.sendMessage(chat_id,"turning lights on!")
        
        if msg['text'] == 'Off':
            data_entry(chat_id,"Turn Off")
            bot.sendMessage(chat_id,"turning lights off!")
        
        if msg['text'] == '/readdb':
            read_db(chat_id)

if __name__ == '__main__':
    bot = telepot.Bot('')#put the telegram bot key here!
    create_table()
    print('Listening ...')
    bot.message_loop({'chat': message}, run_forever=True)
            