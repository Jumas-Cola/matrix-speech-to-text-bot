import simplematrixbotlib as botlib
from nio import RoomMessageAudio
import os
import uuid
from services.speech2text import Speech2Text
from dotenv import load_dotenv

load_dotenv()

creds = botlib.Creds(
    os.getenv("HOME_SERVER"), os.getenv("LOGIN"), os.getenv("PASSWORD")
)
bot = botlib.Bot(creds)

folder_name = "audios"

os.makedirs(folder_name, exist_ok=True)


@bot.listener.on_custom_event(RoomMessageAudio)
async def recognize_audio(room, message):
    mxc = message.url
    filename = f"audiomessage-{uuid.uuid4()}.ogg"
    resp = await bot.async_client.download(mxc=mxc, filename=filename)

    file_path = f"{folder_name}/{filename}"

    with open(file_path, "wb") as f:
        f.write(resp.body)

    text = ""
    try:
        s2t = Speech2Text()
        text = s2t.recognize(f"audios/{filename}")
        os.remove(file_path)
    except Exception as e:
        raise e
        text = "Ошибка распознавания аудио ⚠️"

    await bot.api.send_text_message(room.room_id, text, reply_to=message.event_id)


bot.run()
