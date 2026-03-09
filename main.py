
# 2.) do stuff with the data the main has given
def read_todos():
    with open('todos.txt', 'r') as file:
        print(file.read())


def add_todo():
    add = input("enter item: ")
    with open('todos.txt', 'a') as file:
        file.writelines(f'{add}\n')


def edit_todo():
    with open('todos.txt', 'r') as file:
        lines = file.readlines()
        print("".join(lines))
        old = input("enter item to edit: ")
        new = input("enter new value: ")
        updated = []
        for line in lines:
            updated.append(line.replace(old, new))
        with open("todos.txt", 'w') as file:
            file.writelines(updated)


def delete_todo():
    with open("todos.txt", "r") as file:
        lines = file.readlines()
        print("".join(lines))
        delete = input("select value to delete: ")
        updated = []
        for line in lines:
            if line.strip() != delete:
                updated.append(line)

# 1.) here is the data


def main():
    print("select a mode")
    mode = input("read | add | edit | delete")
    match mode:
        case "read":
            read_todos()
        case "add":
            add_todo()
        case "edit":
            edit_todo()
        case "delete":
            delete_todo()
        case _:
            print("please select a mode")


if __name__ == "__main__":
    main()


# ==================== note ====================

# mode input tells mode which match to trigger based off the string case which triggers the function
# the helper fns at the top, perform the action
# and the main supplies the data
