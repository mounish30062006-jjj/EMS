from customtkinter import *
from PIL import Image, ImageOps
from tkinter import ttk, messagebox
import database
import pandas as pd
from tkinter import filedialog
import shutil
import os
import sys
import tkinter as tk

# Global variables for pagination
all_data = []
current_page = 1
uploaded_image_path = ""


def resource_path(filename):
    """Find a file next to this script, whether run normally or bundled by PyInstaller."""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)


def validate_fields():
    """Returns an error message string, or None if everything is valid."""
    if (idEntry.get() == '' or phoneEntry.get() == '' or nameEntry.get().strip() == ''
            or roleBox.get() == '' or genderBox.get() == '' or salaryEntry.get() == ''):
        return 'All Fields Are Required'

    phone = phoneEntry.get().strip()
    if not phone.isdigit() or len(phone) != 10:
        return 'Phone number must be exactly 10 digits'

    salary = salaryEntry.get().strip()
    try:
        if float(salary) < 0:
            return 'Salary cannot be negative'
    except ValueError:
        return 'Salary must be a number'

    return None


# Functions
def upload_image():
    emp_id = idEntry.get()
    if not emp_id:
        messagebox.showerror("Error", "Please enter or select an Employee ID first")
        return

    file_path = filedialog.askopenfilename(
        title="Select Image to Upload",
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")]
    )
    if file_path:
        if not os.path.exists("employee_images"):
            os.makedirs("employee_images")

        _, ext = os.path.splitext(file_path)
        filename = f"{emp_id}{ext}"
        destination = os.path.join("employee_images", filename)

        try:
            for file in os.listdir("employee_images"):
                if file.startswith(f"{emp_id}."):
                    os.remove(os.path.join("employee_images", file))

            shutil.copy(file_path, destination)
            messagebox.showinfo("Success", "Image Uploaded to System Successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload image: {str(e)}")


def view_image():
    emp_id = idEntry.get()
    if not emp_id:
        messagebox.showerror("Error", "Please enter or select an Employee ID first")
        return

    if not os.path.exists("employee_images"):
        messagebox.showerror("Error", "No images uploaded yet")
        return

    img_path = None
    for file in os.listdir("employee_images"):
        name, _ = os.path.splitext(file)
        if name == emp_id:
            img_path = os.path.join("employee_images", file)
            break

    if img_path:
        try:
            top = CTkToplevel()
            top.title(f"Employee {emp_id} Image")
            top.geometry("450x450")
            top.attributes('-topmost', True)

            img_data = Image.open(img_path)
            target_size = (400, 400)
            img_data.thumbnail(target_size, Image.Resampling.LANCZOS)
            ctk_img = CTkImage(img_data, size=img_data.size)

            lbl = CTkLabel(top, image=ctk_img, text="")
            lbl.pack(expand=True, fill='both', padx=20, pady=20)

            caption = CTkLabel(top, text=f"ID: {emp_id}", font=('arial', 12))
            caption.pack(pady=5)

            top.focus()

        except Exception as e:
            messagebox.showerror('Error', f'Could not open image: {str(e)}')
    else:
        messagebox.showinfo("Info", "No image found for this Employee ID")


def display_data():
    global current_page, all_data
    tree.delete(*tree.get_children())
    start = (current_page - 1) * 10
    end = start + 10
    for employee in all_data[start:end]:
        tree.insert('', END, values=employee)

    if 'pageLabel' in globals():
        pageLabel.configure(text=f"Page {current_page}")


def next_page():
    global current_page
    if current_page * 10 < len(all_data):
        current_page += 1
        display_data()


def prev_page():
    global current_page
    if current_page > 1:
        current_page -= 1
        display_data()


def export_to_excel():
    employees = database.fetch_employees()

    if not employees:
        messagebox.showerror('Error', 'No data available to export')
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel Files", "*.xlsx")],
        title="Save Employee Data"
    )

    if not file_path:
        return

    try:
        df = pd.DataFrame(
            employees,
            columns=['Id', 'Name', 'Phone', 'Role', 'Gender', 'Salary', 'Image_Path']
        )
        df.to_excel(file_path, index=False)
        messagebox.showinfo('Success', 'Employee data exported successfully')
    except Exception as e:
        messagebox.showerror('Error', f'Failed to export: {str(e)}')


def delete_all():
    result = messagebox.askyesno('Confirm', 'Do You Really Want To Delete All The Records ?')
    if result:
        database.deleteall_records()
        treeview_data()
    else:
        pass


def show_all():
    treeview_data()
    searchEntry.delete(0, END)
    searchBox.set('Search By')


