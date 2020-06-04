import json

import tkinter as tk
from tkinter import filedialog


def save():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.asksaveasfilename(defaultextension='.json')

    if len(file_path) == 0 or file_path == "()":
        return

    data = {}
    data['obstacles'] = []
    data['surfaces'] = []
    data['cup'] = []
    data['ball'] = []

    data['people'].append({
        'name': 'n',
        'pos': 'p',
        'dim': 'd'
    })

    with open(file_path, 'w') as outfile:
        json.dump(data, outfile)


def load():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()

    if len(file_path) == 0 or file_path == "()":
        return
