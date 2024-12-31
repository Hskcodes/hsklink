import cloudscraper
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
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
    service = Service("path/to/chromedriver")  # Replace with your ChromeDriver path
    return webdriver.Chrome(service=service, options=chrome_options)

# Bypass functions
def cloudscraper_bypass(url):
    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url)
        if response.status_code == 200:
            return f"Bypassed URL: {response.url}"
        else:
            return f"Failed to bypass, status code: {response.status_code}"
    except Exception as e:
        return f"CloudScraper Error: {e}"

def selenium_bypass(url):
    try:
        driver = setup_selenium()
        driver.get(url)
        time.sleep(5)  # Wait for JavaScript to load
        final_url = driver.current_url
        driver.quit()
        return f"Bypassed URL: {final_url}"
    except Exception as e:
        return f"Selenium Error: {e}"

# Dynamic URL bypass
def bypass_url(url):
    for website, method in bypass_methods.items():
        if website in url:
            if method == "cloudscraper":
                return cloudscraper_bypass(url)
            elif method == "selenium":
                return selenium_bypass(url)
    return "Yeh website abhi supported nahi hai. /addwebsite command use karein."

# Command to add a new website
def add_website(update, context):
    try:
        args = context.args
        if len(args) != 2:
            update.message.reply_text("Usage: /addwebsite <website> <method>\nExample: /addwebsite ouo.io cloudscraper")
            return

        website, method = args
        if method not in ["cloudscraper", "selenium"]:
            update.message.reply_text("Supported methods: cloudscraper, selenium")
            return

        bypass_methods[website] = method
        update.message.reply_text(f"Website {website} added with method {method}!")
    except Exception as e:
        update.message.reply_text(f"Error: {e}")

# Command to list supported websites
def list_websites(update, context):
    if not bypass_methods:
        update.message.reply_text("Koi website abhi tak add nahi hui.")
        return

    message = "Supported Websites:\n"
    for website, method in bypass_methods.items():
        message += f"- {website}: {method}\n"
    update.message.reply_text(message)

# Start command
def start(update, context):
    update.message.reply_text("Assalam o Alaikum! Mujh se supported links bypass karwane ke liye link bhejein.\n"
                              "Nayi websites add karne ke liye /addwebsite command use karein.")

# Handle URLs
def handle_message(update, context):
    url = update.message.text
    result = bypass_url(url)
    update.message.reply_text(result)

# Main function
def main():
    TOKEN = "6934514903:AAHLVkYqPEwyIZiyqEhJocOrjDYwTk9ue8Y"
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("addwebsite", add_website))
    dp.add_handler(CommandHandler("listwebsites", list_websites))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
