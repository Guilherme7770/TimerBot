import logging
from telegram.ext import (Updater, CommandHandler)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(bot, update):
    update.message.reply_text('Ola! Use /set <segundos> para definir o timer')

def alarm(bot, job):
    bot.send_message(job.context, text='beep')

def set_timer(bot, update, args, job_queue, chat_data):
    chat_id = update.message.chat_id
    
    try:
        due = int(args[0])
        if due < 0:
            update.message.reply_text('Tempo inválido!')
            return
        job = job_queue.run_once(alarm, due, context = chat_id)
        chat_data['job'] = job
        update.message.reply_text('Timer definido com sucesso!')
        
    except (IndexError, ValueError):
        update.message.reply_text('Uso: /set <segundos>')

def unset(bot, update, chat_data):
    if 'job' not in chat_data:
        update.message.reply_text('Você não tem nenhum timer definido')
        return
    
    job = chat_data['job']
    job.schedule_removal()
    del chat_data['job']
    
    update.message.reply_text('Timer desligado com sucesso!')

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

def main():
    updater = Updater('770069679:AAEb3EG5cu_UJBYNrzGEK41tiyo-ECRJmbw')
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', start))
    dp.add_handler(CommandHandler('set', set_timer,
                                  pass_args = True,
                                  pass_job_queue = True,
                                  pass_chat_data = True
                                  ))
    dp.add_handler(CommandHandler('unset', unset,
                                  pass_chat_data = True))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
