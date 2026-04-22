from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import json
import os
import time
import uuid
import requests

BOT_TOKEN = "8505375356:AAGknVv021Gnb5Akpz1kWwAjKuc3WgCmT2Y"
CRYPTOBOT_TOKEN = "511784:AAU9aOOW193fC7UQkg3trqZdF0FyMfOeaR4"
VIP_PRICE_USDT = 3
VIP_WEEK_STARS = 100
BINANCE = "https://api.binance.com/api/v3"
CRYPTO_API = "https://pay.crypt.bot/api"

ADMIN_IDS = [1609966483]

try:
    import numpy as np
except Exception:
    np = None

try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None


DATA_FILE = "users_data.json"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

users = {}

FREE_COINS = [
    "BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT", "TONUSDT", "DOGEUSDT", "TRXUSDT",
    "ADAUSDT", "AVAXUSDT", "LINKUSDT", "DOTUSDT", "LTCUSDT", "BCHUSDT", "ATOMUSDT", "NEARUSDT",
    "MATICUSDT", "SUIUSDT", "TIAUSDT", "UNIUSDT", "SHIBUSDT", "PEPEUSDT"
]

VIP_COINS = [
    "BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT", "TONUSDT",
    "TRXUSDT", "AVAXUSDT", "DOTUSDT", "LINKUSDT", "LTCUSDT", "BCHUSDT", "ATOMUSDT", "APTUSDT",
    "ARBUSDT", "OPUSDT", "NEARUSDT", "INJUSDT", "FILUSDT", "SUIUSDT", "TIAUSDT", "SEIUSDT",
    "HBARUSDT", "UNIUSDT", "ETCUSDT", "AAVEUSDT", "ICPUSDT", "PEPEUSDT", "SHIBUSDT", "MKRUSDT",
    "RNDRUSDT", "GALAUSDT", "VETUSDT", "ALGOUSDT", "XLMUSDT", "IMXUSDT", "RUNEUSDT", "SANDUSDT",
    "MANAUSDT", "AXSUSDT", "FLOWUSDT", "EOSUSDT", "XTZUSDT", "KAVAUSDT", "FTMUSDT", "JUPUSDT",
    "WLDUSDT", "NOTUSDT", "PYTHUSDT", "ENAUSDT", "TAOUSDT", "BONKUSDT", "FETUSDT", "WIFUSDT",
    "ARKMUSDT", "CRVUSDT", "DYDXUSDT", "PENDLEUSDT", "STRKUSDT", "ZROUSDT"
]

FREE_LIMIT = 4
VIP_LIMIT = 15

AUTO_INTERVAL_OPTIONS = {
    "10m": 600,
    "15m": 900,
    "30m": 1800,
    "1h": 3600,
    "2h": 7200,
    "4h": 14400,
}

