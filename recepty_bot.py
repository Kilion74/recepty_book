import requests  # pip install requests
# from PIL import Image
from telebot import *
from bs4 import BeautifulSoup  # pip install bs4

TOKEN = '#'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def command(message):
    bot.reply_to(message, 'Введите название блюда...')
    bot.register_callback_query_handler(message, bodyes)


@bot.message_handler(content_types=['text'])
def bodyes(mess):
    name = mess.text.lower()

    url = f'https://povar.ru/xmlsearch?query={name}&page=1'
    data = requests.get(url).text
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
        bot.reply_to(mess, head.text.strip())
        # pixx = dock.find('div', class_='bigImgBox').find('img').get('src')
        # try:
        #     image = Image.open(pixx)
        #     # image.show()
        #     bot.send_photo(mess.chat.id, image)
        # except FileNotFoundError:
        #     bot.reply_to(mess, "Файл не найден.")
        opiss = dock.find('span', class_='detailed_full description')
        bot.reply_to(mess, opiss.text.strip())
        sostav = dock.find('div', class_='ingredients_wrapper').find('h2')
        bot.reply_to(mess, sostav.text.strip())
        lists = dock.find('div', class_='ingredients_wrapper').find('ul').find_all('li')
        for el in lists:
            bot.reply_to(mess, ' '.join(el.text.strip().split()))
        # print(' '.join(lists[0].text.strip().split()))
        podhead = dock.find('h2', class_='span')
        bot.reply_to(mess, podhead.text.strip())
        try:
            instructiuns = dock.find('div', class_='instructions').find_all('div',
                                                                            class_='detailed_step_description_big')
            for det in instructiuns:
                bot.reply_to(mess, det.text.strip())
        except:
            instructiuns = dock.find('span', itemprop='recipeInstructions')
            bot.reply_to(mess, instructiuns.text.strip())


bot.polling(none_stop=True)
