# ====================================== Imports for front end and backend =============================================
import tkinter
import random
import pyperclip
import sqlite3
from PIL import ImageTk, Image
from tkinter import messagebox

# ======================================================================================================================

# ================================= Root Window: Pass-Stash Password Manager & Vault ===================================

pass_stash_window = tkinter.Tk()
pass_stash_window.title("Pass-Stash: Manager and Vault")
pass_stash_window.geometry("800x600")
pass_stash_window.configure(bg="#708090")
pass_stash_window.resizable(False, False)
pass_stash_window.eval('tk::PlaceWindow . center')
pass_stash_icon = tkinter.Image("photo", file="pass_stash_icon.png")
pass_stash_window.iconphoto(True, pass_stash_icon)
pass_stash_window.wm_iconphoto(True, pass_stash_icon)


# ======================================================================================================================

# ========================================== All Pass-Stash Operation Frames ===========================================

pass_stash_welcome_frame = tkinter.Frame(pass_stash_window, bg="#708090")
home_options_frame = tkinter.Frame(pass_stash_window, bg="#708090")
add_entry_frame = tkinter.Frame(pass_stash_window, bg="#708090")
update_entry_frame = tkinter.Frame(pass_stash_window, bg="#708090")
delete_entry_frame = tkinter.Frame(pass_stash_window, bg="#708090")
search_entry_frame = tkinter.Frame(pass_stash_window, bg="#708090")
generate_password_frame = tkinter.Frame(pass_stash_window, bg="#708090")


# ======================================================================================================================

# ======================================== Functions for switching Frames ==============================================


def change_frame_intro():
    home_options_frame.pack_forget()
    pass_stash_label.grid(row=0, column=0, sticky="news", pady=50)
    pass_stash_slogan.grid(row=1, column=0)
    enter_button.grid(row=3, column=0, pady=10)
    pass_stash_welcome_frame.pack()
    logo_label.pack(pady=24)


def change_frame_home():
    logo_label.pack_forget()
    pass_stash_welcome_frame.pack_forget()
    add_entry_frame.pack_forget()
    account_entry.delete(first=0, last=100)
    username_entry.delete(first=0, last=100)
    password_entry.delete(first=0, last=100)
    update_entry_frame.pack_forget()
    update_username_verify_entry.delete(first=0, last=100)
    update_account_verify_entry.delete(first=0, last=100)
    verify_selected_entry.delete(first=0, last=100)
    update_account_entry.delete(first=0, last=100)
    update_username_entry.delete(first=0, last=100)
    update_password_entry.delete(first=0, last=100)
    delete_entry_frame.pack_forget()
    delete_account_entry.delete(first=0, last=100)
    delete_username_entry.delete(first=0, last=100)
    delete_selected_entry.delete(first=0, last=100)
    search_entry_frame.pack_forget()
    search_result_text.delete("1.0", "end")
    search_entry.delete(first=0, last=100)
    generate_password_frame.pack_forget()
    new_password_entry.delete(first=0, last=100)
    home_options_frame.pack(fill='both', expand=1)


def change_frame_add():
    home_options_frame.pack_forget()
    add_entry_frame.pack(fill='both', expand=1)


def change_frame_update():
    home_options_frame.pack_forget()
    update_entry_frame.pack(fill='both', expand=1)


def change_frame_delete():
    home_options_frame.pack_forget()
    delete_entry_frame.pack(fill='both', expand=1)


def change_frame_search():
    home_options_frame.pack_forget()
    search_entry_frame.pack(fill='both', expand=1)


def change_frame_generate():
    home_options_frame.pack_forget()
    generate_password_frame.pack(fill='both', expand=1)


# ======================================================================================================================

# ======================================== Functions for all Operations ================================================

def add_new_credential():
    conn = sqlite3.connect("pass_stash_vault.db")
    c = conn.cursor()

    c.execute("INSERT INTO user_credentials VALUES (:nickname, :username, :password)",
              {
                  'nickname': account_entry.get(),
                  'username': username_entry.get(),
                  'password': password_entry.get()
              })

    conn.commit()
    conn.close()
    account_entry.delete(first=0, last=100)
    username_entry.delete(first=0, last=100)
    password_entry.delete(first=0, last=100)
    messagebox.showinfo("Add Credential", "Credential Added!")
    change_frame_home()