MESSAGES = {
    "ua": {
        "welcome": (
            "🚀 *Crypto AI Signal Bot*\n\n"
            "Цей бот допомагає аналізувати ринок, але *не гарантує 100% успішності* і не є фінансовою порадою.\n\n"
            "Free:\n"
            "• базовий аналіз монет\n"
            "• обмежений список функцій\n\n"
            "VIP:\n"
            "• великий список монет\n"
            "• VIP-сканер ринку\n"
            "• сильніші сигнали\n"
            "• AUTO Signals з гнучким інтервалом\n"
            "• розширена аналітика по монетах"
        ),
        "choose_language": "Виберіть мову:",
        "lang_changed": "✅ Мову змінено",
        "only_vip": "❌ Ця функція доступна тільки для VIP",
        "free_locked": "🔒 У free ця функція обмежена. Відкрий VIP для повного доступу.",
        "vip_already": "✅ У тебе вже активний VIP",
        "vip_activated": "🎉 VIP активовано. Повний доступ відкрито.",
        "auto_on": "✅ Авто-сигнали увімкнено",
        "auto_off": "⛔ Авто-сигнали вимкнено",
        "auto_time_set": "⏱ Інтервал авто-сигналів змінено на {interval}",
        "profile": (
            "👤 *Профіль*\n"
            "ID: `{id}`\n"
            "План: {vip}\n"
            "VIP до: {vip_until}\n"
            "Auto: {auto}\n"
            "Інтервал: {interval}\n"
            "Мова: {lang}\n"
            "Обрані: {fav_count}\n"
            "Алерти: {alert_count}\n"
            "Історія сигналів: {history_count}"
        ),
        "choose_coin": "Виберіть монету для аналізу:",
        "choose_timeframe": "Виберіть таймфрейм:",
        "added_fav": "⭐ Монету додано в обрані",
        "fav_limit": "❌ Ліміт обраних: {limit}",
        "price_alert": "🚨 {coin} досягнув `{price}$`",
        "favorites_empty": "⭐ Список обраних поки порожній",
        "favorites_title": "⭐ *Обрані монети*",
        "removed_fav": "🗑 Монету видалено з обраних",
        "alert_set": "🔔 Алерт встановлено: `{coin}` -> `{price}$`",
        "alert_format": "Надішли у форматі:\n`BTCUSDT 70000`",
        "invalid_alert": "❌ Невірний формат. Приклад: `BTCUSDT 70000`",
        "top_market": "🔥 *Топ рухів за 24h*",
        "no_data": "❌ Дані тимчасово недоступні",
        "vip_buy_info": (
            "💎 *VIP дає більше сенсу боту:*\n"
            "• 45+ популярних монет\n"
            "• VIP scanner по всьому ринку\n"
            "• multi-timeframe аналіз\n"
            "• support / resistance / volatility\n"
            "• сильні сигнали та історія\n"
            "• AUTO Signals 10m / 15m / 30m / 1h / 2h / 4h\n"
            "• weekly VIP за Stars\n"
            "• більше обраних і алерти\n\n"
            f"Ціна місяць: *{VIP_PRICE_USDT} USDT*\n"
            f"Тиждень через Stars: *{VIP_WEEK_STARS} ⭐*"
        ),
        "vip_created": "💳 Рахунок для VIP створено. Натисни кнопку нижче для оплати.",
        "stars_invoice_sent": "⭐ Інвойс на тижневий VIP через Stars відправлено.",
        "stars_week_activated": "⭐ VIP через Stars активовано на 7 днів.",
        "invoice_wait": "⌛ Оплату ще не підтверджено. Якщо вже оплатив, перевір ще раз через кілька секунд.",
        "invoice_expired": "⌛ Рахунок більше неактивний. Створи новий.",
        "invoice_error": "❌ Не вдалося створити рахунок. Перевір CryptoBot токен.",
        "market_unavailable": "⚠️ Дані ринку тимчасово недоступні",
        "chart_unavailable": "⚠️ Графік недоступний без `matplotlib`",
        "main_menu": "Головне меню",
        "auto_settings": "⚙️ Налаштування AUTO Signals:",
        "already_listed": "ℹ️ Ця монета вже є в обраних",
        "broadcast_done": "✅ Розсилку завершено. Надіслано: {sent}",
        "admin_only": "❌ Команда лише для адміністратора",
        "payment_caption": "💎 *Оплата VIP*\nБезпечно через CryptoBot",
        "scanner_title": "🧠 *VIP Scanner*",
        "history_empty": "📭 Історія сигналів поки порожня",
        "history_title": "🗂 *Останні сигнали*",
        "market_mood": "🌍 *Настрій ринку*",
        "trend_bull": "Бичачий",
        "trend_bear": "Ведмежий",
        "trend_flat": "Нейтральний",
        "risk_label": "Ризик",
        "strength_label": "Сила",
        "support_label": "Підтримка",
        "resistance_label": "Опір",
        "volatility_label": "Волатильність",
        "free_hint": "Free версія дає базовий вхід. Найсильніші сигнали та сканер відкриті у VIP.",
        "signal_saved": "📝 Сигнал збережено в історію",
        "vip_report_title": "💎 *VIP Аналіз*",
        "free_report_title": "🆓 *Free Аналіз*",
        "top_buy_title": "📈 *VIP Top BUY*",
        "top_sell_title": "📉 *VIP Top SELL*",
        "admin_stats": (
            "🛠 *Адмін статистика*\n"
            "Користувачів: `{users}`\n"
            "VIP: `{vip}`\n"
            "Free: `{free}`\n"
            "Алертів: `{alerts}`\n"
            "Обраних: `{favorites}`"
        ),
        "vip_granted": "✅ VIP видано користувачу `{uid}`",
        "vip_revoked": "✅ VIP знято у користувача `{uid}`",
    },
    "en": {
        "welcome": (
            "🚀 *Crypto AI Signal Bot*\n\n"
            "This bot helps analyze the market, but it *does not guarantee 100% success* and is not financial advice.\n\n"
            "Free:\n"
            "• basic coin analysis\n"
            "• limited feature set\n\n"
            "VIP:\n"
            "• many more coins\n"
            "• VIP market scanner\n"
            "• stronger signals\n"
            "• AUTO Signals with flexible intervals\n"
            "• extended coin analytics"
        ),
        "choose_language": "Choose language:",
        "lang_changed": "✅ Language changed",
        "only_vip": "❌ This feature is VIP only",
        "free_locked": "🔒 This feature is limited on free. Unlock VIP for full access.",
        "vip_already": "✅ VIP is already active",
        "vip_activated": "🎉 VIP activated. Full access unlocked.",
        "auto_on": "✅ Auto-signals enabled",
        "auto_off": "⛔ Auto-signals disabled",
        "auto_time_set": "⏱ Auto interval changed to {interval}",
        "profile": (
            "👤 *Profile*\n"
            "ID: `{id}`\n"
            "Plan: {vip}\n"
            "VIP until: {vip_until}\n"
            "Auto: {auto}\n"
            "Interval: {interval}\n"
            "Language: {lang}\n"
            "Favorites: {fav_count}\n"
            "Alerts: {alert_count}\n"
            "Signal history: {history_count}"
        ),
        "choose_coin": "Choose a coin:",
        "choose_timeframe": "Choose timeframe:",
        "added_fav": "⭐ Coin added to favorites",
        "fav_limit": "❌ Favorites limit: {limit}",
        "price_alert": "🚨 {coin} reached `{price}$`",
        "favorites_empty": "⭐ Favorites list is empty",
        "favorites_title": "⭐ *Favorite coins*",
        "removed_fav": "🗑 Coin removed from favorites",
        "alert_set": "🔔 Alert set: `{coin}` -> `{price}$`",
        "alert_format": "Send in format:\n`BTCUSDT 70000`",
        "invalid_alert": "❌ Invalid format. Example: `BTCUSDT 70000`",
        "top_market": "🔥 *Top 24h movers*",
        "no_data": "❌ Data temporarily unavailable",
        "vip_buy_info": (
            "💎 *VIP makes the bot actually stronger:*\n"
            "• 45+ popular coins\n"
            "• VIP scanner across the market\n"
            "• multi-timeframe analysis\n"
            "• support / resistance / volatility\n"
            "• stronger signals and history\n"
            "• AUTO Signals 10m / 15m / 30m / 1h / 2h / 4h\n"
            "• weekly VIP via Stars\n"
            "• more favorites and alerts\n\n"
            f"Monthly price: *{VIP_PRICE_USDT} USDT*\n"
            f"Weekly via Stars: *{VIP_WEEK_STARS} ⭐*"
        ),
        "vip_created": "💳 VIP invoice created. Tap the button below to pay.",
        "stars_invoice_sent": "⭐ Weekly VIP Stars invoice sent.",
        "stars_week_activated": "⭐ VIP via Stars activated for 7 days.",
        "invoice_wait": "⌛ Payment is not confirmed yet. If you already paid, check again in a few seconds.",
        "invoice_expired": "⌛ Invoice is no longer active. Create a new one.",
        "invoice_error": "❌ Could not create invoice. Check the CryptoBot token.",
        "market_unavailable": "⚠️ Market data is temporarily unavailable",
        "chart_unavailable": "⚠️ Chart is unavailable without `matplotlib`",
        "main_menu": "Main menu",
        "auto_settings": "⚙️ AUTO Signals settings:",
        "already_listed": "ℹ️ This coin is already in favorites",
        "broadcast_done": "✅ Broadcast complete. Sent: {sent}",
        "admin_only": "❌ Admin only command",
        "payment_caption": "💎 *VIP payment*\nSecure via CryptoBot",
        "scanner_title": "🧠 *VIP Scanner*",
        "history_empty": "📭 Signal history is empty",
        "history_title": "🗂 *Recent signals*",
        "market_mood": "🌍 *Market mood*",
        "trend_bull": "Bullish",
        "trend_bear": "Bearish",
        "trend_flat": "Neutral",
        "risk_label": "Risk",
        "strength_label": "Strength",
        "support_label": "Support",
        "resistance_label": "Resistance",
        "volatility_label": "Volatility",
        "free_hint": "Free version is a basic entry point. The strongest signals and scanner are VIP-only.",
        "signal_saved": "📝 Signal saved to history",
        "vip_report_title": "💎 *VIP Analysis*",
        "free_report_title": "🆓 *Free Analysis*",
        "top_buy_title": "📈 *VIP Top BUY*",
        "top_sell_title": "📉 *VIP Top SELL*",
        "admin_stats": (
            "🛠 *Admin stats*\n"
            "Users: `{users}`\n"
            "VIP: `{vip}`\n"
            "Free: `{free}`\n"
            "Alerts: `{alerts}`\n"
            "Favorites: `{favorites}`"
        ),
        "vip_granted": "✅ VIP granted to `{uid}`",
        "vip_revoked": "✅ VIP revoked for `{uid}`",
    },
}


