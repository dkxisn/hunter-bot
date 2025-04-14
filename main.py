import random
import string
import asyncio
from pyrogram import Client
from pyrogram.errors import UsernameInvalid, UsernameOccupied, FloodWait
import requests
import os

api_id = 29122339
api_hash = "562fa80d6ca06cc732b8d9c0c2110243"
string_session = "BAG8XyMAiYTRRGIgkmagpqTXM6zSgAlpSs7QhJ4t9zQAxpTkKzKo7kWlwHsHSpCnXCMFHnJ-7b21MtA7878JnByHBfY-6mI3AD8G7CqVLP9Ytp-jt80tKNYFnRfJsP6ZP_DpKUvwak-JipCqVP3cM0mt1KrMMz9_K7m_el5qSt0dZnUA1TUAO0gww6VmHjb5m0Jz3e8RWsNwDIyyda9WAz29UWKwYiXkGyZBrFGmz5VVvRqh1itJuYecSKl8BQf257mbaPCQWZS9aYVrzg57XfZE8yfsesDJeXHrxHjRT4c3D_W_EPij9061R-kbqMMcjwTQwiqxpuA8mKfhOKLrck_p5NzkAQAAAAHUA6KhAA"

BOT_TOKEN = "7635180275:AAFa3K4YnFROv_Vw-MiljhByStGS-0S6wJU"
CHAT_ID = 7635180275  # إرسال الإشعارات لنفس البوت

app = Client(name="hunter_session", api_id=api_id, api_hash=api_hash, session_string=string_session)

def generate_username():
    chars = string.ascii_lowercase + string.digits
    while True:
        u = random.choices(chars, k=3)
        yield f"{u[0]}_{u[1]}_{u[2]}"

def notify(text):
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={
            "chat_id": CHAT_ID,
            "text": text
        })
    except Exception as e:
        print(f"فشل في إرسال الإشعار: {e}")

async def hunt_usernames():
    async with app:
        notify("✅ تم تشغيل بوت الصيد.")
        for username in generate_username():
            print(f"🔎 تجربة: @{username}")
            try:
                await app.set_username(username)
                notify(f"🎯 تم صيد يوزر متاح وتغييره تلقائيًا: @{username}")
                break
            except UsernameOccupied:
                print("❌ محجوز")
            except UsernameInvalid:
                print("⚠️ غير صالح")
            except FloodWait as e:
                print(f"⏳ انتظار {e.value} ثانية بسبب الحظر المؤقت")
                await asyncio.sleep(e.value)
            except Exception as err:
                print(f"❌ خطأ: {err}")
            await asyncio.sleep(30)

if __name__ == "__main__":
    asyncio.run(hunt_usernames())