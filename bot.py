import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ===== CONFIG =====
TELEGRAM_BOT_TOKEN = "5060780668:AAFMl_ORaP8o75IYiXvTg17EztdLYFhltqA"
OPENAI_API_KEY = "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"

openai.api_key = OPENAI_API_KEY

# ===== COMMANDS =====

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "Use:\n"
        "/image <description>\n\n"
        "Example:\n"
        "/image a cyberpunk cat with neon lights"
    )

async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)

    if not prompt:
        await update.message.reply_text("❌ Please provide a prompt.\nExample:\n/image a flying car")
        return

    msg = await update.message.reply_text("🎨 Generating image...")

    try:
        response = openai.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024"
        )

        image_url = response.data[0].url

        await update.message.reply_photo(photo=image_url, caption=f"🖼 Prompt:\n{prompt}")
        await msg.delete()

    except Exception as e:
        await msg.edit_text(f"❌ Error:\n{str(e)}")

# ===== MAIN =====

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("image", image))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
  
