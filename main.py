from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, FlexSendMessage
import json

app = Flask(__name__)

line_bot_api = LineBotApi("05vHrRwgpz49TjqDB1PGlBkuSWobIkosX9n0K3IhGOX7FwmIr1e3ZYSTQ08/MwKbu+6CbyCD+ZPIQyT/moS8dkfM/YnR/9bpB5Bnd6iROCSWvXaTo8Q78DIXTQA4yzb/cglXNWyVYlQ3sKClqI2r9gdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("e59fcd3fb17e68ed4f33ed740889dfa2")

flex_message = {
  "type": "bubble",
  "size": "kilo",
  "hero": {
    "type": "image",
    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
    "size": "full",
    "aspectRatio": "16:3.5",
    "aspectMode": "cover"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "🔔 อัพเดทธีมล่าสุด",
        "weight": "bold",
        "wrap": True,
        "align": "center",
        "color": "#1A3C5E",
        "size": "lg"
      },
      {
        "type": "separator",
        "margin": "sm",
        "color": "#D0D8E4"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "md",
        "contents": [
          {
            "type": "button",
            "action": {"type": "uri", "label": "🌐 ธีมต่างประเทศ", "uri": "https://store.line.me"},
            "style": "primary", "height": "sm", "color": "#1A3C5E"
          },
          {
            "type": "button",
            "action": {"type": "uri", "label": "🎨 ธีมจากครีเอเตอร์", "uri": "https://creator.line.me"},
            "style": "primary", "height": "sm", "margin": "md", "color": "#2E6DA4"
          },
          {
            "type": "button",
            "action": {"type": "uri", "label": "📢 แชร์ให้เพื่อน", "uri": "https://google.com"},
            "style": "primary", "margin": "md", "height": "sm", "color": "#4A90D9"
          }
        ]
      }
    ],
    "paddingAll": "12px"
  }
}

@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text.lower()
    if "ธีม" in text:
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text="อัพเดทธีม LINE ล่าสุด",
                contents=FlexSendMessage.new_from_json_dict(flex_message),
                sender={"name": "LINE Theme Center 📋", "iconUrl": "https://video-public.canva.com/VAEQmJMm6R8/v/a372d097e3.gif"},
                quick_reply={"items": [
                    {"type": "action", "imageUrl": "https://video-public.canva.com/VADhwZBf_RY/v/0d1c3ca5c8.gif",
                     "action": {"type": "uri", "label": "ธีมทางการใหม่", "uri": "https://line.me/R/shop/theme/showcase?id=new"}},
                    {"type": "action", "imageUrl": "https://media-public.canva.com/M7NGs/MAEwAnM7NGs/1/tl.png",
                     "action": {"type": "uri", "label": "สั่งซื้อ iton5", "uri": "line://nv/profilePopup/mid=ufb9d34cac39cc328b9febede9f106341"}}
                ]}
            )
        )

if __name__ == "__main__":
    app.run(port=5000)