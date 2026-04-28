import sys # استدعاء مكتبة النظام للتعامل مع بيئة ويندوز
import asyncio # مكتبة المهام المتزامنة لتشغيل العمليات في الخلفية
import uvicorn # الخادم المحلي الذي سيشغل برنامج Nexus
from fastapi import FastAPI, Query # أدوات إنشاء الروابط من FastAPI
from fastapi.middleware.cors import CORSMiddleware # أداة السماح للواجهة بالاتصال بالسيرفر
from scraper import get_live_users # استدعاء محرك السحب الخاص بنا

# حل مشكلة توقف المتصفح الخفي في بيئة ويندوز
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

app = FastAPI() # إنشاء نسخة من تطبيق Nexus (السيرفر)

# متغيرات النظام للاحتفاظ بحالة البوت والعداد
bot_active = False # مفتاح التشغيل (متوقف افتراضياً)
live_count = 0     # عداد النتائج الحية

# إعدادات الأمان لفك الحظر والسماح لواجهة HTML بالتحدث مع بايثون
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # السماح لأي واجهة بالاتصال
    allow_methods=["*"], # السماح بجميع العمليات
    allow_headers=["*"], # السماح بجميع الترويسات
)

# الرابط الأول: إعطاء أمر البدء لمحرك Nexus
@app.get("/api/start")
async def start_bot(keyword: str = Query("Genel"), speed: int = Query(100)):
    global bot_active, live_count # السماح بتعديل المتغيرات العامة
    bot_active = True # تفعيل مفتاح البوت
    live_count = 0    # تصفير العداد
    
    # رسالة النظام في الشاشة السوداء بالهوية الجديدة
    print(f"🚀 Nexus Engine Started | القسم: {keyword} | السرعة: {speed}%")
    
    # دالة تحديث العداد التي سنرسلها للمحرك
    def update_count(count):
        global live_count
        live_count = count

    # إطلاق محرك TikTok Live Scraper
    await get_live_users(keyword, speed, lambda: bot_active, update_count)
    return {"status": "finished"}

# الرابط الثاني: إعطاء أمر الإيقاف
@app.get("/api/stop")
async def stop_bot():
    global bot_active
    bot_active = False # إيقاف المفتاح
    print("🛑 Nexus Engine Stopped (تم الإيقاف)") # رسالة الإيقاف
    return {"status": "stopped"}

# الرابط الثالث: رادار التحديث الحي للواجهة
@app.get("/api/status")
async def get_status():
    global live_count, bot_active
    return {"count": live_count, "active": bot_active} # إرسال البيانات للواجهة

# أمر تشغيل السيرفر تلقائياً عند فتح هذا الملف
if __name__ == "__main__":
    # log_level="warning" تمنع السيرفر من طباعة الرسائل الخضراء المزعجة كل ثانية
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")