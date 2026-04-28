import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
import os
import random
from datetime import datetime

async def get_live_users(keyword="Genel", speed=100, check_active=None, update_count=None):
    users_list = []
    
    # 1. إعداد المسارات أولاً (مهم جداً لكي تعمل الذاكرة)
    now = datetime.now()
    folder_day = now.strftime("%d-%m-%Y") # مجلد يومي لضمان عمل نظام منع التكرار
    save_directory = os.path.join("TikTokLiveBot", "Scraper", folder_day)
    os.makedirs(save_directory, exist_ok=True)
    filename = os.path.join(save_directory, f"{keyword}_TR.txt") 

    # 2. 🧠 نظام الذاكرة الدائمة (منع التكرار النهائي)
    seen_usernames = set()
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                seen_usernames = set(line.strip() for line in f if line.strip())
            print(f"🧠 ذاكرة نكسس: تم استرجاع {len(seen_usernames)} يوزر سابق. لن يتم تكرارهم.")
        except Exception as e:
            print(f"⚠️ تنبيه الذاكرة: {e}")
    
    # 3. إعدادات السرعة
    wait_delay = max((100 - speed) * 10, 500) / 1000 
    
    # 4. المكتبات الضخمة
    GAMING_KEYWORDS = [
        "roblox+türkiye", "pubg+mobile+tr", "free+fire+tr", "gta+5+rp+tr", "mobile+legends+tr",
    "fortnite+tr", "minecraft+türkçe", "valorant+tr", "call+of+duty+tr", "efootball+tr",
    "brawl+stars+tr", "clash+royale+tr", "fc+25+türkiye", "stumble+guys+tr", "metin2+tr",
    "knight+online+tr", "cs2+tr", "apex+legends+tr", "league+of+legends+tr", "arena+of+valor+tr",
    "euro+truck+simulator+2+tr", "car+parking+multiplayer+tr", "resident+evil+tr", "among+us+tr",
    "8+ball+pool+tr", "ludo+tr", "subway+surfers+tr", "slither.io+tr", "point+blank+tr",
    "growing+up+tr", "delta+force+tr", "arena+breakout+tr", "genshin+impact+tr", "pokemon+go+tr",
    "word+cookies+tr", "standoff+2+tr", "super+mario+64+tr", "world+of+warcraft+tr", "farming+simulator+tr"
    ]
    
    GENEL_KEYWORDS = [
        # --- كلمات التفاعل العام (High Traffic) ---
    "türkiye", "istanbul", "canlı+yayın", "sohbet", "muhabbet", "keşfet", "keşfetteyiz", 
    "takip", "gt", "takipet", "canlı", "yayın", "popüler", "türk", "türkiyem",
    
    # --- كلمات الدعم والهدايا (Agency/Support) ---
    "pk+match", "hediye", "sandık", "destek", "sıralama", "ranking", "puan", "jeton", 
    "hediyem", "gül", "aslan", "balon", "padişah", "rekor", "kapışma", "yarışma",
    
    # --- استهداف أكبر المدن التركية (Regional Target) ---
    "ankara", "izmir", "bursa", "antalya", "adana", "konya", "gaziantep", "şanlıurfa", 
    "mersin", "kocaeli", "diyarbakır", "hatay", "manisa", "kayseri", "samsun", "trabzon",
    
    # --- كلمات عاطفية واجتماعية (Social/Daily) ---
    "günaydın", "iyigeceler", "akşam", "canım", "dostlar", "aile", "ortam", "selam", 
    "merhaba", "huzur", "sevgi", "gönül", "canlar", "yolculuk", "hayat",
    
    # --- اهتمامات وهوايات (Lifestyle) ---
    "müzik", "türkü", "şarkı", "araba", "tofaş", "modifiye", "yemek", "mutfak", 
    "makyaj", "güzellik", "moda", "spor", "fenerbahçe", "galatasaray", "beşiktaş"
]

    try:
        with open(filename, "a", encoding="utf-8") as file: 
            async with Stealth().use_async(async_playwright()) as p: 
                
                user_data_dir = os.path.join(os.getcwd(), "NexusProfile")
                
                browser_context = await p.chromium.launch_persistent_context(
                    user_data_dir=user_data_dir, headless=False,
                    viewport={'width': 1280, 'height': 800},
                    locale="tr-TR", timezone_id="Europe/Istanbul",
                    geolocation={"longitude": 28.9784, "latitude": 41.0082},
                    permissions=["geolocation"],
                    args=["--disable-blink-features=AutomationControlled"]
                )
                
                page = browser_context.pages[0] 

                while check_active():
                    if keyword == "Genel":
                        urls = [f"https://www.tiktok.com/search/live?q={kw}" for kw in GENEL_KEYWORDS]
                    elif keyword == "Oyun":
                        urls = [f"https://www.tiktok.com/search/live?q={game}" for game in GAMING_KEYWORDS]
                    else:
                        urls = [f"https://www.tiktok.com/search/live?q={keyword}"]

                    for target_url in urls:
                        if not check_active(): break 
                        
                        await page.goto(target_url, timeout=60000) 
                        print(f"\n🚀 اكتساح القسم: {target_url}")
                        await page.wait_for_timeout(4000)
                        await page.mouse.click(640, 400) 

                        while check_active():
                            # 🛑 1. فحص نهاية الصفحة
                            is_end = await page.evaluate('''() => {
                                let txt = document.body.innerText;
                                return txt.includes('Başka sonuç yok') || txt.includes('No more results');
                            }''')

                            if is_end:
                                print("🏁 نهاية القسم. الانتقال للتالي...")
                                break 

                            # ⚡ 2. صيد اليوزرات
                            data = await page.evaluate('''() => {
                                return Array.from(document.querySelectorAll('a[href*="/live"]'))
                                    .map(a => ({
                                        user: (a.href.match(/@([^/?]+)/) || [])[1]
                                    })).filter(x => x.user);
                            }''')

                            for item in data:
                                if item['user'] not in seen_usernames:
                                    seen_usernames.add(item['user']) 
                                    file.write(f"{item['user']}\n") 
                                    file.flush() 
                                    if update_count: update_count(len(seen_usernames)) 
                                    print(f"✅ صيد جديد: {item['user']}")

                            # ⏬ 3. التمرير القسري السريع
                            await page.mouse.move(640, 750)
                            await page.mouse.down()
                            await page.mouse.move(640, 50, steps=2) 
                            await page.mouse.up()
                            
                            await page.keyboard.press("PageDown")

                            # 💡 4. حركة التنشيط
                            await page.keyboard.press("End")
                            await page.mouse.wheel(0, -300)
                            await asyncio.sleep(0.2)
                            await page.mouse.wheel(0, 800)

                            await asyncio.sleep(wait_delay)

                    print("🔄 انتهت الدورة.. إعادة المسح!")
                    await asyncio.sleep(2) 

                await browser_context.close() 

    except Exception as e:
        print(f"Nexus Error: {e}")
        
    return users_list