def save_users():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def load_users():
    global users
    if not os.path.exists(DATA_FILE):
        users = {}
        return
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
        users = {int(k): v for k, v in raw.items()}
    except Exception:
        users = {}


def get_user(uid):
    if uid not in users:
        users[uid] = {
            "vip": False,
            "vip_until": 0,
            "favorites": [],
            "alerts": {},
            "last_coin": None,
            "last_timeframe": "15m",
            "auto": False,
            "interval": AUTO_INTERVAL_OPTIONS["30m"],
            "last_signal": 0,
            "invoice_id": None,
            "invoice_url": None,
            "lang": "ua",
            "awaiting_alert": False,
            "history": [],
        }
        save_users()

    user = users[uid]
    user.setdefault("vip_until", 0)
    user.setdefault("favorites", [])
    user.setdefault("alerts", {})
    user.setdefault("last_coin", None)
    user.setdefault("last_timeframe", "15m")
    user.setdefault("auto", False)
    user.setdefault("interval", AUTO_INTERVAL_OPTIONS["30m"])
    user.setdefault("last_signal", 0)
    user.setdefault("invoice_id", None)
    user.setdefault("invoice_url", None)
    user.setdefault("lang", "ua")
    user.setdefault("awaiting_alert", False)
    user.setdefault("history", [])
    return user


def msg(uid, key, **kwargs):
    lang = get_user(uid).get("lang", "ua")
    return MESSAGES.get(lang, MESSAGES["ua"]).get(key, key).format(**kwargs)


def user_is_vip(uid):
    user = get_user(uid)
    if user.get("vip", False):
        return True
    return user.get("vip_until", 0) > int(time.time())


def format_vip_until(uid):
    user = get_user(uid)
    if user.get("vip", False):
        return "`∞`"
    vip_until = int(user.get("vip_until", 0) or 0)
    if vip_until <= int(time.time()):
        return "`-`"
    days_left = max(1, int((vip_until - time.time()) // 86400) + 1)
    return f"`{days_left} дн.`"


def api_get_json(url, headers=None, timeout=10):
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except Exception:
        return None


def api_post_json(url, payload=None, headers=None, timeout=10):
    try:
        response = requests.post(url, json=payload or {}, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except Exception:
        return None


def crypto_headers():
    return {"Crypto-Pay-API-Token": CRYPTOBOT_TOKEN}


def create_vip_invoice(uid):
    payload = {
        "asset": "USDT",
        "amount": str(VIP_PRICE_USDT),
        "description": "Crypto AI Signal Bot VIP access",
        "hidden_message": "VIP activated successfully. Return to the bot and tap payment check.",
        "paid_btn_name": "openBot",
        "paid_btn_url": "https://t.me/",
        "payload": f"vip:{uid}:{uuid.uuid4().hex[:8]}",
        "allow_comments": True,
        "allow_anonymous": True,
        "expires_in": 3600,
    }
    data = api_post_json(f"{CRYPTO_API}/createInvoice", payload=payload, headers=crypto_headers())
    if not data or not data.get("ok"):
        return None
    result = data.get("result") or {}
    return {
        "invoice_id": result.get("invoice_id"),
        "invoice_url": result.get("bot_invoice_url") or result.get("pay_url"),
    }


def get_invoice_status(invoice_id):
    data = api_get_json(f"{CRYPTO_API}/getInvoices?invoice_ids={invoice_id}", headers=crypto_headers())
    if not data or not data.get("ok"):
        return None
    items = ((data.get("result") or {}).get("items") or [])
    return items[0] if items else None


def klines(symbol, interval="15m", limit=120):
    data = api_get_json(f"{BINANCE}/klines?symbol={symbol}&interval={interval}&limit={limit}")
    if not data or not isinstance(data, list):
        return []
    try:
        return [float(item[4]) for item in data]
    except Exception:
        return []


def get_price(symbol):
    data = api_get_json(f"{BINANCE}/ticker/price?symbol={symbol}")
    try:
        return float(data["price"])
    except Exception:
        return 0.0


def ticker_24h(symbol):
    data = api_get_json(f"{BINANCE}/ticker/24hr?symbol={symbol}")
    if not data:
        return None
    try:
        return {
            "change_percent": float(data.get("priceChangePercent", 0)),
            "high": float(data.get("highPrice", 0)),
            "low": float(data.get("lowPrice", 0)),
            "volume": float(data.get("quoteVolume", 0)),
        }
    except Exception:
        return None


def market_movers(limit=12):
    data = api_get_json(f"{BINANCE}/ticker/24hr")
    if not data or not isinstance(data, list):
        return []
    result = []
    for item in data:
        symbol = item.get("symbol", "")
        if not symbol.endswith("USDT"):
            continue
        try:
            change_percent = float(item.get("priceChangePercent", 0))
            volume = float(item.get("quoteVolume", 0))
        except Exception:
            continue
        if volume < 1_500_000:
            continue
        result.append({"symbol": symbol, "change_percent": change_percent, "volume": volume})
    result.sort(key=lambda x: abs(x["change_percent"]), reverse=True)
    return result[:limit]


def mean(values):
    return sum(values) / len(values) if values else 0.0


def diff(values):
    return [values[i] - values[i - 1] for i in range(1, len(values))]


def RSI(data, period=14):
    if len(data) < period + 1:
        return 50.0
    changes = diff(data)
    gains = [x if x > 0 else 0 for x in changes[-period:]]
    losses = [-x if x < 0 else 0 for x in changes[-period:]]
    avg_gain = mean(gains)
    avg_loss = mean(losses) or 0.0001
    rs = avg_gain / avg_loss
    return round(100 - (100 / (1 + rs)), 2)


def EMA(data, period):
    if not data:
        return 0.0
    if len(data) < period:
        return float(data[-1])
    if np is not None:
        weights = np.exp(np.linspace(-1.0, 0.0, period))
        weights /= weights.sum()
        return float(np.convolve(np.array(data, dtype=float), weights, mode="valid")[-1])
    multiplier = 2 / (period + 1)
    ema = float(data[0])
    for price in data[1:]:
        ema = (float(price) - ema) * multiplier + ema
    return ema


def support_resistance(data):
    if len(data) < 20:
        return 0.0, 0.0
    zone = data[-20:]
    return min(zone), max(zone)


def volatility_percent(data):
    if len(data) < 2 or not data[-1]:
        return 0.0
    high = max(data[-20:]) if len(data) >= 20 else max(data)
    low = min(data[-20:]) if len(data) >= 20 else min(data)
    return round(((high - low) / data[-1]) * 100, 2)


def calc_signal_data(symbol, interval="15m"):
    prices = klines(symbol, interval=interval)
    if len(prices) < 35:
        return None

    rsi = RSI(prices)
    ema9 = EMA(prices, 9)
    ema21 = EMA(prices, 21)
    current = prices[-1]
    support, resistance = support_resistance(prices)
    volatility = volatility_percent(prices)

    strength = 0
    if ema9 > ema21:
        strength += 30
    else:
        strength -= 30
    if rsi < 32:
        strength += 25
    elif rsi > 68:
        strength -= 25
    if current > ema9:
        strength += 20
    else:
        strength -= 20
    if volatility > 4:
        strength += 10
    strength = max(-100, min(100, strength))

    risk = "Low"
    if volatility >= 6:
        risk = "High"
    elif volatility >= 3:
        risk = "Medium"

    if rsi < 30 and ema9 > ema21:
        signal = "🟢 BUY"
        reason = f"RSI {rsi} + bullish EMA crossover"
    elif rsi > 70 and ema9 < ema21:
        signal = "🔴 SELL"
        reason = f"RSI {rsi} + bearish EMA crossover"
    elif ema9 > ema21 and rsi < 60 and current > ema9:
        signal = "🟢 BUY"
        reason = f"Trend continuation, RSI {rsi}"
    elif ema9 < ema21 and rsi > 40 and current < ema9:
        signal = "🔴 SELL"
        reason = f"Downtrend pressure, RSI {rsi}"
    else:
        signal = "🟡 HOLD"
        reason = f"No clean setup, RSI {rsi}"

    return {
        "signal": signal,
        "reason": reason,
        "rsi": rsi,
        "ema9": ema9,
        "ema21": ema21,
        "support": support,
        "resistance": resistance,
        "volatility": volatility,
        "strength": strength,
        "risk": risk,
        "current": current,
    }


def market_mood():
    watched = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT", "DOGEUSDT"]
    total = 0
    count = 0
    for symbol in watched:
        ticker = ticker_24h(symbol)
        if ticker:
            total += ticker["change_percent"]
            count += 1
    if not count:
        return None
    avg = total / count
    if avg > 1.25:
        trend = "bull"
    elif avg < -1.25:
        trend = "bear"
    else:
        trend = "flat"
    return {"avg": avg, "trend": trend}


def format_price(value):
    if value >= 1000:
        return f"{value:,.2f}"
    if value >= 1:
        return f"{value:.4f}"
    return f"{value:.6f}"


def timeframe_menu(symbol):
    kb = InlineKeyboardMarkup(row_width=3)
    for tf in ["15m", "1h", "4h"]:
        kb.insert(InlineKeyboardButton(tf, callback_data=f"tf_{symbol}_{tf}"))
    return kb


def coin_actions_inline(symbol, user):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("⭐ В обрані", callback_data="add_fav"),
        InlineKeyboardButton("🔄 Оновити", callback_data=f"refresh_{symbol}"),
    )
    kb.add(InlineKeyboardButton("🕒 Таймфрейм", callback_data=f"timeframe_{symbol}"))
    if user.get("vip"):
        kb.add(InlineKeyboardButton("🔔 Алерт", callback_data=f"prepare_alert_{symbol}"))
    return kb


def coins_menu_inline(user, page=0):
    kb = InlineKeyboardMarkup(row_width=2)
    coins = VIP_COINS if user["vip"] else FREE_COINS
    per_page = 8
    start = page * per_page
    for coin in coins[start:start + per_page]:
        kb.insert(InlineKeyboardButton(f"💰 {coin}", callback_data=f"coin_{coin}"))
    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton("⬅️", callback_data=f"page_{page-1}"))
    if start + per_page < len(coins):
        nav.append(InlineKeyboardButton("➡️", callback_data=f"page_{page+1}"))
    if nav:
        kb.row(*nav)
    return kb


def favorites_menu_inline(favorites):
    kb = InlineKeyboardMarkup(row_width=1)
    for coin in favorites:
        kb.add(InlineKeyboardButton(f"📊 {coin}", callback_data=f"coin_{coin}"))
        kb.add(InlineKeyboardButton(f"🗑 Видалити {coin}", callback_data=f"remove_fav_{coin}"))
    return kb


def lang_menu_inline():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("🇺🇦 UA", callback_data="lang_ua"),
        InlineKeyboardButton("🇬🇧 EN", callback_data="lang_en"),
    )
    return kb


