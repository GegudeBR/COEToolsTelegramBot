import time
import Laps
import Tools
import credentials
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

updater = Updater(credentials.telegram_key,
                  use_context=True)
  
  
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello sir, Welcome to the Bot.Please write\
        /help to see the commands available.")
  
def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands :-
    /laps (computer_name) - To get the LAPS password
    /jitbit (computer_name) - To get the asset page
    /cyder (computer_name) - To get the cyder entry
    /log (computer_name) - To get the activity log""")
    
def laps(update: Update, context: CallbackContext):
    if len(context.args) < 1 or len(context.args) > 1:
        update.message.reply_text("Use: /laps (computer_name)")
    else:
        computer_name = context.args[0]
        laps = Laps.LAPS()
        laps.start(computer_name)
        while(laps.get_password() == None):
            time.sleep(0.1)
        update.message.reply_text(computer_name.toUpper() + ":\n" + laps.get_password())

def jitbit(update: Update, context: CallbackContext):
    if len(context.args) < 1 or len(context.args) > 1:
        update.message.reply_text("Use: /jitbit (computer_name)")
    else:
        try:
            computer_name = context.args[0]
            update.message.reply_text(Tools.Jitbit(computer_name).get_url())
        except:
            update.message.reply_text("An error has occured.")


def cyder(update: Update, context: CallbackContext):
    if len(context.args) < 1 or len(context.args) > 1:
        update.message.reply_text("Use: /cyder (computer_name)")
    else:
        computer_name = context.args[0]
        update.message.reply_text(Tools.Cyder(computer_name).get_url())
           
def log(update: Update, context: CallbackContext):
    if len(context.args) < 1 or len(context.args) > 1:
        update.message.reply_text("Use: /log (computer_name)")
    else:
        computer_name = context.args[0]
        update.message.reply_text(Tools.Log(computer_name).get_url())
        
    
def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text)
  
  
def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry I can't recognize you , you said '%s'" % update.message.text)
 
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('laps', laps, Filters.user(username=credentials.telegram_user)))
updater.dispatcher.add_handler(CommandHandler('jitbit', jitbit, Filters.user(username=credentials.telegram_user)))
updater.dispatcher.add_handler(CommandHandler('cyder', cyder, Filters.user(username=credentials.telegram_user)))
updater.dispatcher.add_handler(CommandHandler('log', log, Filters.user(username=credentials.telegram_user)))
updater.dispatcher.add_handler(CommandHandler('help', help))

updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(
    Filters.command, unknown))  # Filters out unknown commands
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

try:
    updater.start_polling()
    updater.idle()
except KeyboardInterrupt:
    exit(1)