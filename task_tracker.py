import json
import sys
from datetime import datetime

TASKS_FILE = "tasks.json"


def load_tasks():
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


def add_task(description):
    if not description.strip():
        print("Error: task description cannot be empty.")
        return

    tasks = load_tasks()
    next_id = max([t["id"] for t in tasks], default=0) + 1

    task = {
        "id": next_id,
        "description": description.strip(),
        "completed": False,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    tasks.append(task)
    save_tasks(tasks)
    print(f"Added task {task['id']}: {task['description']}")


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        status = "✓" if task["completed"] else " "
        print(f"[{status}] {task['id']}. {task['description']}")


def complete_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            if task["completed"]:
                print("Task already completed.")
                return
            task["completed"] = True
            save_tasks(tasks)
            print(f"Completed task {task_id}.")
            return
    print("Task not found.")


def print_help():
    print(
        "CLI Task Tracker\n\n"
        "Usage:\n"
        "  python task_tracker.py add \"Task description\"\n"
        "  python task_tracker.py list\n"
        "  python task_tracker.py complete <task_id>\n"
    )


def main():
    if len(sys.argv) < 2:
        print_help()
        return

    command = sys.argv[1].lower()

    if command == "add":
        add_task(" ".join(sys.argv[2:]))
    elif command == "list":
        list_tasks()
    elif command == "complete":
        if len(sys.argv) < 3:
            print("Error: missing task ID.")
            return
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("Error: task ID must be an integer.")
            return
        complete_task(task_id)
    else:
        print_help()


if __name__ == "__main__":
    main()
