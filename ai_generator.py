import os
from openai import OpenAI
from dotenv import load_dotenv

# Явная загрузка config.env из родительской директории
env_path = os.path.join(os.path.dirname(__file__), "..", "config.env")
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY не найден. Проверь файл config.env и путь к нему.")

client = OpenAI(api_key=api_key)

def generate_tasks(topic: str):
    prompt = f"Сгенерируй 5 практических задач по теме '{topic}' для изучения."
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    tasks = response.choices[0].message.content.split("\n")
    return [t.strip("-•1234567890. ").strip() for t in tasks if t.strip()]


def analyze_progress(completed_tasks):
    if not completed_tasks:
        return ["Отметьте хотя бы одну задачу, чтобы получить рекомендации."]

    prompt = (
        "Вот список задач, которые пользователь выполнил:\n\n" +
        "\n".join(f"- {task}" for task in completed_tasks) +
        "\n\nНа основе этого предложи 3 следующих шага или задания, которые помогут углубить знания пользователя."
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    recommendations = response.choices[0].message.content.split("\n")
    return [r.strip("-•1234567890. ").strip() for r in recommendations if r.strip()]
