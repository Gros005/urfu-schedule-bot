import httpx
from .config import logger

def main():
    r = httpx.get('https://urfu.ru/api/v2/schedule/groups/63725/schedule?date_gte=2026-03-16&date_lte=2026-03-16')
    logger.info(r)
    logger.info(r.json()['events'][4]['title'])

if __name__ == "__main__":
    main()