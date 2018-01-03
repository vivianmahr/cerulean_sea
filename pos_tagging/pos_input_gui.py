"""
GUI for processing, tagging, and storing text in an output file. Mainly used for making tagged texts.

...It would be more convenient to make this a django project huh, and more to the end of what I want it to do.
And that would all be work using the POST and GET. 
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
        result[t[0]] = t[1]
    return result


class POS_Input_Display():
    def __init__(self):
        self._tag_meanings = get_tag_meanings()
        self._tag_dropdown = [tag for tag, meaning in self._tag_meanings.items()]
        self._sentence_inputs = []
        
        self.current_sentence = []
        
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
        self._setup_weights()
        self._setup_widgets()

    def _setup_weights(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=0)
        self.frames["top"].columnconfigure(0, weight=10)
        self.frames["top"].columnconfigure(1, weight=1)
        
    def _setup_widgets(self):
        self.text_input = tk.StringVar()
        text_input = tk.Entry(self.frames["top"], textvariable=self.text_input)
        #text_input.insert(tk.END, "This is a test sentence.")
        text_input.bind("<Return>", self.get_text_event)
        text_input.grid(row=0, column=0, sticky="we")

        input_button = tk.Button(self.frames["top"], text="Enter", command=self.get_text)
        input_button.grid(row=0, column=1, sticky="e")

        quit_button = tk.Button(self.frames["bottom"], text='Quit', command=self.quit)
        quit_button.pack(side=tk.TOP)
        
    def get_text(self):
        """Gets a sentence from the input form"""
        self.text = self.text_input.get()
        if self._sentence_inputs != []:
            self.save_sentence()
            to_delete = self.frames["center"].grid_slaves()
            for d in to_delete:
                d.destroy()
        self.display_text()
        self.text_input.set("")
        
    def get_text_event(self, event):
        """Handles input getting when enter is pressed on the input panel"""
        self.get_text()
        
    def display_text(self):
        self.sentence = tag_sentence(self.text)
        self._sentence_inputs = []
        for n in range(len(self.sentence)):
            text = self.sentence[n][0]
            tag = self.sentence[n][1]

            text_var = tk.StringVar()
            text_var.set(text)
            tag_var = tk.StringVar()
            #tag_var.set(tag + " - " + self._tag_meanings[tag])
            tag_var.set(tag)
            
            self._sentence_inputs.append((text_var, tag_var))
            
            entry = tk.Entry(self.frames["center"], textvariable=text_var)
            op_menu = tk.OptionMenu(self.frames["center"], tag_var, *self._tag_dropdown)

            entry.grid(row=int(n/5)*2, column=n%5)
            op_menu.grid(row=int(n/5)*2 + 1, column=n%5)

    def save_sentence(self):# Call this in more places besides quit
        sentence = []
        for textvar, tagvar in self._sentence_inputs:
            sentence.append((textvar.get(), tagvar.get()))
        with open("output.txt", "a") as output_file:
             output_file.write(repr(sentence) + "\n")
        
    def start(self):
        self.root.mainloop()
                  
    def quit(self):
        self.save_sentence()
        self.root.destroy()

if __name__ == "__main__":
    disp = POS_Input_Display()
    disp.start()