def vip_menu_inline(user):
    kb = InlineKeyboardMarkup(row_width=1)
    if user.get("invoice_url") and user.get("invoice_id"):
        kb.add(InlineKeyboardButton("💳 Оплатити VIP", url=user["invoice_url"]))
        kb.add(InlineKeyboardButton("✅ Перевірити оплату", callback_data="check_vip_payment"))
        kb.add(InlineKeyboardButton("🆕 Створити новий рахунок", callback_data="buy_vip"))
    else:
        kb.add(InlineKeyboardButton("💎 Купити VIP", callback_data="buy_vip"))
    kb.add(InlineKeyboardButton(f"⭐ VIP на 7 днів за {VIP_WEEK_STARS} Stars", callback_data="buy_vip_stars_week"))
    return kb


def payment_inline(invoice_url):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("💳 Перейти до оплати", url=invoice_url))
    kb.add(InlineKeyboardButton("✅ Я оплатив", callback_data="check_vip_payment"))
    return kb


def auto_menu(user):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("▶️ Увімкнути", "⏹ Вимкнути")
    kb.add("⏱ 10 хв", "⏱ 15 хв", "⏱ 30 хв")
    kb.add("⏱ 1 година", "⏱ 2 години", "⏱ 4 години")
    if user.get("vip"):
        kb.add("🧠 VIP Сканер", "🗂 Історія")
    kb.add("🔙 Назад")
    return kb


def main_menu(user=None):
    user = user or {"vip": False}
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("📈 Монети", "⭐ Обрані")
    kb.add("🔥 Топ рухів", "🌍 Настрій ринку")
    if user.get("vip"):
        kb.add("🔔 Алерт", "🤖 Auto Signals")
        kb.add("🧠 VIP Сканер", "🗂 Історія")
        kb.add("📈 Top BUY", "📉 Top SELL")
    else:
        kb.add("🤖 Auto Signals", "💎 VIP")
    kb.add("👤 Профіль", "🌐 Мова")
    return kb


def interval_label(seconds):
    for label, value in AUTO_INTERVAL_OPTIONS.items():
        if value == seconds:
            return label
    return "30m"


