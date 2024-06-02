import requests
from PIL import Image
from bs4 import BeautifulSoup
import tkinter as tk


def search_recipe():
    name = entry.get()
    count = 1
    while count <= 3:
        url = f'https://povar.ru/xmlsearch?query={name}&page={count}'
        data = requests.get(url).text
        block = BeautifulSoup(data, 'lxml')
        heads = block.find_all('div', class_='recipe')
        for i in heads:
            w = i.find_next('a').get('href')
            get_url = 'https://povar.ru' + w
            sock = requests.get(get_url).text
            dock = BeautifulSoup(sock, 'lxml')
            head = dock.find('h1', class_='detailed fn')
            pixx = dock.find('div', class_='bigImgBox').find('img').get('src')
            try:
                image = Image.open(requests.get(pixx, stream=True).raw)
                image.show()
            except:
                print("Файл не найден.")
            opiss = dock.find('span', class_='detailed_full description')
            sostav = dock.find('div', class_='ingredients_wrapper').find('h2')
            lists = dock.find('div', class_='ingredients_wrapper').find('ul').find_all('li')
            podhead = dock.find('h2', class_='span')
            try:
                instructiuns = dock.find('div', class_='instructions').find_all('div',
                                                                                class_='detailed_step_description_big')
            except:
                instructiuns = dock.find('span', itemprop='recipeInstructions')

        count += 1


# GUI setup
root = tk.Tk()
root.title("Recipe Search")

label = tk.Label(root, text="Enter dish name:")
label.pack()

entry = tk.Entry(root)
entry.pack()

btn = tk.Button(root, text="Search", command=search_recipe)
btn.pack()

root.mainloop()


