import httpx
from datetime import datetime, timedelta

def fetch_schedule(group_id: int, start_date: str = None, end_date: str = None) -> dict:
    """
    Получает расписание для конкретной группы (синхронная версия)
    """
    # Если даты не указаны, берем период в 2 недели от сегодня
    if not start_date:
        start_date = datetime.now().strftime("%Y-%m-%d")
    if not end_date:
        end_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
    
    url = f"https://urfu.ru/api/v2/schedule/groups/{group_id}/schedule"
    params = {
        "date_gte": start_date,
        "date_lte": end_date
    }
    
    try:
        # Создаем клиент и делаем запрос
        with httpx.Client(timeout=30.0) as client:
            response = client.get(url, params=params)
            response.raise_for_status()  # Проверка на HTTP ошибки
            return response.json()
            
    except httpx.HTTPStatusError as e:
        print(f"HTTP ошибка для группы {group_id}: {e}")
        print(f"Статус код: {e.response.status_code}")
        return None
    except httpx.RequestError as e:
        print(f"Ошибка соединения для группы {group_id}: {e}")
        return None
    except Exception as e:
        print(f"Неожиданная ошибка для группы {group_id}: {e}")
        return None

def print_schedule(data: dict):
    """
    Выводит расписание в читаемом формате
    """
    if not data or 'events' not in data:
        print("Нет данных о расписании")
        return
    
    group_info = data.get('group', {})
    print(f"\n{'='*60}")
    print(f"РАСПИСАНИЕ ДЛЯ ГРУППЫ: {group_info.get('title', 'Неизвестно')}")
    print(f"Курс: {group_info.get('course', 'Неизвестно')}")
    print(f"ID группы: {group_info.get('id', 'Неизвестно')}")
    print(f"{'='*60}")
    
    # Сортируем события по дате и времени
    events = sorted(data['events'], key=lambda x: (x['date'], x.get('timeBegin', '00:00:00')))
    
    current_date = None
    for event in events:
        # Разделитель для разных дней
        if event['date'] != current_date:
            current_date = event['date']
            print(f"\n📅 {current_date}")
            print("-" * 40)
        
        # Время занятия
        time_str = ""
        if event.get('timeBegin') and event.get('timeEnd'):
            time_str = f"{event['timeBegin'][:5]}-{event['timeEnd'][:5]}"
        elif event.get('timeBegin'):
            time_str = f"{event['timeBegin'][:5]}"
        else:
            time_str = "время не указано"
        
        # Номер пары
        pair_info = f"[{event.get('pairNumber', '?')} пара]" if event.get('pairNumber') else ""
        
        print(f"\n{time_str} {pair_info}")
        print(f"📚 {event['title']}")
        print(f"   Тип: {event.get('loadType', 'не указан')}")
        
        if event.get('teacherName'):
            print(f"   👨‍🏫 {event['teacherName']}")
        
        if event.get('auditoryTitle'):
            print(f"   🏛 Аудитория: {event['auditoryTitle']}")
            if event.get('auditoryLocation'):
                print(f"   📍 {event['auditoryLocation']}")
        
        if event.get('comment'):
            print(f"   📝 {event['comment']}")


def main1():
        # ID группы из вашего примера
    GROUP_ID = 63725
    
    print("🚀 Получаем расписание...")
    
    # Вариант 1: Полный с обработкой
    schedule_data = fetch_schedule(
        group_id=GROUP_ID,
        start_date="2026-03-16",
        end_date="2026-03-29"
    )
    
    if schedule_data:
        # Выводим расписание
        print_schedule(schedule_data)


def main():
    print('API UrFU')
