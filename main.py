import sys

from task_manager import TaskManager


def main():
    task_manager = TaskManager()
    args = split_args(sys.argv)

    options = {
        "help": get_help,
        "add": add,
        "delete": delete,
        "show": show,
        "update-status": update_status,
        "update-desctiption": update_description
    }

    for key, value in args.items():
        if key not in options:
            options["help"]()
            return
        if key == "help":
            options[key]()
            return
        options[key](task_manager, value)
    

def split_args(args: list) -> dict:
    params, values = [], []
    for arg in args[1:]:
        if arg[:2] != "--" and len(params) == 0:
            continue
        if arg[:2] == "--":
            params.append(arg[2:])
            values.append([])
        else:
            values[-1].append(arg)
    return dict(zip(params, values))

def add(tm: TaskManager, descriptions: list):
    description = " ".join(descriptions)
    tm.add(description)

def delete(tm: TaskManager, ids: list):
    for id in ids:
        try:
            id = int(id)
        except ValueError:
            print("task ids must be numerical")
            return
        tm.delete(id)

def show(tm: TaskManager, what:list):
    if len(what) > 1:
        print("You should specify only one show method")
        return
    if len(what) == 0:
        tm.list_task("all")
        return
    if what[0] not in ["all", "todo", "done", "in-progress"]:
        print("Task should be one of the following all, todo, done, in-progress")
        return
    tm.list_task(what[0])

def update_status(tm: TaskManager, data:list):
    if len(data) != 2:
        print("You need to enter task id and a new status")
        return
    id, status = tuple(data)
    try:
        id = int(id)
    except ValueError:
        print("Id must be numerical")
        return
    if status not in ["todo", "done", "in-progress"]:
        print("status should be todo, done or in-progress")
        return
    tm.change_status(id, status)
        
def update_description(tm: TaskManager, data: list):
    id, description = data[0], data[1:]
    try:
        id = int(id)
    except ValueError:
        print("id must be a number")
        return
    description = ' '.join(description)
    tm.update_description(id, description)

def get_help():
    help = "\n--help — show this menu\n"+\
    "--add {description} — add task\n"+\
    "--delete {id} — remove task\n"+\
    "--update-description {id} {new description}\n"+\
    "--update-status {id} {new status}, status can be todo, done in-progress\n"+\
    "--show {what} — show tasks, can be all, todo, done, in-progress, all by default"
    print(help)
            
if __name__ == "__main__":
    main()