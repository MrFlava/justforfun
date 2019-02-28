from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sys
import PyPDF2
root = Tk()
root.title('Simple PDF reader')

def func(key, entry):
    if key == 'Показать содержимое документа':
        path = entry.get()
        doc = open(path, 'rb')
        reading_doc = PyPDF2.PdfFileReader(doc)
        pages = reading_doc.getNumPages()
        begins = reading_doc.getPage(0)
        content_pages = begins.extractText()
        content_pages.encode('utf-8')
        area_for_content.insert(1.0, content_pages)
    elif key == 'Выйти':
        root.after(1,root.destroy)
        sys.exit
entry = Entry(width=50)
buttons_list  = ["Показать содержимое документа","Выйти"]
r = 0
c = 0
for i in buttons_list:
     rel = ""
     commands = lambda x=i: func(x,entry)
     ttk.Button(root, text = i, command = commands , width = 50).grid(row = r, column = c,)
     c += 1
     if c > 4:
         c = 0
         r += 1
entry.grid(row = 0, column = 4)
area_for_content = Text(root, height = 20, width = 50, font = 'Arial 14')
area_for_content.grid(row=5,column=1)
root.mainloop()
