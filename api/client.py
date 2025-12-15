# /home/xty/Documents/Projects/PetProject/BomberBot_GUI/BomberBot_GUI/api/client.py
import aiohttp
from .endpoints import *
import datetime


class APIClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "API-Key": api_key,
            "Content-Type": "application/json"
        }

    async def fetch_status(self):
        try:
            async with aiohttp.ClientSession(headers=self.headers) as s:
                async with s.get(SERVICE_STATUS_URL) as r:
                    return await r.json()
        except Exception as e:
            return {'detail': 'error', 'code': str(e)}

    async def fetch_balance(self):
        try:
            async with aiohttp.ClientSession(headers=self.headers) as s:
                async with s.get(BALANCE_URL) as r:
                    return await r.json()
        except Exception as e:
            return {'detail': 'error', 'code': str(e)}

    async def create_order_now_mode_time(self, phone: str, duration: int):
        start_time = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d %H:%M')
        payload = {
            "mode": "Time",
            "phone_number": phone,
            "duration": int(duration),
            "holder_timezone": "0",
            "scheduled_task": False,
            "start_time": start_time
        }
        try:
            async with aiohttp.ClientSession(headers=self.headers) as s:
                async with s.post(CREATE_ORDER_TIME_URL, json=payload) as r:
                    return await r.json()
        except Exception as e:
            return {'detail': 'error', 'code': str(e)}

    async def create_order_scheduled_mode_time(self, phone: str, duration: int, start_time: datetime):
        payload = {
            "mode": "Time",
            "phone_number": phone,
            "duration": int(duration),
            "holder_timezone": "0",
            "scheduled_task": True,
            "start_time": start_time
        }
        try:
            async with aiohttp.ClientSession(headers=self.headers) as s:
                async with s.post(CREATE_ORDER_TIME_URL, json=payload) as r:
                    return await r.json()
        except Exception as e:
            return {'detail': 'error', 'code': str(e)}

    async def create_order_now_mode_smart(self, phone: str, timezone: int):
        start_time = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d %H:%M')

        if int(timezone) > 0:
            timezone = f"+{timezone}"
        else:
            timezone = f"-{timezone}"

        payload = {
            "mode": "Smart",
            "phone_number": phone,
            "duration": 160,
            "holder_timezone": timezone,
            "scheduled_task": False,
            "start_time": start_time
        }
        try:
            async with aiohttp.ClientSession(headers=self.headers) as s:
                async with s.post(CREATE_ORDER_SMART_URL, json=payload) as r:
                    return await r.json()
        except Exception as e:
            return {'detail': 'error', 'code': str(e)}

    async def create_order_scheduled_mode_smart(self, phone: str, timezone: int, start_time: datetime):
        if int(timezone) > 0:
            timezone = f"+{timezone}"
        else:
            timezone = f"-{timezone}"
        payload = {
            "mode": "Smart",
            "phone_number": phone,
            "duration": 160,
            "holder_timezone": timezone,
            "scheduled_task": True,
            "start_time": start_time
        }
        try:
            async with aiohttp.ClientSession(headers=self.headers) as s:
                async with s.post(CREATE_ORDER_SMART_URL, json=payload) as r:
                    return await r.json()
        except Exception as e:
            return {'detail': 'error', 'code': str(e)}
