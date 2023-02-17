import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import json

# ---------------------------- SAVE & SHOW ALL ------------------------------- #
def save():
    """Add the inputs from the entry fields to data.json"""
    # get data from input
    university = university_input.get()
    program = program_input.get()
    link = link_input.get()
    add_info = additional_note_input.get("1.0", "end-1c")  # -1c deletes new line
    country = country_input.get()
    status = status_input.get()

    university_lower = university.lower()
    new_data = {
        university_lower: {
            "program": program,
            "link": link,
            "additional info": add_info,
            "country": country,
            "status": status,
        }
    }

    # show messagebox if entry field is empty
    if len(university) == 0 or len(link) == 0 or len(add_info) == 0 or len(country) ==0 or len(status) == 0:
        messagebox.showinfo(title="Empty box", message="Please don't leave any fields empty")
    else:
        try:  # read from file
            with open("data.json", mode="r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:  # file not found? write new file and add new_data
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:  # if file is found, add new_data to new line
            if university_lower not in data:
                data.update(new_data)
                with open("data.json", mode="w") as data_file:
                    json.dump(data, data_file, indent=4)
            else:
                messagebox.showinfo(title="Error", message="University exists in the data")
        finally:  # clear the input fields
            university_input.delete(0, END)
            link_input.delete(0, END)
            program_input.delete(0, END)
            additional_note_input.delete("1.0", END)
            country_input.delete(0, END)
            status_input.delete(0, END)

def show_all():
    """Show all data in treeview"""
    def show_item_info(event):
        """action when a university in treeview is double-clicked"""
        def update_json():
            """Save changes made"""

            value["program"] = program.get()
            value["link"] = link.get()
            value["additional info"] = additional_note.get("1.0", "end-1c")
            value["country"] = country.get()
            value["status"] = status.get()

            with open("data.json", mode="w") as info:
                json.dump(json_data_, info, indent=4)

        selected_uni_iid = tree_view.focus()
        index = tree_view.index(selected_uni_iid)
        uni_key = list(json_data_)[index]
        value = list(json_data_.values())[index]
        print(value)

        top_window = Toplevel(show_all_window)
        top_window.title(uni_key)
        top_window.config(bg='white')
        top_window.configure(pady=10, padx=10)


        # labels
        tw_program_label = Label(top_window, text="Program:", bg="white", highlightthickness=0)
        tw_program_label.grid(row=0, column=0, pady=5)
        tw_link_label = Label(top_window, text="Link:", bg="white")
        tw_link_label.grid(row=1, column=0, pady=5)
        tw_additional_note_label = Label(top_window, text="Additional note:", bg="white", highlightthickness=0)
        tw_additional_note_label.grid(row=2, column=0, pady=5)
        tw_country_label = Label(top_window, text="Country:", bg="white", highlightthickness=0)
        tw_country_label.grid(row=6, column=0, pady=5)
        tw_status_label = Label(top_window, text="status:", bg="white", highlightthickness=0)
        tw_status_label.grid(row=7, column=0, pady=5)

        # default texts in entry fields
        program = Entry(top_window, width=36)
        program.insert(0, f"{value['program']}")
        program.grid(row=0, column=1, columnspan=2, pady=5)
        link = Entry(top_window, width=36)
        link.insert(0, f"{value['link']}")
        link.grid(row=1, column=1, columnspan=2, pady=5)
        additional_note = Text(top_window, width=38, height=3, )
        additional_note.insert(1.0, f"{value['additional info']}")
        additional_note.grid(row=2, column=1, rowspan=3, columnspan=2, pady=5)
        country = Entry(top_window, width=36)
        country.insert(0, f"{value['country']}")
        country.grid(row=6, column=1, columnspan=2, pady=5)
        status = Entry(top_window, width=36)
        status.insert(0, f"{value['status']}")
        status.grid(row=7, column=1, columnspan=2, pady=5)

        # save change and close window button
        save_changes_button = Button(top_window, text='Save change', bg="#d0f2c7", width=10, command=update_json)
        save_changes_button.grid(row=8, column=1, pady=20)
        close_window_button = Button(top_window, text='Close', bg="#ff4040", width=10, command=top_window.destroy)
        close_window_button.grid(row=9, column=1, pady=20)

        top_window.wm_transient(show_all_window)

    try:
        with open("data.json", mode='r+') as data:
            json_data_ = json.load(data)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="You currently do not have any saved data")
    else:
        show_all_window = Toplevel(window)
        show_all_window.title('Data')
        show_all_window.config(bg='white')
        show_all_window.configure(pady=10, padx=10)

        # frame = Frame(show_all_window, width=1, height=1)
        # frame.grid(column=0, row=0, )
        # frame.pack_propagate(False)

        columns = ('universities',)  # column identifiers - tuple
        tree_view = ttk.Treeview(show_all_window, columns=columns, height=5, show='headings', style='Treeview', )
        tree_view.heading('universities', text='All Universities')
        tree_view.column(column='universities', width=750, stretch=True)
        # tree_view.rowconfigure(0, weight=1,) # configure the root grid rows
        tree_view.grid(column=0, row=0,)

        tree_view.bind('<Double-1>', show_item_info)

        tree_view_config = ttk.Style()
        tree_view_config.configure('Treeview', rowheight=35)

        for key in json_data_:
            tree_view.insert("", tkinter.END, values=(key,))

        scrollbar = ttk.Scrollbar(show_all_window, orient=tkinter.VERTICAL, command=tree_view.yview)
        tree_view.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(column=1, row=0, sticky=tkinter.N+tkinter.S)

# ---------------------------- PARENT WINDOW ------------------------------- #

window = Tk()
window.title("University Manager")
window.config(padx=50, pady=50, bg="white")

# image canvas
canvas = Canvas(height=200, width=200, bg="white", highlightthickness=0)
logo_image = PhotoImage(file="images.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(row=0, column=1, columnspan=1, pady=10)

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

show_all_button = Button(window, text='Show All', bg="#d0f2c7", width=35, command=show_all)
show_all_button.grid(row=11, column=1, columnspan=2, pady=10)

window.mainloop()