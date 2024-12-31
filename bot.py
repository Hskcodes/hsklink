import cloudscraper
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import time

# Dictionary to store website bypass methods
bypass_methods = {
    "inshorturl.com": "cloudscraper",
    "adf.ly": "selenium"
}

# Setup for Selenium
def setup_selenium():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service("/usr/local/bin/chromedriver")  # Replace with your ChromeDriver path
    return webdriver.Chrome(service=service, options=chrome_options)

# Bypass functions
def cloudscraper_bypass(url):
    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url)
        if response.status_code == 200:
            return f"✅ Bypassed URL: {response.url}"
        else:
            return f"❌ Failed to bypass, status code: {response.status_code}"
    except Exception as e:
        return f"⚠️ CloudScraper Error: {e}"

def selenium_bypass(url):
    try:
        driver = setup_selenium()
        driver.get(url)
        time.sleep(5)  # Wait for JavaScript to load
        final_url = driver.current_url
        driver.quit()
        return f"✅ Bypassed URL: {final_url}"
    except Exception as e:
        return f"⚠️ Selenium Error: {e}"

# Dynamic URL bypass
def bypass_url(url):
    for website, method in bypass_methods.items():
        if website in url:
            if method == "cloudscraper":
                return cloudscraper_bypass(url)
            elif method == "selenium":
                return selenium_bypass(url)
    return "🚫 Yeh website abhi supported nahi hai. /addwebsite command use karein."

# Command to add a new website
async def add_website(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if len(args) != 2:
            await update.message.reply_text("🛠️ Usage: /addwebsite <website> <method>\nExample: /addwebsite ouo.io cloudscraper")
            return

        website, method = args
        if method not in ["cloudscraper", "selenium"]:
            await update.message.reply_text("🤖 Supported methods: cloudscraper, selenium")
            return

        bypass_methods[website] = method
        await update.message.reply_text(f"🌐 Website {website} added with method {method}!")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")

# Command to list supported websites
async def list_websites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not bypass_methods:
        await update.message.reply_text("🔍 Koi website abhi tak add nahi hui.")
        return

    message = "🌐 Supported Websites:\n"
    for website, method in bypass_methods.items():
        message += f"- {website}: {method}\n"
    await update.message.reply_text(message)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Assalam o Alaikum! Mujh se supported links bypass karwane ke liye link bhejein.\n"
        "➕ Nayi websites add karne ke liye /addwebsite command use karein."
    )

# Handle URLs
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    result = bypass_url(url)
    await update.message.reply_text(result)

# Main function
def main():
    TOKEN = "6934514903:AAHLVkYqPEwyIZiyqEhJocOrjDYwTk9ue8Y"  # Your bot token
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("addwebsite", add_website))
    application.add_handler(CommandHandler("listwebsites", list_websites))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == "__main__":
    main()
