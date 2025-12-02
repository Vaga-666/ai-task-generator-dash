from dotenv import load_dotenv
load_dotenv()

from dash import dcc, html, Output, Input, State, ctx
import dash_bootstrap_components as dbc
from ai_generator import generate_tasks, analyze_progress
from export import export_tasks_to_txt, export_tasks_to_json

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])
server = app.server

app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H2("🧠 AI-генератор задач по теме", className="text-center mb-4"))),
    
    dbc.Row(dbc.Col(
        dcc.Input(id="topic-input", type="text", placeholder="Введите тему, например: Python", className="form-control"), width=6
    ), justify="center", className="mb-3"),

    dbc.Row(dbc.Col(
        dbc.Button("🎯 Сгенерировать задачи", id="generate-btn", color="primary", className="w-100"), width=3
    ), justify="center", className="mb-4"),

    dbc.Row(dbc.Col(html.Div(id="task-list-container"), width=8), justify="center"),

    dbc.Row([
        dbc.Col(dbc.Button("📄 Экспорт в TXT", id="export-txt-btn", color="secondary", className="w-100"), width=2),
        dbc.Col(dbc.Button("🗂 Экспорт в JSON", id="export-json-btn", color="secondary", className="w-100"), width=2)
    ], justify="center", className="mt-4"),

    dbc.Row(dbc.Col(
        dbc.Button("📊 Проанализировать прогресс", id="analyze-btn", color="success", className="w-50"), width=4
    ), justify="center", className="mt-4"),

    dbc.Row([
        dbc.Col(html.Div(id="progress-output"), width=6),
        dbc.Col(html.Div(id="recommendations-output"), width=6)
    ], className="mt-4"),

    dbc.Row(
        dbc.Col(html.Div(id="history-output"), width=12),
        className="mt-4"
    ),

    dcc.Store(id="stored-tasks"),
    dcc.Store(id="analysis-history", data=[]),  # 💾 История анализа
    dcc.Download(id="download-file")
], fluid=True)


@app.callback(
    Output("stored-tasks", "data"),
    Output("task-list-container", "children"),
    Input("generate-btn", "n_clicks"),
    State("topic-input", "value")
)
def generate_and_display_tasks(n_clicks, topic):
    if not n_clicks or not topic:
        return dash.no_update, ""

    try:
        tasks = generate_tasks(topic)
        data = [{"task": t, "done": False} for t in tasks]

        checklist = dcc.Checklist(
            id="task-checklist",
            options=[{"label": t, "value": i} for i, t in enumerate(tasks)],
            value=[],
            labelStyle={"display": "block"}
        )

        return data, checklist
    except Exception as e:
        return dash.no_update, html.Div(f"Ошибка: {e}", className="text-danger")


@app.callback(
    Output("download-file", "data"),
    Input("export-txt-btn", "n_clicks"),
    Input("export-json-btn", "n_clicks"),
    State("stored-tasks", "data"),
    State("topic-input", "value"),
    prevent_initial_call=True
)
def export_data(n_txt, n_json, task_data, topic):
    if not task_data or not topic:
        return dash.no_update

    trigger_id = ctx.triggered_id
    tasks = [t["task"] for t in task_data]

    if trigger_id == "export-txt-btn":
        path = export_tasks_to_txt(tasks, topic)
        with open(path, encoding="utf-8") as f:
            content = f.read()
        os.remove(path)
        return dict(content=content, filename=f"{topic}_tasks.txt")

    elif trigger_id == "export-json-btn":
        path = export_tasks_to_json(tasks, topic)
        with open(path, encoding="utf-8") as f:
            content = f.read()
        os.remove(path)
        return dict(content=content, filename=f"{topic}_tasks.json")

    return dash.no_update


# 🔄 Анализ прогресса и сохранение в историю
@app.callback(
    Output("progress-output", "children"),
    Output("recommendations-output", "children"),
    Output("analysis-history", "data"),
    Input("analyze-btn", "n_clicks"),
    State("task-checklist", "value"),
    State("stored-tasks", "data"),
    State("analysis-history", "data")
)
def analyze_tasks(n_clicks, completed_ids, task_data, history):
    if not n_clicks or not task_data:
        return "", "", history

    completed_tasks = [task_data[i]["task"] for i in completed_ids]
    percent = int(len(completed_tasks) / len(task_data) * 100)

    try:
        recommendations = analyze_progress(completed_tasks)
        new_entry = {
            "done": completed_tasks,
            "percent": percent,
            "recommendations": recommendations
        }

        updated_history = history + [new_entry]

        return (
            html.Div([
                html.H5("✅ Прогресс выполнения:"),
                html.Div(f"Вы выполнили {percent}% задач.")
            ]),
            html.Div([
                html.H5("📌 Рекомендации:"),
                html.Ul([html.Li(r) for r in recommendations])
            ]),
            updated_history
        )
    except Exception as e:
        return "", html.Div(f"Ошибка анализа: {e}", className="text-danger"), history


# 🔄 Отображение истории анализов
@app.callback(
    Output("history-output", "children"),
    Input("analysis-history", "data")
)
def display_history(history):
    if not history:
        return ""

    history_blocks = []
    for i, entry in enumerate(history):
        block = html.Div([
            html.H5(f"🕒 Анализ #{i + 1} — {entry['percent']}%"),
            html.P("✔️ Выполненные задачи:"),
            html.Ul([html.Li(task) for task in entry["done"]]),
            html.P("🔁 AI-рекомендации:"),
            html.Ul([html.Li(r) for r in entry["recommendations"]]),
            html.Hr()
        ])
        history_blocks.append(block)

    return html.Div([
        html.H4("📚 История анализов", className="text-center mb-3"),
        html.Div(history_blocks)
    ])


if __name__ == '__main__':
    print("🚀 Запуск Dash-приложения на http://127.0.0.1:8050")
    app.run(debug=True)