def verify_update_credential():
    conn = sqlite3.connect("pass_stash_vault.db")
    c = conn.cursor()

    verify_update_nickname = update_account_verify_entry.get()
    verify_update_username = update_username_verify_entry.get()

    verify_credential_update = c.execute("SELECT * FROM user_credentials WHERE nickname=? AND username=?",
                                         (verify_update_nickname, verify_update_username))
    verified_update = verify_credential_update.fetchone()

    verify_selected_entry.insert(tkinter.END, verified_update)

    conn.commit()
    conn.close()


def update_credential():
    conn = sqlite3.connect("pass_stash_vault.db")
    c = conn.cursor()

    c.execute("""UPDATE user_credentials
        SET
            nickname = :updated_nickname,
            username = :updated_username,
            password = :updated_password
        WHERE
            nickname= :old_nickname AND username = :old_username""",
              {
                  'updated_nickname': update_account_entry.get(),
                  'updated_username': update_username_entry.get(),
                  'updated_password': update_password_entry.get(),
                  'old_nickname': update_account_verify_entry.get(),
                  'old_username': update_username_verify_entry.get()
              })

    conn.commit()
    conn.close()
    update_username_verify_entry.delete(first=0, last=100)
    update_account_verify_entry.delete(first=0, last=100)
    verify_selected_entry.delete(first=0, last=100)
    update_account_entry.delete(first=0, last=100)
    update_username_entry.delete(first=0, last=100)
    update_password_entry.delete(first=0, last=100)
    messagebox.showinfo("Update Credential", "Credential Updated!")
    change_frame_home()


def verify_delete_credential():
    conn = sqlite3.connect("pass_stash_vault.db")
    c = conn.cursor()

    verify_delete_nickname = delete_account_entry.get()
    verify_delete_username = delete_username_entry.get()

    verify_credential = c.execute(
        "SELECT * FROM user_credentials WHERE nickname=? AND username=?",
        (verify_delete_nickname, verify_delete_username))
    verified_credential = verify_credential.fetchone()

    delete_selected_entry.insert(tkinter.END, verified_credential)

    conn.commit()
    conn.close()


def delete_credential():
    conn = sqlite3.connect("pass_stash_vault.db")
    c = conn.cursor()

    delete_nickname = delete_account_entry.get()
    delete_username = delete_username_entry.get()

    c.execute("DELETE FROM user_credentials WHERE nickname=? AND username=?", (delete_nickname, delete_username))

    delete_account_entry.delete(first=0, last=100)
    delete_username_entry.delete(first=0, last=100)
    delete_selected_entry.delete(first=0, last=100)
    conn.commit()
    conn.close()
    messagebox.showinfo("Delete Credential", "Credential Deleted!")
    change_frame_home()


def search_credential():
    conn = sqlite3.connect("pass_stash_vault.db")
    c = conn.cursor()

    search_result_text.delete("1.0", "end")

    search_nickname = search_entry.get()

    search_for_credential = c.execute("SELECT * FROM user_credentials WHERE nickname=?", (search_nickname,))
    found_credentials = search_for_credential.fetchall()

    for item in found_credentials:
        search_result_text.insert(tkinter.END, item)
        search_result_text.insert(tkinter.END, "\n")

    conn.commit()
    conn.close()


def search_all_credentials():
    conn = sqlite3.connect("pass_stash_vault.db")
    c = conn.cursor()

    search_result_text.delete("1.0", "end")

    credentials = c.execute("SELECT * FROM user_credentials")

    all_credentials = credentials.fetchall()

    for item in all_credentials:
        search_result_text.insert(tkinter.END, item)
        search_result_text.insert(tkinter.END, "\n")

    conn.commit()
    conn.close()


new_password = tkinter.StringVar()


def generate_new_password():
    generate_password = ""
    all_characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                      't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                      'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5',
                      '6', '7', '8', '9', '0', '`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_',
                      '+', '=', '[', '{', ']', '}', ':', ';', '<', ',', '>', '.', '?', '/']
    for x in range(1, 13):
        generate_password = generate_password + random.choice(all_characters)
    new_password.set(generate_password)


def copy_new_password():
    new_generated_password = new_password.get()
    pyperclip.copy(new_generated_password)
    messagebox.showinfo("Copy Password", "Password Copied!")


# ======================================================================================================================

# =========================================== Pass-Stash Intro Screen Frame ============================================

# Creating Pass-Stash Intro Related Widgets and Fields
pass_stash_label = tkinter.Label(
    pass_stash_welcome_frame, text="Pass-Stash: Manager & Vault",
    bg="#708090", fg="#FFFFFF", font=("Quicksand", 50, "bold"))

