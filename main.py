import os
import logging
from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from PIL import Image, ImageDraw, ImageFont

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot Token
BOT_TOKEN = "7529913637:AAFr-E6m5HRQLwhCRGUZBhT9pUfzcwRnG4Q"

# Function to edit PSD (Using PIL for demonstration, replace with PSD processing lib)
def generate_logo(customer_name, color):
    template_path = "template.png"  # PSD file should be converted to PNG first
    output_path = f"output/{customer_name}_logo.png"
    
    img = Image.open(template_path)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 50)
    
    draw.text((100, 100), customer_name, fill=color, font=font)
    img.save(output_path)
    
    return output_path

# Start Command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("👋 Hi! Send your name & color for a customized logo! (Format: Name,Color)")

# Handle Messages
def handle_message(update: Update, context: CallbackContext):
    try:
        text = update.message.text
        name, color = text.split(",")
        name, color = name.strip(), color.strip()
        
        update.message.reply_text("🎨 Creating your logo... Please wait!")
        
        logo_path = generate_logo(name, color)
        
        with open(logo_path, "rb") as logo_file:
            update.message.reply_photo(photo=InputFile(logo_file))
        
        update.message.reply_text("✅ Here’s your customized logo! 🎉")
    except Exception as e:
        update.message.reply_text("❌ Error: Please send your name & color in the correct format (e.g., Dinesh,Red).")
        logger.error(f"Error processing request: {e}")

# Main Function
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

