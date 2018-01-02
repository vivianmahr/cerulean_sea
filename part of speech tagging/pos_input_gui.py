"""
GUI for processing, tagging, and storing text in an output file. Mainly used for making tagged texts.
"""

import nltk
import tkinter as tk


def tag_sentence(sentence):
    s = nltk.word_tokenize(sentence)
    return nltk.pos_tag(s)

def get_tag_meanings():
    file = open("tag_meanings.txt", "r")
    text = file.read()
    file.close()
    text = text.split('\n')
    result = {}
    for tag in text:
        t = tag.split('\t')
        print(t)
        result[t[0]] = t[1]
    return result


class POS_Input_Display():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title = "POS Input"
        self.root.minsize(500, 300)
        self.frames = {
            "bottom": tk.Frame(self.root, padx=30, pady=15),
            "center": tk.Frame(self.root, padx=30, pady=15),
            "top": tk.Frame(self.root, padx=30, pady=15)
            }
        self.frames["top"].grid(sticky="new")
        self.frames["center"].grid(sticky="nsew")
        self.frames["bottom"].grid(sticky="sew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=0)
        self._setup_widgets()
        
    def _setup_widgets(self):
        self.frames["top"].columnconfigure(0, weight=10)
        self.frames["top"].columnconfigure(1, weight=1)
        self.text_input = tk.Entry(self.frames["top"])
        self.text_input.bind("<Return>", self.get_text)
        self.text_input.grid(row=0, column=0, sticky="we")

        input_button = tk.Button(self.frames["top"], text="Enter", command=self.get_text)
        input_button.grid(row=0, column=1, sticky="e")

        quit_button = tk.Button(self.frames["bottom"], text='Quit', command=self.quit)
        quit_button.pack(side=tk.TOP)

        placeholder_tag_lists = [("text", "tag"), ("text1", "tag2"), ("text1", "tag2")]

        self.text_display = tk.Label(self.frames["center"])
        self.text_display.pack(fill=tk.X)

    def quit(self):
        self.root.destroy()
        
    def get_text(self, event):
        self.text = self.text_input.get()
        self.display_text()
        
    def get_text_event(self, event):
        """Handles input getting when enter is pressed on the input panel"""
        self.get_text()

    def display_text(self):
        self.text_display.insert(tk.INSERT, self.text)
        
    def start(self):
        self.root.mainloop()
        
if __name__ == "__main__":
    disp = POS_Input_Display()
    disp.start()
