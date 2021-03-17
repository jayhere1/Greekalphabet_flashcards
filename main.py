import pandas
from tkinter import *
import random

BACKGROUND_COLOR = "#B1DDC6"

# ---------------------------- Words setup ------------------------------- #

try:
    data = pandas.read_csv("words_to_learn.csv")
    to_learn = data.to_dict(orient="records")
except FileNotFoundError:
    data = pandas.read_csv("greek_letters.csv")
    to_learn = data.to_dict(orient="records")

current_card = {}


def card_known():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="Greek", fill="black")
    canvas.itemconfig(card_word, text=current_card["Greek"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=after_screen)


def card_unknown():
    to_learn.remove(current_card)
    card_known()
    data_frame = pandas.DataFrame(to_learn)
    data_frame.to_csv("words_to_learn.csv", index=False)


def after_screen():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["Alphabet"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=after_screen)

# Cards

canvas = Canvas(height=526, width=800, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
canvas.config(bg=BACKGROUND_COLOR)
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# Buttons
wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, borderwidth=0, command=card_unknown)
wrong_button.grid(row=1, column=0)

right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, highlightthickness=0, borderwidth=0, command=card_known)
right_button.grid(row=1, column=1)

card_known()

window.mainloop()