pass_stash_slogan = tkinter.Label(
    pass_stash_welcome_frame, text="Password Peace of Mind All in One Place",
    bg="#708090", fg="#FFFFFF", font=("Times New Roman", 24, "italic"))

enter_button = tkinter.Button(
    pass_stash_welcome_frame, text="Enter The Vault",
    bg="#FFFFFF", fg="#181818", font=("Quicksand", 30), command=change_frame_home)

pass_stash_logo = Image.open("pass_stash_logo.png")
resize_logo = pass_stash_logo.resize((250, 250))
new_pass_stash_logo = ImageTk.PhotoImage(resize_logo)
logo_label = tkinter.Label(image=new_pass_stash_logo, bg="#708090")

# Placing Pass-Stash Intro Related Widgets and Fields
pass_stash_label.grid(row=0, column=0, sticky="news", pady=50)
pass_stash_slogan.grid(row=1, column=0)
enter_button.grid(row=3, column=0, pady=35)
pass_stash_welcome_frame.pack()
logo_label.pack()

# ======================================================================================================================

# =========================================== Home Screen Options Frame ================================================

# Creating Home Screen Options Related Widgets and Fields
options_label = tkinter.Label(
    home_options_frame, text="Select An Option",
    bg="#708090", fg="#FFFFFF", font=("Quicksand", 60, "bold"), pady=50)

create_label = tkinter.Label(
    home_options_frame, text="Create Entry", bg="#708090", fg="#FFFFFF", font=("Quicksand", 24), pady=5)

update_label = tkinter.Label(
    home_options_frame, text="Update Entry", bg="#708090", fg="#FFFFFF", font=("Quicksand", 24), pady=5)

delete_label = tkinter.Label(
    home_options_frame, text="Delete Entry", bg="#708090", fg="#FFFFFF", font=("Quicksand", 24), pady=5)

search_label = tkinter.Label(
    home_options_frame, text="Search Entry", bg="#708090", fg="#FFFFFF", font=("Quicksand", 24), pady=5)

generate_label = tkinter.Label(
    home_options_frame, text="Generate Password", bg="#708090", fg="#FFFFFF", font=("Quicksand", 24), pady=5)

lock_label = tkinter.Label(
    home_options_frame, text="Quit Pass-Stash", bg="#708090", fg="#FFFFFF", font=("Quicksand", 18), pady=5)

create_button = tkinter.Button(
    home_options_frame, text="CREATE", bg="#FFFFFF", fg="#181818", font=("Quicksand", 30), command=change_frame_add)

update_button = tkinter.Button(
    home_options_frame, text="UPDATE", bg="#FFFFFF", fg="#181818", font=("Quicksand", 30), command=change_frame_update)

delete_button = tkinter.Button(
    home_options_frame, text="DELETE", bg="#FFFFFF", fg="#181818", font=("Quicksand", 30), command=change_frame_delete)

search_button = tkinter.Button(
    home_options_frame, text="SEARCH", bg="#FFFFFF", fg="#181818", font=("Quicksand", 30), command=change_frame_search)

generate_button = tkinter.Button(
    home_options_frame, text="GENERATE",
    bg="#FFFFFF", fg="#181818", font=("Quicksand", 30), command=change_frame_generate)

lock_button = tkinter.Button(
    home_options_frame, text="QUIT",
    bg="#FFFFFF", fg="#181818", font=("Quicksand", 24), command=pass_stash_window.destroy)

# Placing Home Screen Options Related Widgets and Fields
options_label.place(relx=0.5, rely=0.05, anchor="n")
create_label.place(relx=0.125, rely=0.425, anchor="center")
create_button.place(relx=0.125, rely=0.5, anchor="center")
update_button.place(relx=0.375, rely=0.5, anchor="center")
update_label.place(relx=0.375, rely=0.425, anchor="center")
delete_button.place(relx=0.625, rely=0.5, anchor="center")
delete_label.place(relx=0.625, rely=0.425, anchor="center")
search_button.place(relx=0.875, rely=0.5, anchor="center")
search_label.place(relx=0.875, rely=0.425, anchor="center")
generate_button.place(relx=0.5, rely=0.7, anchor="center")
generate_label.place(relx=0.5, rely=0.625, anchor="center")
lock_label.place(relx=0.5, rely=0.865, anchor="center")
lock_button.place(relx=0.5, rely=0.925, anchor="center", width=130)

# ======================================================================================================================

# ============================================== Add New Entry Frame ===================================================

