# export.py
import json

def export_tasks_to_txt(tasks: list, topic: str, file_path: str = None) -> str:
    if not file_path:
        file_path = f"{topic}_tasks.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        for task in tasks:
            f.write(f"- {task}\n")
    return file_path

def export_tasks_to_json(tasks: list, topic: str, file_path: str = None) -> str:
    if not file_path:
        file_path = f"{topic}_tasks.json"
    data = {
        "topic": topic,
        "tasks": tasks
    }
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return file_path
