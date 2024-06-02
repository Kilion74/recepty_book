import requests  # pip install requests
from telebot import *
from bs4 import BeautifulSoup  # pip install bs4

# from transliterate import translit

TOKEN = '#'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def command(message):
    bot.reply_to(message, 'Введите название блюда...')
    bot.register_callback_query_handler(message, bodyes)


@bot.message_handler(content_types=['text'])
def bodyes(mess):
    name = mess.text.lower()
    # transliterated_text = translit(name, 'ru', reversed=True)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    url = f'https://povar.ru/xmlsearch?query={name}&page=1'
    data = requests.get(url, headers=headers).text
    block = BeautifulSoup(data, 'lxml')
    heads = block.find_all('div', class_='recipe')
    # print(len(heads))
    for i in heads:
        w = i.find_next('a').get('href')
        # print('https://povar.ru'+w)
        get_url = ('https://povar.ru' + w)
        sock = requests.get(get_url).text
        dock = BeautifulSoup(sock, 'lxml')
        head = dock.find('h1', class_='detailed fn')
        photo = dock.find('div', class_='bigImgBox').find('a').get('href')
        try:
            bot.send_photo(mess.chat.id, photo)
        except:
            bot.send_message(mess.chat.id, 'No photo')
        try:
            bot.send_message(mess.chat.id, head.text.strip())
        except:
            bot.send_message(mess.chat.id, 'No head')
        opiss = dock.find('span', class_='detailed_full description')
        bot.send_message(mess.chat.id, opiss.text.strip())
        sostav = dock.find('div', class_='ingredients_wrapper').find('h2')
        bot.send_message(mess.chat.id, sostav.text.strip(), parse_mode='Markdown')
        lists = dock.find('div', class_='ingredients_wrapper').find('ul').find_all('li')
        for el in lists:
            try:
                bot.send_message(mess.chat.id, ' '.join(el.text.strip().split()))
            except:
                continue
        # print(' '.join(lists[0].text.strip().split()))
        podhead = dock.find('h2', class_='span')
        try:
            bot.send_message(mess.chat.id, podhead.text.strip())
        except:
            continue
        try:
            instructiuns = dock.find('div', class_='instructions').find_all('div',
                                                                            class_='detailed_step_description_big')
            for det in instructiuns:
                try:
                    bot.send_message(mess.chat.id, ' '.join(det.text.strip().split()))

                    # print(det.text.strip())
                except:
                    continue
        except:
            # instructiuns = dock.find('span', itemprop='recipeInstructions')
            bot.send_message(mess.chat.id, "Данные отсутствуют")


bot.polling(none_stop=True)

