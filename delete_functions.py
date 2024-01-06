# delete_functions.py
import telebot

def delete_messages(bot, chat_id, message_ids):
    for message_id in message_ids:
        try:
            bot.delete_message(chat_id, message_id)
        except Exception as e:
            print(f"Error deleting message {message_id}: {e}")

def delete_message_by_text(bot, chat_id, text, reply_to_message_id=None):
    try:
        sent_message = bot.send_message(chat_id, text, reply_to_message_id=reply_to_message_id)
        message_id = sent_message.message_id
        return message_id
    except Exception as e:
        print(f"Error sending message: {e}")
        return None
