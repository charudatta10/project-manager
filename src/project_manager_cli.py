import argparse
from project_manager import ProjectManager


def main():
    parser = argparse.ArgumentParser(description="Project Management CLI")
    parser.add_argument(
        "action",
        choices=[
            "init",
            "add-task",
            "edit-task",
            "view-tasks",
            "delete-task",
            "log-time",
            "categorize-task",
            "add-tag",
            "add-repeating-task",
            "query-tasks",
        ],
        help="Action to perform",
    )
    parser.add_argument("--project", required=True, help="Project name")
    parser.add_argument("--task", help="Task name")
    parser.add_argument("--due-date", help="Due date (YYYY-MM-DD)")
    parser.add_argument("--tags", nargs="+", help="Tags for the task")
    parser.add_argument(
        "--status", choices=["TODO", "DOING", "DONE"], help="Task status"
    )
    parser.add_argument("--hours", type=float, help="Hours to log")
    parser.add_argument(
        "--interval", type=int, help="Interval in days for repeating tasks"
    )
    parser.add_argument("--message", help="Additional message")
    parser.add_argument("--overdue", action="store_true", help="Query overdue tasks")

    args = parser.parse_args()

    manager = ProjectManager()

    if args.action == "init":
        manager.initialize_project(args.project)
    elif args.action == "add-task":
        manager.add_task(args.project, args.task, args.due_date, args.tags)
    elif args.action == "edit-task":
        updates = {}
        if args.status:
            updates["status"] = args.status
        if args.due_date:
            updates["due_date"] = args.due_date
        if args.tags:
            updates["tags"] = args.tags
        manager.edit_task(args.project, args.task, **updates)
    elif args.action == "view-tasks":
        tasks = manager.view_tasks(args.project, args.status)
        for task in tasks:
            print(task)
    elif args.action == "delete-task":
        manager.delete_task(args.project, args.task)
    elif args.action == "log-time":
        manager.log_time(args.project, args.task, args.hours, args.tags)
    elif args.action == "categorize-task":
        manager.categorize_task(args.project, args.task, args.status)
    elif args.action == "add-tag":
        manager.add_tag_to_task(args.project, args.task, args.message)
    elif args.action == "add-repeating-task":
        manager.add_repeating_task(
            args.project, args.task, args.interval, args.due_date, args.tags
        )
    elif args.action == "query-tasks":
        tasks = manager.query_tasks(
            args.project, args.status, args.due_date, args.overdue
        )
        for task in tasks:
            print(task)


if __name__ == "__main__":
    main()
