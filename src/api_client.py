from .types import Group

from typing import Optional
from datetime import datetime, timedelta 
import httpx

class UrfuAPIClient:
    
    def __init__(self, 
                 base_url = "https://urfu.ru/api/v2"
                 ):
        self.base_url: str = base_url        

    def _get(self, endpoint, params):
        url = self.base_url + "/" + endpoint + "/"
        print(url)
        with httpx.Client(timeout=30.0) as client:
            response = client.get(url, params=params)
            response.raise_for_status()  # Проверка на HTTP ошибки
            return response.json()

    def search_groups(self, name: str) ->list[Group]:
        """Ищет группу по названию"""
        data = self._get("schedule/groups", {"search": name})
        if len(data)>1:
            print(f"Название группы введено не полностью, Найдено {len(data)} группы с названием {name}")
        
        group = Group(id=data[0]['id'],
                      divisionId=data[0]['divisionId'],
                      course=data[0]['course'],
                      title=data[0]['title'])

        return group

    def get_group_shedule(self,
                          group_id: str,
                          date_from: Optional[datetime] = None,
                          date_to: Optional[datetime] = None):
        """Получение расписания группы"""
        if date_from is None:
            date_from = datetime.now()
        if date_to is None:
            date_to = date_from + timedelta(days = 7)

        params = {
            'date_gte': date_from.strftime("%Y-%m-%d"),
            'date_lte': date_to.strftime("%Y-%m-%d")
        } 

        data = self._get(f"schedule/groups/{group_id}/schedule", params)

        return self._parse_shedule(data)
    
    def _parse_shedule(self, data):
        pass
        

def main():
    client = UrfuAPIClient()
    data = client.search_groups(name = 'МЕН-333009')
    data1 = client.get_group_shedule(data.id)
    print(data1)
