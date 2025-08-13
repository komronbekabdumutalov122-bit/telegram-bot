import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# 3 ta adminning Telegram ID’lari
ADMINS = [8194221675, 222222222, 333333333]  # <-- o'z IDlaringizni qo'ying
# Hodimlar ro‘yxati (Telegram ID)
EMPLOYEES = [7570338476, 555555555]  # <-- o'z hodimlaringizni qo'shing

# MoySklad API ma'lumotlari
MOYSKLAD_LOGIN = "abdumutalov@forge-group"
MOYSKLAD_PASSWORD = "122Komronbek"

# Ruxsatni tekshiruvchi funksiya
def check_access(user_id):
    if user_id in ADMINS:
        return "admin"
    elif user_id in EMPLOYEES:
        return "employee"
    else:
        return None

# Start buyrug‘i
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    role = check_access(user_id)

    if role == "admin":
        await update.message.reply_text("✅ Salom, ADMIN!\nQoldiq uchun /ostatki buyrug‘ini ishlating.")
    elif role == "employee":
        await update.message.reply_text("✅ Salom, Hodim!\nQoldiq uchun /ostatki buyrug‘ini ishlating.")
    else:
        await update.message.reply_text("⛔ Sizga bu botdan foydalanish ruxsati yo‘q.")

# MoySklad’dan qoldiq olish
def get_moysklad_stock():
    url = "https://online.moysklad.ru/app/#stockReport?reportType=STORES"
    response = requests.get(url, auth=(MOYSKLAD_LOGIN, MOYSKLAD_PASSWORD))
    if response.status_code == 200:
        data = response.json()
        results = []
        for item in data.get('rows', []):
            name = item.get('name', 'Noma’lum')
            quantity = item.get('quantity', 0)
            results.append(f"{name} — {quantity}")
        return "\n".join(results) if results else "📭 Qoldiq topilmadi."
    else:
        return f"❌ Xato: {response.status_code}"

# /ostatki buyrug‘i
async def ostatki(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    role = check_access(user_id)

    if role in ["admin", "employee"]:
        await update.message.reply_text("⏳ Qoldiqlar yuklanmoqda...")
        stock_data = get_moysklad_stock()
        await update.message.reply_text(stock_data)
    else:
        await update.message.reply_text("⛔ Sizga bu buyruqni ishlatish ruxsati yo‘q.")

# Botni ishga tushirish
def main():
    TOKEN = "8278628485:AAHyivU1jG7cg3PY6DaM2kDG1g4YWQ7EkQA"  # BotFather tokeni
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ostatki", ostatki))

    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