# Creating Add Credential Entry Related Widgets and Fields
add_label = tkinter.Label(
    add_entry_frame, text="Enter Account Information",
    bg="#708090", fg="#FFFFFF", font=("Quicksand", 50, "bold"), pady=50)

account_label = tkinter.Label(
    add_entry_frame, text="Nickname", bg="#708090", fg="#FFFFFF", font=("Quicksand", 36), pady=5)

username_label = tkinter.Label(
    add_entry_frame, text="Username", bg="#708090", fg="#FFFFFF", font=("Quicksand", 36), pady=5)

password_label = tkinter.Label(
    add_entry_frame, text="Password", bg="#708090", fg="#FFFFFF", font=("Quicksand", 36), pady=5)

account_entry = tkinter.Entry(add_entry_frame, bg="#181818", fg="#FFFFFF", font=("Quicksand", 16), justify="center")
username_entry = tkinter.Entry(add_entry_frame, bg="#181818", fg="#FFFFFF", font=("Quicksand", 16), justify="center")
password_entry = tkinter.Entry(add_entry_frame, bg="#181818", fg="#FFFFFF", font=("Quicksand", 16), justify="center")

add_save_button = tkinter.Button(
    add_entry_frame, text="Save Entry", bg="#FFFFFF", fg="#181818", font=("Quicksand", 30), command=add_new_credential)

add_cancel_button = tkinter.Button(
    add_entry_frame, text="Cancel Entry", bg="#FFFFFF", fg="#181818", font=("Quicksand", 30), command=change_frame_home)

# Placing Add Credential Entry Related Widgets and Fields
add_label.place(relx=0.5, rely=0.05, anchor="n")
account_label.place(relx=0.2, rely=0.475, anchor="s")
account_entry.place(relx=0.2, rely=0.55, anchor="s")
username_label.place(relx=0.5, rely=0.475, anchor="s")
username_entry.place(relx=0.5, rely=0.55, anchor="s")
password_label.place(relx=0.8, rely=0.475, anchor="s")
password_entry.place(relx=0.8, rely=0.55, anchor="s")
add_save_button.place(relx=0.5, rely=0.75, anchor="s")
add_cancel_button.place(relx=0.5, rely=0.9, anchor="s")

# ======================================================================================================================

# =========================================== Update Existing Entry Frame ==============================================

# Creating Add Credential Entry Related Widgets and Fields
update_header_label = tkinter.Label(
    update_entry_frame, text="Enter Account Information",
    bg="#708090", fg="#FFFFFF", font=("Quicksand", 50, "bold"), pady=50)

update_account_verify_entry = tkinter.Entry(update_entry_frame,
                                            bg="#181818", fg="#FFFFFF", font=("Quicksand", 16), justify="center")
update_username_verify_entry = tkinter.Entry(update_entry_frame,
                                             bg="#181818", fg="#FFFFFF", font=("Quicksand", 16), justify="center")
update_password_verify_entry = tkinter.Entry(update_entry_frame,
                                             bg="#181818", fg="#FFFFFF", font=("Quicksand", 16), justify="center")

verify_selected_button = tkinter.Button(update_entry_frame, text="Verify Account",
                                        bg="#FFFFFF", fg="#181818", font=("Quicksand", 30),
                                        command=verify_update_credential)

update_account_verify_label = tkinter.Label(
    update_entry_frame, text="Nickname", bg="#708090", fg="#FFFFFF", font=("Quicksand", 36), pady=5)

update_username_verify_label = tkinter.Label(
    update_entry_frame, text="Username", bg="#708090", fg="#FFFFFF", font=("Quicksand", 36), pady=5)

update_password_verify_label = tkinter.Label(
    update_entry_frame, text="Password", bg="#708090", fg="#FFFFFF", font=("Quicksand", 36), pady=5)

verify_selected_label = tkinter.Label(
    update_entry_frame, text="Selected Account", bg="#708090", fg="#FFFFFF", font=("Quicksand", 30), pady=5)

verify_selected_entry = tkinter.Entry(update_entry_frame,
                                      bg="#181818", fg="#FFFFFF", font=("Quicksand", 24), width=43, justify="center")

update_account_label = tkinter.Label(
    update_entry_frame, text="Nickname", bg="#708090", fg="#FFFFFF", font=("Quicksand", 36), pady=5)

update_username_label = tkinter.Label(
    update_entry_frame, text="Username", bg="#708090", fg="#FFFFFF", font=("Quicksand", 36), pady=5)

