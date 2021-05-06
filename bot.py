import logging
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ForceReply

#------------------------------------------------------------------------------------------
# Обработчик команды /start
# Инфу об объекте update смотри в доке: https://core.telegram.org/bots/api#getting-updates
#------------------------------------------------------------------------------------------
def start(update, context):
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )

#------------------------------------------------------------------------------------------
# Обработчик команды /help
#------------------------------------------------------------------------------------------
def help(update, context):
    update.message.reply_text('Sorry, "help" does not work yet')

#------------------------------------------------------------------------------------------
# Обработчик по дефолту
#------------------------------------------------------------------------------------------
def default(update, context):
    update.message.reply_text('Use command /help')

#------------------------------------------------------------------------------------------
# Обработчик ошибок бота
#------------------------------------------------------------------------------------------
def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

#------------------------------------------------------------------------------------------
# От сюда скрипт начинает выполняться
#------------------------------------------------------------------------------------------
def main():
    # Настраиваем логгер
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Устанавливаем порт, на котором будет висеть скрипт бота
    PORT = int(os.environ.get('PORT', 8443))    
 
    # Токен доступа к боту в телеграм, с ним нужно делать все HTTP-запросы
    TOKEN = '1765524728:AAHaEI8wL5Y2Fos2t6ye0j5dENYOS5sAjkQ'

    # Это адрес твоего скрипта в Heroku, телеграм будет отправлять сюда всё, что пользователи напишут боту
    WEBHOOK_URL = 'https://guarded-savannah-59373.herokuapp.com/'    

    # Создаем бота
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Прикручиваем к нему наши обработчики команд,
    # которые мы определили выше над функцией main
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # Если пользователь написал произвольный текст,
    # который не распознался как команда, то сработает дефолтный обработчик
    dp.add_handler(MessageHandler(Filters.text, default))

    # Прикручиваем обработчик ошибок
    dp.add_error_handler(error)

    # Устанавливаем вебхук, на который телеграм будет присылать все сообщения
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN,
                          webhook_url=WEBHOOK_URL + TOKEN)

    # Запускаем бота
    # Теперь скрипт будет висеть в памяти, пока мы сами его не убьем
    updater.idle()

if __name__ == '__main__':
    main()