def filter_by_id():
    dialog = CTkToplevel(window)
    dialog.title("Filter by ID")

    window_width = 300
    window_height = 150
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")
    dialog.resizable(False, False)
    dialog.attributes('-topmost', True)

    label = CTkLabel(dialog, text="Enter Employee ID:", font=('arial', 14))
    label.pack(pady=10)

    entry = CTkEntry(dialog, font=('arial', 14))
    entry.pack(pady=5)
    entry.focus()

    user_input = {"value": None}

    def on_submit():
        user_input["value"] = entry.get()
        dialog.destroy()

    submit_btn = CTkButton(dialog, text="OK", command=on_submit, width=100)
    submit_btn.pack(pady=15)

    dialog.transient(window)
    dialog.grab_set()
    window.wait_window(dialog)

    emp_id = user_input["value"]

    if emp_id:
        global all_data, current_page
        searched_data = database.search_by_exact_id(emp_id)
        if searched_data:
            all_data = searched_data
            current_page = 1
            display_data()
        else:
            messagebox.showinfo('Result', 'No Employee Found with that ID')


def search_employee():
    if searchEntry.get() == '':
        messagebox.showerror('Error', 'Enter Value To Search')
    elif searchBox.get() == 'Search By':
        messagebox.showerror('Error', 'Please Select An Option')
    else:
        global all_data, current_page
        searched_data = database.search(searchBox.get(), searchEntry.get())

        if searched_data:
            all_data = searched_data
            current_page = 1
            display_data()
        else:
            tree.delete(*tree.get_children())
            all_data = []
            display_data()
            messagebox.showinfo('Result', 'No Data Found')


def delete_employee():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror('Error', 'Select Data To Delete')
    else:
        result = messagebox.askyesno('Confirm', 'Delete this employee record?')
        if result:
            database.delete(idEntry.get())
            treeview_data()
            clear()
            messagebox.showinfo('Success', 'Data Is Deleted')


def update_employee():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror('Error', 'Select Data To Update')
        return

    error = validate_fields()
    if error:
        messagebox.showerror('Error', error)
        return

    database.update(idEntry.get(), nameEntry.get(), phoneEntry.get(), roleBox.get(), genderBox.get(), salaryEntry.get(), "")
    treeview_data()
    clear()
    messagebox.showinfo('Success', 'Data Is Updated')


def selection(event):
    selected_item = tree.selection()
    if selected_item:
        row = tree.item(selected_item)['values']
        clear()
        idEntry.insert(0, row[0])
        idEntry.configure(state='disabled')
        nameEntry.insert(0, row[1])
        phoneEntry.insert(0, row[2])
        roleBox.set(row[3])
        genderBox.set(row[4])
        salaryEntry.insert(0, row[5])


def clear(value=False):
    if value:
        tree.selection_remove(tree.focus())
    idEntry.configure(state='normal')
    idEntry.delete(0, END)
    nameEntry.delete(0, END)
    phoneEntry.delete(0, END)
    roleBox.set('')
    genderBox.set('')
    salaryEntry.delete(0, END)


def treeview_data():
    global all_data, current_page
    all_data = database.fetch_employees()
    current_page = 1
    display_data()


def add_employee():
    error = validate_fields()
    if error:
        messagebox.showerror('Error', error)
        return

    if database.id_exists(idEntry.get()):
        messagebox.showerror('Error', 'Id already exists')
        return

    database.insert(idEntry.get(), nameEntry.get(), phoneEntry.get(), roleBox.get(), genderBox.get(), salaryEntry.get(), "")
    treeview_data()
    clear()
    messagebox.showinfo('Success', 'Data Is Added')


# ============== GUI PART ==============
window = CTk()


def _suppress_harmless_tcl_errors(exc, val, tb):
    if issubclass(exc, tk.TclError) and "invalid command name" in str(val):
        return
    import traceback
    traceback.print_exception(exc, val, tb)


window.report_callback_exception = _suppress_harmless_tcl_errors

window.geometry('1400x820+60+40')
window.minsize(1100, 650)
window.resizable(True, True)
window.title('Employee Management System')
window.configure(fg_color='#161C30')

try:
    window.state('zoomed')
except Exception:
    pass

# Root grid: row0 = header (fixed height), row1 = main content (stretches), row2 = button bar (fixed)
window.grid_rowconfigure(0, weight=0)
window.grid_rowconfigure(1, weight=1)
window.grid_rowconfigure(2, weight=0)
window.grid_columnconfigure(0, weight=1)

# ---- Header banner: scales width with the window, fixed height ----
HEADER_HEIGHT = 130
header_container = CTkFrame(window, height=HEADER_HEIGHT, fg_color='#0d1326', corner_radius=0)
header_container.grid(row=0, column=0, sticky='ew')
header_container.grid_propagate(False)

header_label = CTkLabel(header_container, text='')
header_label.place(relx=0, rely=0, relwidth=1, relheight=1)

_header_source = None
try:
    _header_source = Image.open(resource_path('bg.jpeg'))
