import ttkbootstrap as ttk  # importing the GUI library
import random   # importing the module to generate random numbers

# dictionary containing all the exercises and its properties
EXERCISE_DICT = {
    'Addition': {
        'symbol': '+',  # symbol of operation
        'range_1': (100000, 999999),  # range of values to choose the first number
        'range_2': (100000, 999999),  # range of values to choose the second number
        'operation': lambda num1, num2: num1 + num2,  # the operation you have to do to get the answer
        'button_pos': (1, 0),  # position of the button corresponding to the exercise in home page
    },
    'Subtraction': {
        'symbol': '-',
        'range_1': (500000, 999999),
        'range_2': (100000, None),
        'operation': lambda num1, num2: num1 - num2,
        'button_pos': (1, 1),
    },
    'Multiplication': {
        'symbol': '×',
        'range_1': (100, 999),
        'range_2': (10, 99),
        'operation': lambda num1, num2: num1 * num2,
        'button_pos': (2, 0),
    },
    'Division': {
        'symbol': '÷',
        'range_1': (1000, 9999),
        'range_2': (10, 25),
        'operation': lambda num1, num2: num1 // num2,
        'button_pos': (2, 1),
    },
}


def change_page(exercise):
    """Changes the page according to the selected exercise"""

    # destroying the widgets of previous page
    for widget in window.winfo_children():
        widget.destroy()

    # generating random numbers according to the exercise
    range_1 = EXERCISE_DICT[exercise]['range_1']
    range_2 = EXERCISE_DICT[exercise]['range_2']
    num1 = random.randint(range_1[0], range_1[1])
    num2 = random.randint(range_2[0], range_2[1] if range_2[1] else num1)

    # making a dummy variable
    remainder_entry = ttk.Entry()

    # making the label for the first number
    num1_label = ttk.Label(text=num1, font=('Helvetica', 50))
    num1_label.grid(row=0, column=0, columnspan=2)

    # making the label for the operator
    ttk.Label(
        text=EXERCISE_DICT[exercise]['symbol'],
        font=('Helvetica', 50),
    ).grid(row=0, column=2)

    # making the label for the second number
    num2_label = ttk.Label(
        text=num2,
        font=('Helvetica', 50),
        justify='right',
        anchor='e',
        width=len(str(num1)),
    )
    num2_label.grid(row=1, column=0, columnspan=2)

    # making the button to check the answer
    check_button = ttk.Button(
        text='Check Your Answer',
        style='light.TButton',
        width=20,
        command=lambda: check_answer(
            exercise,
            num1,
            num2,
            solution_entry.get(),
            remainder_entry.get()
        ),
    )
    check_button.grid(row=0, column=3, padx=(75, 0), columnspan=2)

    if exercise != 'Division':
        # making the entry for entering the solution
        solution_entry = ttk.Entry(style='light', font=('Helvetica', 25), width=len(str(num1))*2)
        solution_entry.grid(row=2, column=0)

    else:
        # making the adjusted solution(quotient) entry if it is division
        solution_entry = ttk.Entry(
            style='light',
            font=('Helvetica', 25),
            width=3,
            foreground='grey',
        )
        solution_entry.insert(0, 'Q:')  # adding the placeholder
        solution_entry.grid(row=2, column=0)
        # binding the entry to a function that removes placeholder on focus event
        solution_entry.bind(
            '<FocusIn>',
            func=lambda event,
            entry=solution_entry: on_focus(event, entry)
        )

        # making the entry for entering the remainder
        remainder_entry = ttk.Entry(
            style='light',
            font=('Helvetica', 25),
            width=3,
            foreground='grey',
        )
        remainder_entry.insert(0, 'R:')  # adding the placeholder
        remainder_entry.grid(row=2, column=1)
        # binding the entry to a function that removes placeholder on focus event
        remainder_entry.bind(
            '<FocusIn>',
            func=lambda event,
            entry=remainder_entry: on_focus(event, entry)
        )


def on_focus(event, entry):
    """Removes the placeholder of an entry"""

    if entry.cget('foreground') != 'white':
        entry.delete(0, ttk.END)
        entry.config(foreground='white')


def check_answer(exercise, num1, num2, solution, remainder=None):
    """Checks the answer given by the user"""

    # creating the label to show the result
    result_label = ttk.Label(font=('Helvetica', 25))
    result_label.grid(row=1, column=3, padx=(50, 0), columnspan=2)

    try:
        # converting the solution and reminder from string to integer
        solution = int(solution)
        remainder = int(remainder)
    except ValueError:
        # if the string is not an integer, calls the wrong_answer() function
        wrong_answer(result_label)

    if solution == EXERCISE_DICT[exercise]['operation'](num1, num2):  # seeing if the answer is correct
        if exercise == 'Division':  # seeing if the exercise is division
            if remainder == num1 % num2:  # if it is, checking if the remainder is correct
                correct_answer(result_label, exercise)
            else:
                wrong_answer(result_label)
        else:   # if it is not division
            correct_answer(result_label, exercise)
    else:
        wrong_answer(result_label)


def correct_answer(label, exercise):
    """Activates if the given answer is correct and
     shows the user answer is correct and
     gives the option to go to the main page or
     to do the next question"""

    # changing the result label to show the answer is correct
    label.configure(bootstyle='success', text='✓ Correct Answer!')

    # creating the home button
    home_button = ttk.Button(
        text='Home',
        command=lambda: main(),  # goes to the home page
        style='light.TButton',
        width=5
    )
    home_button.grid(row=2, column=3, padx=(85, 0))

    # creating the button to attempt the next question
    next_button = ttk.Button(
        text='Next',
        command=lambda: change_page(exercise),  # goes to another question of same exercise
        style='light.TButton',
        width=5
    )
    next_button.grid(row=2, column=4)


def wrong_answer(label):
    """Activates when the given answer is wrong and
    shows the user the answer is wrong"""

    # changing the result label to show the answer is wrong
    label.configure(bootstyle='danger', text='❌ Wrong Answer')
    label.after(1000, lambda: label.destroy())


def main():
    """The main page"""

    # destroying the widgets of previous page
    for widget in window.winfo_children():
        widget.destroy()

    # creating the label that tells the user to choose an exercise
    choice_label = ttk.Label(text='Choose The Exercise', font=('Helvetica', 60))
    choice_label.grid(row=0, column=0, columnspan=2, pady=(0, 30))

    # making a customised button style
    button_style = ttk.Style()
    button_style.configure(style='light.TButton', font=('Helvetica', 20))

    # looping through the exercise dictionary and creating a button for each of them
    for exercise, properties in EXERCISE_DICT.items():
        button_pos = properties['button_pos']

        ttk.Button(
            text=exercise,
            style='light.TButton',
            width=20,
            command=lambda ex=exercise: change_page(ex)
        ).grid(
            row=button_pos[0],
            column=button_pos[1],
            pady=(20, 0)
        )


if __name__ == '__main__':
    # creating the window
    window = ttk.Window(
        title='Arithmetic',
        themename='cyborg',
        iconphoto=r'C:\Users\hp\PycharmProjects\arithmetic\icon.png',
    )
    window.config(padx=100, pady=100)
    main()  # starting the home page
    window.mainloop()
