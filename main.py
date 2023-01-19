from tkinter import *
from tkinter import messagebox
import json

# ---------------------------- SAVE & SEARCH INPUT ------------------------------- #
def save():
    """Add the info from the inputs to data.json"""
    # get data from input
    university = university_input.get()
    program = program_input.get()
    link = link_input.get()
    add_info = additional_note_input.get("1.0", END)
    country = country_input.get()
    status = status_input.get()

    # data storage format
    new_data = {
        university: {
            "program": program,
            "link": link,
            "additional info": add_info,
            "country": country,
            "status": status,
        }
    }

    # if university or length field is empty show messagebox
    if len(university) == 0 or len(link) == 0 or len(add_info) == 0 or len(country) ==0 or len(status) == 0:
        messagebox.showinfo(title="Empty box", message="Please don't leave any fields empty")

    else:
        try:  # read from file
            with open("data.json", mode="r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:  # if file not found, write new file and add new_data
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:  # if file is found, add new_data to new line
            data.update(new_data)
            with open("data.json", mode="w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:  # clear the input fields
            university_input.delete(0, END)
            link_input.delete(0, END)
            program_input.delete(0, END)
            additional_note_input.delete("1.0", END)
            country_input.delete(0, END)
            status_input.delete(0, END)

def search():
    """Search through data.json and provide found details in new window"""
    search_term = search_input.get()
    try:
        with open("data.json") as data_file:
            json_data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if search_term in json_data:  # if input is a key in data.json
            # window for searched term
            top_window = Toplevel(window)
            top_window.title(f'{search_term}')
            top_window.config(bg='white')

            program = Label(top_window, text=f"Program: {json_data[search_term]['program']}", bg="white", highlightthickness=0)
            program.grid(row=1, column=0, pady=10)
            link = Label(top_window, text=f"Link: {json_data[search_term]['link']}", bg="white")
            link.grid(row=2, column=0, pady=10)
            additional_note= Label(top_window, text=f"Additional note: {json_data[search_term]['additional info']}", bg="white", highlightthickness=0)
            additional_note.grid(row=3, column=0, pady=10)
            country = Label(top_window, text=f"Country: {json_data[search_term]['country']}", bg="white", highlightthickness=0)
            country.grid(row=4, column=0, pady=10)
            status = Label(top_window, text=f"status: {json_data[search_term]['status']}", bg="white", highlightthickness=0)
            status.grid(row=5, column=0, pady=10)

            top_window.wm_transient(window)
        else:  # if term is not found show messagebox
            messagebox.showinfo(title="Error", message="University not found.\nCheck your spelling")

# ---------------------------- PARENT WINDOW ------------------------------- #

window = Tk()
window.title("University Manager")
window.config(padx=50, pady=50, bg="white")

# image canvas
canvas = Canvas(height=200, width=200, bg="white", highlightthickness=0)
logo_image = PhotoImage(file="images.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(row=0, column=0, columnspan=2, pady=10)

# labels
university_label = Label(window, text="University:", bg="white", highlightthickness=0)
university_label.grid(row=1, column=0, pady=5)
program_label = Label(window, text="Program:", bg="white", highlightthickness=0)
program_label.grid(row=2, column=0, pady=5)
link_label = Label(window, text="Link:", bg="white")
link_label.grid(row=3, column=0, pady=5)
additional_note_label = Label(window, text="Additional note:", bg="white", highlightthickness=0)
additional_note_label.grid(row=4, column=0, pady=5)
country_label = Label(window, text="Country:", bg="white", highlightthickness=0)
country_label.grid(row=8, column=0, pady=5)
status_label = Label(window, text="status:", bg="white", highlightthickness=0)
status_label.grid(row=9, column=0, pady=5)

# input fields
university_input = Entry(window, width=36)
university_input.focus()  # cursor goes to this input field
university_input.grid(row=1, column=1, columnspan=2, pady=5)
program_input = Entry(window, width=36)
program_input.grid(row=2, column=1, columnspan=2, pady=5)
link_input = Entry(window, width=36)
link_input.grid(row=3, column=1, columnspan=2, pady=5)
additional_note_input = Text(window, width=38, height=3, )
additional_note_input.grid(rowspan=3, row=4, column=1, columnspan=2, pady=5)
country_input = Entry(window, width=36)
country_input.grid(row=8, column=1, columnspan=2, pady=5)
status_input = Entry(window, width=36)
status_input.grid(row=9, column=1, columnspan=2, pady=5)

# add button
add_button = Button(window, text="Add", bg="#d0f2c7", width=35, command=save)
add_button.grid(row=10, column=1, columnspan=2, pady=10)

# search button and input field
search_button = Button(window, text='Search', bg="#d0f2c7", width=10, command=search)
search_button.grid(row=11, column=0)
search_input = Entry(window, width=36)
search_input.grid(row=11, column=1,)

window.mainloop()