except FileNotFoundError:
    pass

_title_overlay = CTkLabel(header_container, text='Employee Management System',
                           font=('Segoe UI', 28, 'bold'), text_color='white')
_title_overlay.place(relx=0.03, rely=0.5, anchor='w')

_last_header_w = [0]


def _resize_header(event=None):
    if _header_source is None:
        return
    w = header_container.winfo_width()
    if w < 2 or w == _last_header_w[0]:
        return
    _last_header_w[0] = w
    fitted = ImageOps.fit(_header_source, (w, HEADER_HEIGHT), Image.LANCZOS)
    ctk_img = CTkImage(fitted, size=(w, HEADER_HEIGHT))
    header_label.configure(image=ctk_img)
    header_label.image = ctk_img


header_container.bind('<Configure>', _resize_header)

# ---- Main content: left form (fixed-ish) + right search/table (stretches) ----
content = CTkFrame(window, fg_color='#161C30')
content.grid(row=1, column=0, sticky='nsew', padx=20, pady=15)
content.grid_columnconfigure(0, weight=0)
content.grid_columnconfigure(1, weight=1)
content.grid_rowconfigure(0, weight=1)

leftFrame = CTkFrame(content, fg_color='#1b2440', corner_radius=14)
leftFrame.grid(row=0, column=0, sticky='ns', padx=(0, 15))

idLabel = CTkLabel(leftFrame, text='Id', font=('arial', 18, 'bold'), text_color='whitesmoke')
idLabel.grid(row=0, column=0, padx=20, pady=15, sticky='s')

idEntry = CTkEntry(leftFrame, font=('arial', 15, 'bold'), width=200)
idEntry.grid(row=0, column=1)

nameLabel = CTkLabel(leftFrame, text='Name', font=('arial', 18, 'bold'), text_color='whitesmoke')
nameLabel.grid(row=1, column=0, padx=20, pady=15, sticky='s')

nameEntry = CTkEntry(leftFrame, font=('arial', 15, 'bold'), width=200)
nameEntry.grid(row=1, column=1)

phoneLabel = CTkLabel(leftFrame, text='Phone', font=('arial', 18, 'bold'), text_color='whitesmoke')
phoneLabel.grid(row=2, column=0, padx=20, pady=15, sticky='s')

phoneEntry = CTkEntry(leftFrame, font=('arial', 15, 'bold'), width=200)
phoneEntry.grid(row=2, column=1)

roleLabel = CTkLabel(leftFrame, text='Role', font=('arial', 18, 'bold'), text_color='whitesmoke')
roleLabel.grid(row=3, column=0, padx=20, pady=15, sticky='s')

role_options = ['Web Developer', 'Cloud Architect', 'Technical Writer', 'Network Engineer', 'DevOps Engineer',
                'Data Scientist', 'Business Analyst', 'IT Consultant', 'UI/UX Designer']
roleBox = CTkComboBox(leftFrame, values=role_options, width=200, font=('arial', 15, 'bold'), state='readonly')
roleBox.grid(row=3, column=1)

genderLabel = CTkLabel(leftFrame, text='Gender', font=('arial', 18, 'bold'), text_color='whitesmoke')
genderLabel.grid(row=4, column=0, padx=20, pady=15, sticky='s')

gender_options = ['Male', 'Female']
genderBox = CTkComboBox(leftFrame, values=gender_options, width=200, font=('arial', 15, 'bold'), state='readonly')
genderBox.grid(row=4, column=1)

salaryLabel = CTkLabel(leftFrame, text='Salary', font=('arial', 18, 'bold'), text_color='whitesmoke')
salaryLabel.grid(row=5, column=0, padx=20, pady=15, sticky='s')

salaryEntry = CTkEntry(leftFrame, font=('arial', 15, 'bold'), width=200)
salaryEntry.grid(row=5, column=1, pady=(0, 20))

# ---- Right side: search bar + table (both stretch) ----
rightFrame = CTkFrame(content, fg_color='#1b2440', corner_radius=14)
rightFrame.grid(row=0, column=1, sticky='nsew')
rightFrame.grid_columnconfigure(0, weight=1)
rightFrame.grid_rowconfigure(1, weight=1)

searchRow = CTkFrame(rightFrame, fg_color='transparent')
searchRow.grid(row=0, column=0, sticky='ew', padx=15, pady=(15, 10))
searchRow.grid_columnconfigure(5, weight=1)

search_options = ['Id', 'Name', 'Phone', 'Role', 'Gender', 'Salary']
filterButton = CTkButton(searchRow, text='Filter Box', width=110, command=filter_by_id)
filterButton.grid(row=0, column=0, padx=5)

searchBox = CTkComboBox(searchRow, values=search_options, state='readonly', width=130)
searchBox.grid(row=0, column=1, padx=5)
searchBox.set('Search By')

