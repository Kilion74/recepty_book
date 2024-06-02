import requests  # pip install requests
from PIL import Image
from bs4 import BeautifulSoup  # pip install bs4

while True:
    print('Введите название блюда...')
    name = input()
    count = 1
    while count <= 3:
        url = f'https://povar.ru/xmlsearch?query={name}&page={count}'
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
            print(head.text.strip())
            pixx = dock.find('div', class_='bigImgBox').find('img').get('src')
            print(pixx)
            try:
                image = Image.open(pixx)
                image.show()
            except:
                print("Файл не найден.")
            opiss = dock.find('span', class_='detailed_full description')
            print(opiss.text.strip())
            sostav = dock.find('div', class_='ingredients_wrapper').find('h2')
            print(sostav.text.strip())
            lists = dock.find('div', class_='ingredients_wrapper').find('ul').find_all('li')
            for el in lists:
                print(' '.join(el.text.strip().split()))
            # print(' '.join(lists[0].text.strip().split()))
            podhead = dock.find('h2', class_='span')
            print(podhead.text.strip())
            try:
                instructiuns = dock.find('div', class_='instructions').find_all('div', class_='detailed_step_description_big')
                for det in instructiuns:
                    print(det.text.strip())
            except:
                instructiuns = dock.find('span', itemprop='recipeInstructions')
                print(instructiuns.text.strip())
            print('\n')
        count += 1