update_password_label = tkinter.Label(
    update_entry_frame, text="Password", bg="#708090", fg="#FFFFFF", font=("Quicksand", 36), pady=5)

update_account_entry = tkinter.Entry(update_entry_frame,
                                     bg="#181818", fg="#FFFFFF", font=("Quicksand", 16), justify="center")
update_username_entry = tkinter.Entry(update_entry_frame,
                                      bg="#181818", fg="#FFFFFF", font=("Quicksand", 16), justify="center")
update_password_entry = tkinter.Entry(update_entry_frame,
                                      bg="#181818", fg="#FFFFFF", font=("Quicksand", 16), justify="center")

update_save_button = tkinter.Button(
    update_entry_frame, text="Update Entry",
    bg="#FFFFFF", fg="#181818", font=("Quicksand", 30), command=update_credential)

update_cancel_button = tkinter.Button(
    update_entry_frame, text="Cancel Update",
    bg="#FFFFFF", fg="#181818", font=("Quicksand", 30), command=change_frame_home)

# Placing Add Credential Entry Related Widgets and Fields
update_header_label.place(relx=0.5, rely=0.05, anchor="n")
update_account_verify_label.place(relx=0.2, rely=0.25, anchor="n")
update_account_verify_entry.place(relx=0.2, rely=0.35, anchor="n")
update_username_verify_label.place(relx=0.8, rely=0.25, anchor="n")
update_username_verify_entry.place(relx=0.8, rely=0.35, anchor="n")
verify_selected_button.place(relx=0.5, rely=0.325, anchor="n")
verify_selected_label.place(relx=0.5, rely=0.4125, anchor="n")
verify_selected_entry.place(relx=0.5, rely=0.5, anchor="n")
update_account_label.place(relx=0.2, rely=0.675, anchor="s")
update_account_entry.place(relx=0.2, rely=0.725, anchor="s")
update_username_label.place(relx=0.5, rely=0.675, anchor="s")
update_username_entry.place(relx=0.5, rely=0.725, anchor="s")
update_password_label.place(relx=0.8, rely=0.675, anchor="s")
update_password_entry.place(relx=0.8, rely=0.725, anchor="s")
update_save_button.place(relx=0.5, rely=0.825, anchor="s")
update_cancel_button.place(relx=0.5, rely=0.975, anchor="s")

# ======================================================================================================================

# ======================================================================================================================

# =========================================== Delete Existing Entry Frame ==============================================

# Creating Delete Credential Entry Related Widgets and Fields
delete_header_label = tkinter.Label(
    delete_entry_frame, text="Enter Account Information",
    bg="#708090", fg="#FFFFFF", font=("Quicksand", 50, "bold"), pady=50)

delete_account_label = tkinter.Label(
    delete_entry_frame, text="Nickname", bg="#708090", fg="#FFFFFF", font=("Quicksand", 30), pady=5)

delete_account_entry = tkinter.Entry(delete_entry_frame,
                                     bg="#181818", fg="#FFFFFF", font=("Quicksand", 24), width=19, justify="center")

delete_username_label = tkinter.Label(
    delete_entry_frame, text="Username", bg="#708090", fg="#FFFFFF", font=("Quicksand", 30), pady=5)

delete_username_entry = tkinter.Entry(delete_entry_frame,
                                      bg="#181818", fg="#FFFFFF", font=("Quicksand", 24), width=19, justify="center")

delete_verify_button = tkinter.Button(
    delete_entry_frame, text="Verify Account", bg="#FFFFFF", fg="#181818", font=("Quicksand", 24),
    command=verify_delete_credential)

delete_selected_label = tkinter.Label(
    delete_entry_frame, text="Selected Account", bg="#708090", fg="#FFFFFF", font=("Quicksand", 30), pady=5)

delete_selected_entry = tkinter.Entry(delete_entry_frame,
                                      bg="#181818", fg="#FFFFFF", font=("Quicksand", 24), width=43, justify="center")

delete_entry_button = tkinter.Button(
    delete_entry_frame, text="Delete Account",
    bg="#FFFFFF", fg="#181818", font=("Quicksand", 30), command=delete_credential)

delete_cancel_button = tkinter.Button(
    delete_entry_frame, text="Cancel Delete",
    bg="#FFFFFF", fg="#181818", font=("Quicksand", 30), command=change_frame_home)