searchEntry = CTkEntry(searchRow, font=('arial', 15, 'bold'), width=160)
searchEntry.grid(row=0, column=2, padx=5)

searchButton = CTkButton(searchRow, text='Search', width=100, command=search_employee)
searchButton.grid(row=0, column=3, padx=5)

showallButton = CTkButton(searchRow, text='Show All', width=100, command=show_all)
showallButton.grid(row=0, column=4, padx=5)

# Table area (expands both directions)
tableFrame = CTkFrame(rightFrame, fg_color='transparent')
tableFrame.grid(row=1, column=0, sticky='nsew', padx=15, pady=(0, 10))
tableFrame.grid_columnconfigure(0, weight=1)
tableFrame.grid_rowconfigure(0, weight=1)

tree = ttk.Treeview(tableFrame)
tree.grid(row=0, column=0, sticky='nsew')

vsb = ttk.Scrollbar(tableFrame, orient='vertical', command=tree.yview)
vsb.grid(row=0, column=1, sticky='ns')
tree.configure(yscrollcommand=vsb.set)

tree['columns'] = ('Id', 'Name', 'Phone', 'Role', 'Gender', 'Salary')
tree.heading('Id', text='Id')
tree.heading('Name', text='Name')
tree.heading('Phone', text='Phone')
tree.heading('Role', text='Role')
tree.heading('Gender', text='Gender')
tree.heading('Salary', text='Salary')

tree.config(show='headings')
tree.column('Id', width=70, stretch=True)
tree.column('Name', width=160, stretch=True)
tree.column('Phone', width=140, stretch=True)
tree.column('Role', width=180, stretch=True)
tree.column('Gender', width=90, stretch=True)
tree.column('Salary', width=110, stretch=True)

style = ttk.Style()
style.theme_use('default')
style.configure('Treeview.Heading', font=('arial', 11, 'bold'))
style.configure('Treeview', font=('arial', 10, 'bold'), rowheight=26, background='#161C30',
                 fieldbackground='#161C30', foreground='whitesmoke')
style.map('Treeview', background=[('selected', '#2e8b86')])

pagerRow = CTkFrame(rightFrame, fg_color='transparent')
pagerRow.grid(row=2, column=0, pady=(0, 12))

prevButton = CTkButton(pagerRow, text='<', width=50, command=prev_page)
prevButton.grid(row=0, column=0, padx=10)

pageLabel = CTkLabel(pagerRow, text='Page 1', font=('arial', 14, 'bold'))
pageLabel.grid(row=0, column=1, padx=10)

nextButton = CTkButton(pagerRow, text='>', width=50, command=next_page)
nextButton.grid(row=0, column=2, padx=10)

# ---- Bottom button bar ----
buttonFrame = CTkFrame(window, fg_color='#161C30')
buttonFrame.grid(row=2, column=0, pady=16)

newButton = CTkButton(buttonFrame, text='New Employee', font=('arial', 14, 'bold'), width=130, corner_radius=15, command=lambda: clear(True))
newButton.grid(row=0, column=0, pady=5, padx=4)

addButton = CTkButton(buttonFrame, text='Add Employee', font=('arial', 14, 'bold'), width=130, corner_radius=15, command=add_employee)
addButton.grid(row=0, column=1, pady=5, padx=4)

updateButton = CTkButton(buttonFrame, text='Update Employee', font=('arial', 14, 'bold'), width=140, corner_radius=15, command=update_employee)
updateButton.grid(row=0, column=2, pady=5, padx=4)

deleteButton = CTkButton(buttonFrame, text='Delete Employee', font=('arial', 14, 'bold'), width=140, corner_radius=15, command=delete_employee)
deleteButton.grid(row=0, column=3, pady=5, padx=4)

deleteallButton = CTkButton(buttonFrame, text='Delete All', font=('arial', 14, 'bold'), width=110, corner_radius=15, command=delete_all)
deleteallButton.grid(row=0, column=4, pady=5, padx=4)

exportButton = CTkButton(buttonFrame, text='Export to Excel', font=('arial', 14, 'bold'), width=130, corner_radius=15, command=export_to_excel)
exportButton.grid(row=0, column=5, pady=5, padx=4)

uploadButton = CTkButton(buttonFrame, text='Upload Image', font=('arial', 14, 'bold'), width=130, corner_radius=15, command=upload_image)
uploadButton.grid(row=0, column=6, pady=5, padx=4)

viewButton = CTkButton(buttonFrame, text='View Image', font=('arial', 14, 'bold'), width=120, corner_radius=15, command=view_image)
viewButton.grid(row=0, column=7, pady=5, padx=4)

treeview_data()
tree.bind('<ButtonRelease>', selection)
window.after(50, _resize_header)
window.mainloop()
