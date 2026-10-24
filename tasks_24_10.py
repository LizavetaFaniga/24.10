from celery import Celery, chain, chord
from celery.schedules import crontab
import time

app = Celery(
    'tasks_24_10', 
    broker='amqp://guest:guest@localhost:5672//', 
    backend='db+sqlite:///celery_results.sqlite3' 
)

@app.task
def prepare_daily_data(dummy_arg="start"):
    print("Начало сбора данных...")
    return "Начало сбора данных..."

app.conf.beat_schedule = {
    'run-every-2-minutes': {
        'task': 'tasks_24_10.prepare_daily_data',
        'schedule': crontab(minute='*/2'), 
        'args': ("scheduled",)
    },
}

@app.task
def fetch_data(dummy_arg):
    print("fetch_data: Сырые данные")
    return "Сырые данные"

@app.task
def process_data(raw_data):
    print(f"Обработка: {raw_data}")
    return "Обработанный отчет"

@app.task
def save_report(report):
    print(f"Сохранено: {report}")
    return True

@app.task
def run_pipeline(dummy_arg="start"):
    pipeline = chain(
        fetch_data.s(dummy_arg),
        process_data.s(),
        save_report.s()
    )
    return pipeline.delay()

@app.task
def notify_dean(department):
    print(f"Уведомление отправлено руководителю {department}")
    return f"OK: {department}"

@app.task
def final_summary(results):
    print(f"Финальный отчет. Результаты: {results}")
    return "Отчет готов"

@app.task
def run_full_distribution(dummy_arg="start"):
    departments = ['ИТ', 'Экономика', 'Юридический']
    header = [notify_dean.s(dept) for dept in departments]
    return chord(header)(final_summary.s())

@app.task
def urgent_alert(message):
    print(f"СРОЧНО: {message}")
    return f"СРОЧНО: {message}"