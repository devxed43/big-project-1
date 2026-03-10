from text_to_speech import save
from fpdf import FPDF
import csv


def read_todos():
    with open('todos.txt', 'r') as file:
        print(file.read())


def add_todo():
    add = input("enter item: ")
    with open('todos.txt', 'a') as file:
        file.writelines(f'{add}\n')


def newsletter_signup():
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    age = input("Age: ")
    city = input("City: ")
    email = input("Email: ")

    entry = f"{first_name}, {last_name}, {age}, {city}, {email}"

    with open("contacts.txt", "a") as file:
        file.writelines(f'{entry}\n')

    print("Thank You for signing up for the bands touring list!")


def add_todos():
    print("Note: type 'done' to exit and get your new list")
    while True:
        tsk = input("add item: ")
        if tsk == "done":
            return
        else:
            with open('todos.txt', 'a') as file:
                file.writelines(f'{tsk}\n')


def edit_todo():
    with open('todos.txt', 'r') as file:
        lines = file.readlines()
        if len(lines) == 0:
            print('nothing to edit! list is empty!')
            return False
        print("".join(lines))
        old = input("enter item to edit: ")
        new = input("enter new value: ")
        updated = []
        for line in lines:
            updated.append(line.replace(old, new))
        with open("todos.txt", 'w') as file:
            file.writelines(updated)
        return True


def edit_todos():
    with open('todos.txt', 'r') as file:
        lines = file.readlines()
        print("".join(lines))
        old = input("enter word to replace: ")
        new = input("enter new word: ")
        updated = []

        for line in lines:
            updated.append(line.replace(old, new))

        with open('todos.txt', 'w') as file:
            file.writelines(updated)


def delete_todo():
    with open("todos.txt", "r") as file:
        lines = file.readlines()
        if len(lines) == 0:
            print('nothing to delete! list is empty!')
            return False
        print("".join(lines))
        delete = input("select value to delete: ")
        updated = []
        for line in lines:
            if line.strip() != delete:
                updated.append(line)
        with open('todos.txt', 'w+') as file:
            file.writelines(updated)
        return True


def delete_todos():
    with open("todos.txt", "w") as file:
        file.write("")
    print("items deleted")


def speechify():
    with open("todos.txt", "r") as file:
        todo_content = file.read().strip()

        if not todo_content:
            print("empty list")
            return

        print("Generating audio for your todos...beep boop...beep boop...")
        language = "en"
        output_file = "todos.mp3"

        save(todo_content, language, file=output_file)
        print(f'VOICE ANALYSIS COMPLETE! {output_file}')


def pdfify():
    with open("todos.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    print("Generating PDF...⏱️...✅")

    pdf = FPDF()

    pdf.add_page()
    pdf.set_margin(10)
    pdf.set_font("helvetica", "B", size=16)
    pdf.cell(0, 10, text="Your Tasks for Today",
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font("helvetica", size=12)

    for index, line in enumerate(lines, 1):
        content = f"{index}. {line.strip()}"
        pdf.multi_cell(w=0, h=10, text=content, align="L",
                       new_x="LMARGIN", new_y="NEXT")

    output_file = "tasks.pdf"

    pdf.output(output_file)
    print(f"PDF SUCCESSFULLY CREATED! Check {output_file}")


def csvify():
    with open("contacts.txt", "r") as txt_file, open("contacts.csv", "w", newline="") as csv_file:
        writer = csv.writer(csv_file)

        # This creates a header
        writer.writerow(['First Name', 'Last Name', 'Age', 'City', 'Email'])

        # loop thru each line
        for line in txt_file:
            task = line.strip()
            if task:
                # splits into separate columns
                writer.writerow(task.split(','))

    print("CSV conversion complete!")


def main():
    print("**************************** SELECT MODE: **********************************")
    print("**** read -- add -- add multiple -- speech -- pdf -- csv -- email signup -- edit -- replace -- delete -- delete all ****")

    while True:
        mode = input("mode: ").strip().lower()
        print("")
        match mode:
            case "read":
                read_todos()
                break
            case "add":
                add_todo()
                break
            case "add multiple":
                add_todos()
                break
            case "edit":
                edit_todo()
                break
            case "replace":
                edit_todos()
                break
            case "delete":
                delete_todo()
                break
            case "delete all":
                delete_todos()
                break
            case "speech":
                speechify()
                break
            case "pdf":
                pdfify()
                break
            case "csv":
                csvify()
                break
            case "email signup":
                newsletter_signup()
                break
            case _:
                print("please select a mode")


if __name__ == "__main__":
    main()
