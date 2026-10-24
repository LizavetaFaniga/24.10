from tasks_24_10 import run_pipeline, run_full_distribution, urgent_alert
import time

if __name__ == '__main__':
    print("--- Запуск Задания 2 (Chain) ---")
    run_pipeline.delay("dummy_arg")
    
    time.sleep(2) 
    
    print("\n--- Запуск Задания 3 (Chord) ---")
    run_full_distribution.delay("dummy_arg")
    
    time.sleep(2)
    
    print("\n--- Запуск Задания 4 (Отложенная на 15 сек) ---")
    urgent_alert.apply_async(args=["Проверка связи!"], countdown=15)
    
    print("\nВсе задачи отправлены в очередь!")