def build_report(uid, symbol, timeframe="15m"):
    user = get_user(uid)
    signal_data = calc_signal_data(symbol, interval=timeframe)
    ticker = ticker_24h(symbol)
    if not signal_data or not ticker:
        return msg(uid, "market_unavailable")

    if user["vip"]:
        title = msg(uid, "vip_report_title")
        return (
            f"{title}\n"
            f"🪙 *{symbol}*  `{timeframe}`\n"
            f"💲 Ціна: `{format_price(signal_data['current'])}$`\n"
            f"📊 Сигнал: *{signal_data['signal']}*\n"
            f"🤖 {signal_data['reason']}\n"
            f"📈 RSI: `{signal_data['rsi']}`\n"
            f"⚡ EMA9 / EMA21: `{format_price(signal_data['ema9'])}` / `{format_price(signal_data['ema21'])}`\n"
            f"🧱 {msg(uid, 'support_label')}: `{format_price(signal_data['support'])}`\n"
            f"🚧 {msg(uid, 'resistance_label')}: `{format_price(signal_data['resistance'])}`\n"
            f"🌪 {msg(uid, 'volatility_label')}: `{signal_data['volatility']}%`\n"
            f"💪 {msg(uid, 'strength_label')}: `{signal_data['strength']}`\n"
            f"⚠️ {msg(uid, 'risk_label')}: `{signal_data['risk']}`\n"
            f"🕒 24h: `{ticker['change_percent']:+.2f}%`\n"
            f"⬆️ High: `{format_price(ticker['high'])}`\n"
            f"⬇️ Low: `{format_price(ticker['low'])}`"
        )

    title = msg(uid, "free_report_title")
    return (
        f"{title}\n"
        f"🪙 *{symbol}*  `{timeframe}`\n"
        f"💲 Ціна: `{format_price(signal_data['current'])}$`\n"
        f"📊 Сигнал: *{signal_data['signal']}*\n"
        f"📈 RSI: `{signal_data['rsi']}`\n"
        f"🕒 24h: `{ticker['change_percent']:+.2f}%`\n\n"
        f"{msg(uid, 'free_hint')}"
    )


def save_signal_history(uid, symbol, timeframe, signal_data):
    user = get_user(uid)
    history = user.get("history", [])
    history.insert(0, {
        "symbol": symbol,
        "timeframe": timeframe,
        "signal": signal_data["signal"],
        "strength": signal_data["strength"],
        "ts": int(time.time()),
    })
    user["history"] = history[:20]
    save_users()


def make_chart(symbol, timeframe="15m"):
    if plt is None:
        return None
    prices = klines(symbol, interval=timeframe)
    if not prices:
        return None
    ema9 = [EMA(prices[: i + 1], 9) for i in range(len(prices))]
    ema21 = [EMA(prices[: i + 1], 21) for i in range(len(prices))]
    plt.figure(figsize=(9, 4.5))
    plt.style.use("dark_background")
    plt.plot(prices, color="#00E38C", linewidth=2, label="Price")
    plt.plot(ema9, color="#FFB000", linewidth=1.2, label="EMA 9")
    plt.plot(ema21, color="#45A9FF", linewidth=1.2, label="EMA 21")
    plt.title(f"{symbol} {timeframe}")
    plt.grid(alpha=0.18)
    plt.legend()
    plt.tight_layout()
    path = f"chart_{uuid.uuid4().hex[:6]}.png"
    plt.savefig(path, dpi=150)
    plt.close()
    return path


async def send_coin_analysis(uid, symbol, timeframe=None):
    user = get_user(uid)
    timeframe = timeframe or user.get("last_timeframe", "15m")
    user["last_coin"] = symbol
    user["last_timeframe"] = timeframe
    save_users()

    report = build_report(uid, symbol, timeframe)
    signal_data = calc_signal_data(symbol, interval=timeframe)
    if signal_data:
        save_signal_history(uid, symbol, timeframe, signal_data)

    chart = make_chart(symbol, timeframe=timeframe) if user.get("vip") else None
    markup = coin_actions_inline(symbol, user)

    if chart:
        try:
            with open(chart, "rb") as photo:
                await bot.send_photo(uid, photo, caption=report, parse_mode="Markdown", reply_markup=markup)
        finally:
            if os.path.exists(chart):
                os.remove(chart)
    else:
        if user.get("vip") and plt is None:
            report += "\n\n" + msg(uid, "chart_unavailable")
        await bot.send_message(uid, report, parse_mode="Markdown", reply_markup=markup)


async def activate_vip(uid, days=None):
    user = get_user(uid)
    if days is None:
        user["vip"] = True
        user["vip_until"] = 0
    else:
        current_until = int(user.get("vip_until", 0) or 0)
        base = max(int(time.time()), current_until)
        user["vip_until"] = base + days * 86400
    user["invoice_id"] = None
    user["invoice_url"] = None
    save_users()
    await bot.send_message(uid, msg(uid, "vip_activated"), reply_markup=main_menu(user))


def format_history(uid):
    user = get_user(uid)
    if not user["history"]:
        return msg(uid, "history_empty")
    lines = [msg(uid, "history_title"), ""]
    for item in user["history"][:10]:
        lines.append(
            f"`{item['symbol']}` {item['timeframe']} {item['signal']} | strength `{item['strength']}`"
        )
    return "\n".join(lines)


def run_vip_scanner(uid):
    if not user_is_vip(uid):
        return None
    picks = []
    for symbol in VIP_COINS:
        signal_data = calc_signal_data(symbol, interval="15m")
        if not signal_data:
            continue
        if signal_data["signal"] == "🟡 HOLD":
            continue
        score = abs(signal_data["strength"])
        if signal_data["signal"] == "🟢 BUY":
            score += 5
        ticker = ticker_24h(symbol) or {"change_percent": 0}
        picks.append({
            "symbol": symbol,
            "signal": signal_data["signal"],
            "strength": signal_data["strength"],
            "volatility": signal_data["volatility"],
            "change": ticker["change_percent"],
            "score": score,
        })
    picks.sort(key=lambda x: x["score"], reverse=True)
    if not picks:
        return msg(uid, "no_data")

    lines = [msg(uid, "scanner_title"), ""]
    for item in picks[:8]:
        lines.append(
            f"{item['signal']} `{item['symbol']}` | power `{item['strength']}` | 24h `{item['change']:+.2f}%` | vol `{item['volatility']}%`"
        )
    return "\n".join(lines)


def run_directional_scanner(uid, direction="buy"):
    if not user_is_vip(uid):
        return None
    title_key = "top_buy_title" if direction == "buy" else "top_sell_title"
    picks = []
    for symbol in VIP_COINS:
        signal_data = calc_signal_data(symbol, interval="15m")
        if not signal_data:
            continue
        if direction == "buy" and signal_data["signal"] != "🟢 BUY":
            continue
        if direction == "sell" and signal_data["signal"] != "🔴 SELL":
            continue
        ticker = ticker_24h(symbol) or {"change_percent": 0}
        picks.append({
            "symbol": symbol,
            "strength": abs(signal_data["strength"]),
            "volatility": signal_data["volatility"],
            "change": ticker["change_percent"],
        })
    picks.sort(key=lambda x: (x["strength"], abs(x["change"])), reverse=True)
    if not picks:
        return msg(uid, "no_data")
    lines = [msg(uid, title_key), ""]
    for item in picks[:8]:
        lines.append(
            f"`{item['symbol']}` | power `{item['strength']}` | 24h `{item['change']:+.2f}%` | vol `{item['volatility']}%`"
        )
    return "\n".join(lines)


