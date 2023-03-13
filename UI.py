import query 
import os
from bs4 import BeautifulSoup
import tkinter as tk
import json


def search(queryInput):
    docIdList = list()
    resultList = list()
    searchResults = query.queryScore(queryInput)
    bookkeeping = json.load(open('bookkeeping.json'))
    for i in searchResults:
        docIdList.append(i[0])

    for x, i in enumerate(docIdList):
        path = "WEBPAGES_RAW" + "/" + str(i)

        pageReader = open(path, encoding='utf-8')
        content = pageReader.read()
        soup = BeautifulSoup(content, features="lxml")
        title = soup.find('title')
        if title:
            title_text = title.get_text() .strip()
            addString = str(x+1) + "." +" " + title_text
        resultList.append(addString)
        resultList.append('\t' + bookkeeping[i])
        text = soup.get_text().strip()
        firstTen = (text.split()[:15])
        resultList.append('\t' + " ".join(firstTen))
        

    return resultList


def update_results():
    query = search_bar.get()

    results_box.delete("1.0", "end")

    results = search(query)

    for result in results:
        results_box.insert("end", result + "\n")

window = tk.Tk()

window.title("CS 121 Project 3")
window.attributes('-fullscreen', True)

image = tk.PhotoImage(file="121picture.png")

image_label = tk.Label(window, image=image)
image_label.pack()

search_bar = tk.Entry(window, width=100)
search_bar.pack(padx=10, pady=10, anchor="center")  

search_button = tk.Button(window, text="Search", command=update_results)
search_button.pack(padx=10, pady=10)

results_box = tk.Text(window,width=1000)
results_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

window.mainloop()
