import requests
import html
import tkinter as tk
from tkinter import ttk

color = "#FFFBE9"
easy_color = "#F4EAD5"
timer_color = "#181D31"
time_ = 60  # time for easy mode
entry_word_count = 0  # amount of words in entry_list
result_label = None
reset_button = None

def sentence_to_type():
    """get random sentence in list form from api"""
    sentence = ''
    parameters = {
        "amount": 10,
        "type": "boolean",
    }
    response = requests.get("https://opentdb.com/api.php", params=parameters)
    response.raise_for_status()
    data = response.json()
    results = data["results"]
    for data_ in results:
        # html.unescape - decode HTML entities in python string
        sentence += f'{html.unescape(data_["question"])} '
    split_sentence = sentence.split(' ')
    return list(split_sentence)

def click_entry(event):
    global time_
    reset_easy_time = time_

    def action_when_entry_is_clicked():
        """Countdown. Disable entry box at the end of the countdown. Show results. Reset button"""
        global time_
        if time_ != 0:  # if time is not equal to 0
            time_ -= 1
            timer_canvas.itemconfig(timer_text, text=f'{time_}')
            window.after(1000, func=action_when_entry_is_clicked)
        else:  # if time is equal to 0
            entry.config(state=tk.DISABLED)  #disable entry box
            result(wpm_=wpm(), accuracy_=accuracy())  # show results

    def result(wpm_, accuracy_):
        """Display results on screen"""
        global result_label, reset_button
        window.geometry('1200x1000')
        result_label = ttk.Label(window, text=f'WPM: {wpm_}\nAccuracy: {accuracy_}', foreground=timer_color,
                                 background=easy_color, font=("arial", 15, 'bold'), style='TLabel')
        result_label.grid(column=0, row=5, pady=50, columnspan=2)

        # reset button
        reset_button = ttk.Button(window, text='Reset', command=reset)
        reset_button.grid(column=0, row=6, columnspan=2, pady=50)

        # print(len(sentence_list))
        # print(entry.get().split())

    def wpm():
        """calculate words per minute"""
        global entry_word_count
        entry_list = (entry.get().split())  # split entry into list
        entry_word_count = len(entry_list)  # amount of words in entry_list

        for i in range(0, len(entry.get().split())):
            # if current word from entry is not equal to word in the sentence displayed
            if entry_list[i] != sentence_list[i]:
                entry_word_count -= 1  # minus one
        return  entry_word_count

    def accuracy():
        """Calculate typing accuracy"""
        accuracy_calc = entry_word_count / (len(entry.get().split())) * 100
        return round(accuracy_calc, 2)   # rounded to two decimal place

    def reset():
        """reset button"""
        global time_, result_label, reset_button
        time_ = reset_easy_time
        sentence_label.configure(text=next_sentence())  # add new sentence
        timer_canvas.itemconfig(timer_text, text=f'{reset_easy_time}')  # reset time to initial time before countdown
        entry.config(state=tk.NORMAL)
        entry.delete(0, 'end')
        result_label.destroy()  # remove displayed results
        reset_button.destroy()  # remove reset button
        window.geometry('1200x800')  # reset window size

    def next_sentence():
        """makes new sentence"""
        global sentence_list, sentence_joined
        sentence_list = sentence_to_type()[:-1]
        sentence_joined = ' '.join(sentence_list)
        return sentence_joined

    action_when_entry_is_clicked()

#---------- Sentence ----------#
sentence_list = sentence_to_type()[:-1]
sentence_joined = ' '.join(sentence_list)

#---------- GUI ----------#
window = tk.Tk()
window.title('TYPING SPEED TEST')
window.geometry('1200x800')
window.config(padx=100, pady=50, bg=easy_color)

# timer label
style = ttk.Style()
style.configure('TLabel', foreground='red')
timer_label = ttk.Label(window, text='Time Left:', foreground=timer_color, background=easy_color,
                      font=("arial", 15, 'bold'), style='TLabel')
timer_label.grid(column=0, row=0,)

# timer canvas
timer_canvas = tk.Canvas(window, height=30, width=300, bg=easy_color, highlightthickness=0)
timer_text = timer_canvas.create_text(150, 15, text=f"{time_}", fill=timer_color, font=("arial", 15, 'bold'))
timer_canvas.grid(column=1, row=0,)

# sentence label
sentence_label = ttk.Label(window, text=sentence_joined, background=easy_color, foreground='black',
                           wraplength=900, justify="left",)
sentence_label.grid(column=0, row=3, pady=50, columnspan=3 )

# entry
entry = tk.Entry(window, width=52)
entry.grid(column=0, row=4, columnspan=3)
entry.bind("<Button-1>", func=click_entry)

window.mainloop()