# Placing Delete Credential Entry Related Widgets and Fields
delete_header_label.place(relx=0.5, rely=0.05, anchor="n")
delete_account_label.place(relx=0.275, rely=0.36, anchor="s")
delete_account_entry.place(relx=0.275, rely=0.42, anchor="s")
delete_username_label.place(relx=0.725, rely=0.36, anchor="s")
delete_username_entry.place(relx=0.725, rely=0.42, anchor="s")
delete_verify_button.place(relx=0.5, rely=0.5, anchor="s")
delete_selected_label.place(relx=0.5, rely=0.6425, anchor="s")
delete_selected_entry.place(relx=0.5, rely=0.7, anchor="s")
delete_entry_button.place(relx=0.5, rely=0.8, anchor="s")
delete_cancel_button.place(relx=0.5, rely=0.95, anchor="s")

# ======================================================================================================================

# ======================================================================================================================

# =========================================== Search Existing Entry Frame ==============================================

# Creating Search Credential Related Widgets and Fields
search_header_label = tkinter.Label(
    search_entry_frame, text="Enter Account Information",
    bg="#708090", fg="#FFFFFF", font=("Quicksand", 50, "bold"), pady=50)

search_entry_label = tkinter.Label(
    search_entry_frame, text="Account Nickname", bg="#708090", fg="#FFFFFF", font=("Quicksand", 30), pady=5)

search_entry = tkinter.Entry(search_entry_frame, bg="#181818", fg="#FFFFFF", font=("Quicksand", 30), justify="center")

search_entry_button = tkinter.Button(
    search_entry_frame, text="Search Account",
    bg="#FFFFFF", fg="#181818", font=("Quicksand", 18), command=search_credential)

search_entry_all_button = tkinter.Button(
    search_entry_frame, text="Show Accounts",
    bg="#FFFFFF", fg="#181818", font=("Quicksand", 18), command=search_all_credentials)

search_result_text = tkinter.Text(
    search_entry_frame, height=10, width=65, bg="#181818", fg="#FFFFFF", font=("Quicksand", 18))

search_cancel_button = tkinter.Button(
    search_entry_frame, text="Close Search",
    bg="#FFFFFF", fg="#181818", font=("Quicksand", 18), command=change_frame_home)

# Placing Search Credential Related Widgets and Fields
search_header_label.place(relx=0.5, rely=0.05, anchor="n")
search_entry_label.place(relx=0.5, rely=0.35, anchor="s")
search_entry.place(relx=0.5, rely=0.43, anchor="s")
search_entry_button.place(relx=0.359, rely=0.5, anchor="s")
search_entry_all_button.place(relx=0.645, rely=0.5, anchor="s")
search_result_text.place(relx=0.5, rely=0.89, anchor="s")
search_cancel_button.place(relx=0.5, rely=0.975, anchor="s")

# ======================================================================================================================

# ======================================================================================================================

# =========================================== Generate New Password Frame ==============================================

# Creating Generate Password Related Widgets and Fields
generate_password_label = tkinter.Label(
    generate_password_frame, text="Generate New Password",
    bg="#708090", fg="#FFFFFF", font=("Quicksand", 50, "bold"), pady=50)

new_password_label = tkinter.Label(
    generate_password_frame, text="New Password", bg="#708090", fg="#FFFFFF", font=("Quicksand", 36), pady=5)

new_password_entry = tkinter.Entry(generate_password_frame, bg="#181818", fg="#FFFFFF",
                                   font=("Quicksand", 36), textvariable=new_password, justify="center")

generate_new_password_button = tkinter.Button(
    generate_password_frame, text="Generate Password",
    bg="#FFFFFF", fg="#181818", font=("Quicksand", 22), command=generate_new_password)

copy_new_password_button = tkinter.Button(
    generate_password_frame, text="Copy New Password",
    bg="#FFFFFF", fg="#181818", font=("Quicksand", 22), command=copy_new_password)

generate_password_cancel_button = tkinter.Button(
    generate_password_frame, text="Close Password Generator",
    bg="#FFFFFF", fg="#181818", font=("Quicksand", 30), command=change_frame_home)

# Placing Generate Password Related Widgets and Fields
generate_password_label.place(relx=0.5, rely=0.05, anchor="n")
new_password_label.place(relx=0.5, rely=0.4, anchor="s")
new_password_entry.place(relx=0.5, rely=0.5, anchor="s")
generate_new_password_button.place(relx=0.345, rely=0.625, anchor="s")
copy_new_password_button.place(relx=0.65, rely=0.625, anchor="s")
generate_password_cancel_button.place(relx=0.5, rely=0.9, anchor="s")

# ======================================================================================================================

pass_stash_window.mainloop()