def get_admin_stats(uid):
    total_users = len(users)
    vip_users = sum(1 for user in users.values() if user.get("vip"))
    free_users = total_users - vip_users
    total_alerts = sum(len(user.get("alerts", {})) for user in users.values())
    total_favorites = sum(len(user.get("favorites", [])) for user in users.values())
    return msg(
        uid,
        "admin_stats",
        users=total_users,
        vip=vip_users,
        free=free_users,
        alerts=total_alerts,
        favorites=total_favorites,
    )


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    user = get_user(message.from_user.id)
    await message.answer(msg(message.from_user.id, "welcome"), parse_mode="Markdown", reply_markup=main_menu(user))


@dp.message_handler(commands=["vip_free"])
async def vip_free(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer(msg(message.from_user.id, "admin_only"))
        return
    args = message.text.split()
    uid = int(args[1]) if len(args) > 1 else message.from_user.id
    await activate_vip(uid)
    await message.answer(f"✅ VIP видано для {uid}")


@dp.message_handler(commands=["vip_grant"])
async def vip_grant(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer(msg(message.from_user.id, "admin_only"))
        return
    args = message.text.split()
    if len(args) < 2 or not args[1].isdigit():
        await message.answer("Використання: /vip_grant USER_ID")
        return
    uid = int(args[1])
    await activate_vip(uid)
    await message.answer(msg(message.from_user.id, "vip_granted", uid=uid), parse_mode="Markdown")


@dp.message_handler(commands=["vip_revoke"])
async def vip_revoke(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer(msg(message.from_user.id, "admin_only"))
        return
    args = message.text.split()
    if len(args) < 2 or not args[1].isdigit():
        await message.answer("Використання: /vip_revoke USER_ID")
        return
    uid = int(args[1])
    target = get_user(uid)
    target["vip"] = False
    target["vip_until"] = 0
    target["auto"] = False
    save_users()
    await message.answer(msg(message.from_user.id, "vip_revoked", uid=uid), parse_mode="Markdown")


@dp.message_handler(commands=["stats"])
async def stats_cmd(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer(msg(message.from_user.id, "admin_only"))
        return
    await message.answer(get_admin_stats(message.from_user.id), parse_mode="Markdown")


@dp.message_handler(commands=["broadcast"])
async def broadcast_cmd(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer(msg(message.from_user.id, "admin_only"))
        return
    text = message.text.replace("/broadcast", "", 1).strip()
    if not text:
        await message.answer("Використання: /broadcast текст повідомлення")
        return
    sent = 0
    for uid in list(users.keys()):
        try:
            await bot.send_message(uid, text)
            sent += 1
        except Exception:
            pass
    await message.answer(msg(message.from_user.id, "broadcast_done", sent=sent))


@dp.message_handler(lambda m: m.text == "🌐 Мова")
async def lang_cmd(message: types.Message):
    await message.answer(msg(message.from_user.id, "choose_language"), reply_markup=lang_menu_inline())


@dp.callback_query_handler(lambda c: c.data.startswith("lang_"))
async def lang_cb(callback: types.CallbackQuery):
    user = get_user(callback.from_user.id)
    user["lang"] = callback.data.split("_")[1]
    save_users()
    await callback.answer(msg(callback.from_user.id, "lang_changed"))
    await bot.send_message(callback.from_user.id, msg(callback.from_user.id, "welcome"), parse_mode="Markdown", reply_markup=main_menu(user))


@dp.message_handler(lambda m: m.text == "📈 Монети")
async def coins_cmd(message: types.Message):
    user = get_user(message.from_user.id)
    await message.answer(msg(message.from_user.id, "choose_coin"), reply_markup=coins_menu_inline(user))


@dp.callback_query_handler(lambda c: c.data.startswith("page_"))
async def page_cb(callback: types.CallbackQuery):
    user = get_user(callback.from_user.id)
    page = int(callback.data.split("_")[1])
    await callback.message.edit_reply_markup(reply_markup=coins_menu_inline(user, page))
    await callback.answer()


@dp.callback_query_handler(lambda c: c.data.startswith("coin_"))
async def coin_cb(callback: types.CallbackQuery):
    symbol = callback.data.split("_", 1)[1]
    await send_coin_analysis(callback.from_user.id, symbol)
    await callback.answer()


@dp.callback_query_handler(lambda c: c.data.startswith("refresh_"))
async def refresh_coin(callback: types.CallbackQuery):
    symbol = callback.data.split("_", 1)[1]
    user = get_user(callback.from_user.id)
    await send_coin_analysis(callback.from_user.id, symbol, timeframe=user.get("last_timeframe", "15m"))
    await callback.answer("Оновлено")


@dp.callback_query_handler(lambda c: c.data.startswith("timeframe_"))
async def timeframe_choose(callback: types.CallbackQuery):
    symbol = callback.data.split("_", 1)[1]
    await bot.send_message(callback.from_user.id, msg(callback.from_user.id, "choose_timeframe"), reply_markup=timeframe_menu(symbol))
    await callback.answer()


@dp.callback_query_handler(lambda c: c.data.startswith("tf_"))
async def timeframe_selected(callback: types.CallbackQuery):
    _, symbol, timeframe = callback.data.split("_", 2)
    user = get_user(callback.from_user.id)
    if timeframe in ("1h", "4h") and not user["vip"]:
        await callback.answer(msg(callback.from_user.id, "free_locked"), show_alert=True)
        return
    await send_coin_analysis(callback.from_user.id, symbol, timeframe=timeframe)
    await callback.answer()


@dp.callback_query_handler(lambda c: c.data == "add_fav")
async def add_fav_cb(callback: types.CallbackQuery):
    user = get_user(callback.from_user.id)
    last_coin = user.get("last_coin")
    limit = VIP_LIMIT if user["vip"] else FREE_LIMIT
    if not last_coin:
        await callback.answer("Спочатку вибери монету", show_alert=True)
        return
    if last_coin in user["favorites"]:
        await callback.answer(msg(callback.from_user.id, "already_listed"))
        return
    if len(user["favorites"]) >= limit:
        await callback.answer(msg(callback.from_user.id, "fav_limit", limit=limit), show_alert=True)
        return
    user["favorites"].append(last_coin)
    save_users()
    await callback.answer(msg(callback.from_user.id, "added_fav"))


@dp.message_handler(lambda m: m.text == "⭐ Обрані")
async def favorites_cmd(message: types.Message):
    user = get_user(message.from_user.id)
    if not user["favorites"]:
        await message.answer(msg(message.from_user.id, "favorites_empty"))
        return
    text = msg(message.from_user.id, "favorites_title") + "\n\n" + "\n".join(f"• `{coin}`" for coin in user["favorites"])
    await message.answer(text, parse_mode="Markdown", reply_markup=favorites_menu_inline(user["favorites"]))


@dp.callback_query_handler(lambda c: c.data.startswith("remove_fav_"))
async def remove_favorite(callback: types.CallbackQuery):
    coin = callback.data.split("_", 2)[2]
    user = get_user(callback.from_user.id)
    if coin in user["favorites"]:
        user["favorites"].remove(coin)
        save_users()
    await callback.answer(msg(callback.from_user.id, "removed_fav"))
    if user["favorites"]:
        text = msg(callback.from_user.id, "favorites_title") + "\n\n" + "\n".join(f"• `{item}`" for item in user["favorites"])
        await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=favorites_menu_inline(user["favorites"]))
    else:
        await callback.message.edit_text(msg(callback.from_user.id, "favorites_empty"))


@dp.message_handler(lambda m: m.text == "👤 Профіль")
async def profile_cmd(message: types.Message):
    user = get_user(message.from_user.id)
    text = msg(
        message.from_user.id,
        "profile",
        id=message.from_user.id,
        vip="💎 VIP" if user_is_vip(message.from_user.id) else "Free",
        vip_until=format_vip_until(message.from_user.id),
        auto="✅" if user["auto"] else "❌",
        interval=interval_label(user["interval"]),
        lang=user["lang"].upper(),
        fav_count=len(user["favorites"]),
        alert_count=len(user["alerts"]),
        history_count=len(user["history"]),
    )
    await message.answer(text, parse_mode="Markdown")


@dp.message_handler(lambda m: m.text == "🌍 Настрій ринку")
async def market_mood_cmd(message: types.Message):
    mood = market_mood()
    if not mood:
        await message.answer(msg(message.from_user.id, "no_data"))
        return
    trend_key = {
        "bull": "trend_bull",
        "bear": "trend_bear",
        "flat": "trend_flat",
    }[mood["trend"]]
    await message.answer(
        f"{msg(message.from_user.id, 'market_mood')}\n\n"
        f"📊 Avg 24h: `{mood['avg']:+.2f}%`\n"
        f"🧭 Trend: *{msg(message.from_user.id, trend_key)}*",
        parse_mode="Markdown",
    )


@dp.message_handler(lambda m: m.text == "🔥 Топ рухів")
async def top_market_cmd(message: types.Message):
    movers = market_movers()
    if not movers:
        await message.answer(msg(message.from_user.id, "no_data"))
        return
    lines = [msg(message.from_user.id, "top_market"), ""]
    free_mode = not user_is_vip(message.from_user.id)
    visible = movers[:6] if free_mode else movers[:12]
    for item in visible:
        icon = "🟢" if item["change_percent"] >= 0 else "🔴"
        lines.append(f"{icon} `{item['symbol']}`  `{item['change_percent']:+.2f}%`")
    if free_mode:
        lines.append("")
        lines.append(msg(message.from_user.id, "free_hint"))
    await message.answer("\n".join(lines), parse_mode="Markdown")


@dp.message_handler(lambda m: m.text == "🔔 Алерт")
async def alert_cmd(message: types.Message):
    if not user_is_vip(message.from_user.id):
        await message.answer(msg(message.from_user.id, "only_vip"))
        return
    user = get_user(message.from_user.id)
    user["awaiting_alert"] = True
    save_users()
    await message.answer(msg(message.from_user.id, "alert_format"), parse_mode="Markdown")


@dp.callback_query_handler(lambda c: c.data.startswith("prepare_alert_"))
async def prepare_alert(callback: types.CallbackQuery):
    if not user_is_vip(callback.from_user.id):
        await callback.answer(msg(callback.from_user.id, "only_vip"), show_alert=True)
        return
    symbol = callback.data.split("_", 2)[2]
    user = get_user(callback.from_user.id)
    user["last_coin"] = symbol
    user["awaiting_alert"] = True
    save_users()
    await bot.send_message(callback.from_user.id, f"Надішли ціну для `{symbol}` у форматі:\n`{symbol} 70000`", parse_mode="Markdown")
    await callback.answer("Очікую ціну")


@dp.message_handler(lambda m: get_user(m.from_user.id).get("awaiting_alert") is True)
async def alert_input(message: types.Message):
    user = get_user(message.from_user.id)
    parts = message.text.upper().replace(",", ".").split()
    if len(parts) != 2:
        await message.answer(msg(message.from_user.id, "invalid_alert"), parse_mode="Markdown")
        return
    symbol, value = parts
    try:
        target_price = float(value)
    except ValueError:
        await message.answer(msg(message.from_user.id, "invalid_alert"), parse_mode="Markdown")
        return
    if symbol not in VIP_COINS:
        await message.answer(msg(message.from_user.id, "invalid_alert"), parse_mode="Markdown")
        return
    user["alerts"][symbol] = target_price
    user["awaiting_alert"] = False
    save_users()
    await message.answer(msg(message.from_user.id, "alert_set", coin=symbol, price=target_price), parse_mode="Markdown")


@dp.message_handler(lambda m: m.text == "🤖 Auto Signals")
async def auto_cmd(message: types.Message):
    if not user_is_vip(message.from_user.id):
        await message.answer(msg(message.from_user.id, "only_vip"))
        return
    user = get_user(message.from_user.id)
    await message.answer(msg(message.from_user.id, "auto_settings"), reply_markup=auto_menu(user))


@dp.message_handler(lambda m: m.text in ["▶️ Увімкнути", "⏹ Вимкнути"])
async def auto_toggle(message: types.Message):
    if not user_is_vip(message.from_user.id):
        await message.answer(msg(message.from_user.id, "only_vip"))
        return
    user = get_user(message.from_user.id)
    user["auto"] = message.text == "▶️ Увімкнути"
    save_users()
    await message.answer(msg(message.from_user.id, "auto_on" if user["auto"] else "auto_off"))


@dp.message_handler(lambda m: m.text in ["⏱ 10 хв", "⏱ 15 хв", "⏱ 30 хв", "⏱ 1 година", "⏱ 2 години", "⏱ 4 години"])
async def auto_time(message: types.Message):
    if not user_is_vip(message.from_user.id):
        await message.answer(msg(message.from_user.id, "only_vip"))
        return
    user = get_user(message.from_user.id)
    mapping = {
        "⏱ 10 хв": AUTO_INTERVAL_OPTIONS["10m"],
        "⏱ 15 хв": AUTO_INTERVAL_OPTIONS["15m"],
        "⏱ 30 хв": AUTO_INTERVAL_OPTIONS["30m"],
        "⏱ 1 година": AUTO_INTERVAL_OPTIONS["1h"],
        "⏱ 2 години": AUTO_INTERVAL_OPTIONS["2h"],
        "⏱ 4 години": AUTO_INTERVAL_OPTIONS["4h"],
    }
    user["interval"] = mapping[message.text]
    save_users()
    await message.answer(msg(message.from_user.id, "auto_time_set", interval=interval_label(user["interval"])))


@dp.message_handler(lambda m: m.text == "🧠 VIP Сканер")
async def vip_scanner_cmd(message: types.Message):
    if not user_is_vip(message.from_user.id):
        await message.answer(msg(message.from_user.id, "only_vip"))
        return
    report = run_vip_scanner(message.from_user.id)
    await message.answer(report, parse_mode="Markdown")


@dp.message_handler(lambda m: m.text == "📈 Top BUY")
async def top_buy_cmd(message: types.Message):
    if not user_is_vip(message.from_user.id):
        await message.answer(msg(message.from_user.id, "only_vip"))
        return
    await message.answer(run_directional_scanner(message.from_user.id, "buy"), parse_mode="Markdown")


@dp.message_handler(lambda m: m.text == "📉 Top SELL")
async def top_sell_cmd(message: types.Message):
    if not user_is_vip(message.from_user.id):
        await message.answer(msg(message.from_user.id, "only_vip"))
        return
    await message.answer(run_directional_scanner(message.from_user.id, "sell"), parse_mode="Markdown")


@dp.message_handler(lambda m: m.text == "🗂 Історія")
async def history_cmd(message: types.Message):
    if not user_is_vip(message.from_user.id):
        await message.answer(msg(message.from_user.id, "only_vip"))
        return
    await message.answer(format_history(message.from_user.id), parse_mode="Markdown")


@dp.message_handler(lambda m: m.text == "💎 VIP")
async def vip_info(message: types.Message):
    user = get_user(message.from_user.id)
    if user_is_vip(message.from_user.id):
        await message.answer(msg(message.from_user.id, "vip_already"))
        return
    await message.answer(msg(message.from_user.id, "vip_buy_info"), parse_mode="Markdown", reply_markup=vip_menu_inline(user))


@dp.callback_query_handler(lambda c: c.data == "buy_vip")
async def buy_vip(callback: types.CallbackQuery):
    user = get_user(callback.from_user.id)
    if user_is_vip(callback.from_user.id):
        await callback.answer(msg(callback.from_user.id, "vip_already"), show_alert=True)
        return
    invoice = create_vip_invoice(callback.from_user.id)
    if not invoice or not invoice.get("invoice_id") or not invoice.get("invoice_url"):
        await callback.answer(msg(callback.from_user.id, "invoice_error"), show_alert=True)
        return
    user["invoice_id"] = invoice["invoice_id"]
    user["invoice_url"] = invoice["invoice_url"]
    save_users()
    await bot.send_message(
        callback.from_user.id,
        f"{msg(callback.from_user.id, 'payment_caption')}\n\n{msg(callback.from_user.id, 'vip_created')}",
        parse_mode="Markdown",
        reply_markup=payment_inline(invoice["invoice_url"]),
    )
    await callback.answer("Рахунок створено")


@dp.callback_query_handler(lambda c: c.data == "buy_vip_stars_week")
async def buy_vip_stars_week(callback: types.CallbackQuery):
    if user_is_vip(callback.from_user.id):
        await callback.answer(msg(callback.from_user.id, "vip_already"), show_alert=True)
        return
    await bot.send_invoice(
        callback.from_user.id,
        title="VIP Week Access",
        description="Weekly VIP access for Crypto AI Signal Bot",
        provider_token="",
        currency="XTR",
        prices=[types.LabeledPrice(label="VIP Week", amount=VIP_WEEK_STARS)],
        start_parameter="vip-stars-week",
        payload=f"vip_week:{callback.from_user.id}",
    )
    await callback.answer(msg(callback.from_user.id, "stars_invoice_sent"))


@dp.pre_checkout_query_handler(lambda q: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@dp.message_handler(content_types=types.ContentTypes.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    payment = message.successful_payment
    if payment.currency == "XTR" and payment.invoice_payload.startswith("vip_week:"):
        await activate_vip(message.from_user.id, days=7)
        await message.answer(msg(message.from_user.id, "stars_week_activated"))


@dp.callback_query_handler(lambda c: c.data == "check_vip_payment")
async def check_vip_payment(callback: types.CallbackQuery):
    user = get_user(callback.from_user.id)
    if not user.get("invoice_id"):
        await callback.answer("Активного рахунку немає", show_alert=True)
        return
    invoice = get_invoice_status(user["invoice_id"])
    if not invoice:
        await callback.answer(msg(callback.from_user.id, "invoice_error"), show_alert=True)
        return
    status = invoice.get("status")
    if status == "paid":
        await activate_vip(callback.from_user.id)
        await callback.answer("VIP активовано", show_alert=True)
    elif status == "active":
        await callback.answer(msg(callback.from_user.id, "invoice_wait"), show_alert=True)
    else:
        user["invoice_id"] = None
        user["invoice_url"] = None
        save_users()
        await callback.answer(msg(callback.from_user.id, "invoice_expired"), show_alert=True)


@dp.message_handler(lambda m: m.text == "🔙 Назад")
async def back_cmd(message: types.Message):
    await message.answer(msg(message.from_user.id, "main_menu"), reply_markup=main_menu(get_user(message.from_user.id)))


async def background_loop():
    while True:
        now = time.time()
        for uid, user in list(users.items()):
            if user.get("invoice_id") and not user_is_vip(uid):
                try:
                    invoice = get_invoice_status(user["invoice_id"])
                    if invoice and invoice.get("status") == "paid":
                        await activate_vip(uid)
                except Exception:
                    pass

            alerts_to_remove = []
            for coin, target in user.get("alerts", {}).items():
                price = get_price(coin)
                if price and price >= float(target):
                    try:
                        await bot.send_message(uid, msg(uid, "price_alert", coin=coin, price=target), parse_mode="Markdown")
                    except Exception:
                        pass
                    alerts_to_remove.append(coin)
            for coin in alerts_to_remove:
                user["alerts"].pop(coin, None)

            if user_is_vip(uid) and user.get("auto") and user.get("interval", 0) > 0:
                if now - user.get("last_signal", 0) >= user["interval"]:
                    favorites = user.get("favorites") or ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
                    for coin in favorites[:5]:
                        try:
                            signal_data = calc_signal_data(coin, interval="15m")
                            if not signal_data:
                                continue
                            ticker = ticker_24h(coin) or {"change_percent": 0}
                            text = (
                                f"🤖 *AUTO SIGNAL*\n"
                                f"`{coin}` {signal_data['signal']}\n"
                                f"💪 Strength `{signal_data['strength']}`\n"
                                f"⚠️ Risk `{signal_data['risk']}`\n"
                                f"📈 RSI `{signal_data['rsi']}`\n"
                                f"🕒 24h `{ticker['change_percent']:+.2f}%`"
                            )
                            await bot.send_message(uid, text, parse_mode="Markdown")
                            save_signal_history(uid, coin, "15m", signal_data)
                        except Exception:
                            pass
                    user["last_signal"] = now
                    save_users()
        if users:
            save_users()
        await asyncio.sleep(30)


if __name__ == "__main__":
    load_users()
    loop = asyncio.get_event_loop()
    loop.create_task(background_loop())
    executor.start_polling(dp, skip_updates=True)
