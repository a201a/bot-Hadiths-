import telebot
import requests
from delete_functions import delete_message_by_text, delete_messages
from keep_alive import keep_alive
keep_alive()
token = '5938843430:AAHtP05uCN8oze5Od790CVG_k0tjJ-UYIgU'
api_url_hadith = 'https://dorar-hadith-api.mrmichael4.repl.co/v1/api/hadith/search?value='
api_url_degree = 'https://dorar-hadith-api.mrmichael4.repl.co/v1/data/degree'
api_url_book = 'https://dorar-hadith-api.mrmichael4.repl.co/v1/site/book/'
api_url_sharh = 'https://dorar-hadith-api.mrmichael4.repl.co/v1/site/sharh/text/'

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    start_message = "مرحبًا بك في بوت الحديث الشريف!\n\n" \
                    "يمكنك استخدام الأوامر التالية:\n" \
                    "/حديث [البحث عن حديث]\n" \
                    "/درجة [عرض درجات الأحاديث]\n" \
                    "/الكتاب [معلومات عن كتاب]\n" \
                    "/شرح [عرض شرح لحديث]"

    bot.send_message(chat_id, start_message)

@bot.message_handler(func=lambda message: message.text.lower() == 'مسح')
def handle_delete_message(message):
    chat_id = message.chat.id
    delete_text = ''
    
    # حذف الرسالة الأخيرة
    last_message_id = message.message_id - 1
    delete_messages(bot, chat_id, [last_message_id])

    # أرسل رسالة جديدة تؤكد على حدوث الحذف
    delete_message_by_text(bot, chat_id, delete_text)


def get_formatted_hadiths(hadiths):
    return [
        f"{hadith['hadith']}\nالراوي: {hadith['rawi']}\nالمحدث: {hadith['mohdith']}"
        f"\nالكتاب: {hadith['book']}\nالصفحة/الرقم: {hadith['numberOrPage']}"
        f"\nالتصنيف: {hadith['grade']}\n"
        for hadith in hadiths
    ]

@bot.message_handler(commands=['حديث'])
def search_hadith(message):
    chat_id = message.chat.id
    search_term = message.text.split(' ', 1)[1]

    try:
        response = requests.get(api_url_hadith + search_term)
        response.raise_for_status()
        hadiths = response.json()['data']
        formatted_hadiths = get_formatted_hadiths(hadiths)
        bot.send_message(chat_id, '\n'.join(formatted_hadiths))
    except requests.exceptions.RequestException as request_error:
        print('Error making request:', request_error)
        bot.send_message(chat_id, 'حدث خطأ أثناء البحث عن الأحاديث.')
    except Exception as error:
        print('Unexpected error:', error)
        bot.send_message(chat_id, 'حدث خطأ غير متوقع.')

@bot.message_handler(commands=['درجة'])
def get_hadith_degrees(message):
    chat_id = message.chat.id

    try:
        response = requests.get(api_url_degree)
        response.raise_for_status()
        degrees = response.json()['data']
        formatted_degrees = '\n'.join([f"{degree['key']}: {degree['value']}" for degree in degrees])
        bot.send_message(chat_id, formatted_degrees)
    except requests.exceptions.RequestException as request_error:
        print('Error making request:', request_error)
        bot.send_message(chat_id, 'حدث خطأ أثناء جلب درجات الأحاديث.')
    except Exception as error:
        print('Unexpected error:', error)
        bot.send_message(chat_id, 'حدث خطأ غير متوقع.')

@bot.message_handler(commands=['الكتاب'])
def get_book_info(message):
    chat_id = message.chat.id
    book_id = message.text.split(' ', 1)[1]

    try:
        response = requests.get(api_url_book + book_id)
        response.raise_for_status()
        book_info = response.json()['data']
        formatted_book_info = (
            f"اسم الكتاب: {book_info['name']}\n"
            f"المؤلف: {book_info['author']}\n"
            f"المحقق: {book_info['reviewer']}\n"
            f"الناشر: {book_info['publisher']}\n"
            f"الطبعة: {book_info['edition']}\n"
            f"سنة الطبعة: {book_info['editionYear']}\n"
        )
        bot.send_message(chat_id, formatted_book_info)
    except requests.exceptions.RequestException as request_error:
        print('Error making request:', request_error)
        bot.send_message(chat_id, 'حدث خطأ أثناء جلب معلومات الكتاب.')
    except Exception as error:
        print('Unexpected error:', error)
        bot.send_message(chat_id, 'حدث خطأ غير متوقع.')

@bot.message_handler(commands=['شرح'])
def get_hadith_sharh(message):
    chat_id = message.chat.id
    hadith_id = message.text.split(' ', 1)[1]

    try:
        response = requests.get(api_url_sharh + hadith_id)
        response.raise_for_status()
        hadith_info = response.json()['data']
        formatted_hadith_sharh = (
            f"الحديث: {hadith_info['hadith']}\n"
            f"الراوي: {hadith_info['rawi']}\n"
            f"المحدث: {hadith_info['mohdith']}\n"
            f"الكتاب: {hadith_info['book']}\n"
            f"الصفحة/الرقم: {hadith_info['numberOrPage']}\n"
            f"التصنيف: {hadith_info['grade']}\n"
            f"شرح الحديث: {hadith_info['sharhMetadata']['sharh']}"
        )
        bot.send_message(chat_id, formatted_hadith_sharh)
    except requests.exceptions.RequestException as request_error:
        print('Error making request:', request_error)
        bot.send_message(chat_id, 'حدث خطأ أثناء جلب شرح الحديث.')
    except Exception as error:
        print('Unexpected error:', error)
        bot.send_message(chat_id, 'حدث خطأ غير متوقع.')

if __name__ == "__main__":
    bot.polling()

