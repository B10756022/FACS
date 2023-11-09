from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import FlexSendMessage,VideoSendMessage, ImageSendMessage, MessageEvent, TextSendMessage, UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, MemberLeftEvent, MemberJoinedEvent, PostbackEvent

import json

#共用
from fish_app import *

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        # 先設定一個要回傳的message空集合
        #message = []
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        # 在這裡將body寫入機器人回傳的訊息中，可以更容易看出你收到的webhook長怎樣#
        #message.append(TextSendMessage(text=str(body)))
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            #回傳文字訊息
            if isinstance(event, MessageEvent):
                message = []
            #好友資料
                uid = event.source.user_id

                print(event.message.type)
                if event.message.type == 'text':
                    mtext = event.message.text
                    #message.append(TextSendMessage(text='文字訊息'))
                    #line_bot_api.reply_message(event.reply_token, message)

                    if mtext == '會員登入':

                        # 將JSON設定為變數content，並以FlexSendMessage()包成Flex Message
                        link_token_response = line_bot_api.issue_link_token(uid)

                        content = {
                                  "type": "bubble",
                                  "body": {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                      {
                                        "type": "text",
                                        "text": "尚未綁定帳號",
                                        "align": "center"
                                      }
                                    ]
                                  },
                                  "footer": {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                      {
                                        "type": "button",
                                        "action": {
                                          "type": "uri",
                                          "label": "綁定帳號",
                                          "uri": "https://eb8e-180-177-251-31.ngrok.io/login?linkToken="+link_token_response.link_token#隨時更新
                                        }
                                      }
                                    ]
                                  }
                                }
                        message = FlexSendMessage(alt_text='綁定帳號', contents=content)

                        line_bot_api.reply_message(event.reply_token, message)
                    elif mtext == '影像辨識':
                        message.append(TextSendMessage(text='已經準備好了！'))
                        line_bot_api.reply_message(event.reply_token, message)
                    elif mtext == '影片介面':
                        line_bot_api.reply_message(event.reply_token, message)
                    elif mtext == '複製成果':
                        #記得&&暫存數字不為0，辨識前須清空
                        line_bot_api.reply_message(event.reply_token, message)


                elif event.message.type == 'video':
                    video_content = line_bot_api.get_message_content(event.message.id)
                    path = r'../upload_media/'
                    with open(path, 'wb') as fd:
                        for chunk in video_content.iter_content():
                            fd.write(chunk)
                    message.append(TextSendMessage(text='影片處理完畢'))
                    # 設定圖片路徑
                    domain = 'https://aefe-180-177-251-31.ngrok.io'  # 隨時更改
                    gray = domain + gray[1:]
                    binary = domain + binary[1:]
                    message.append(ImageSendMessage(original_content_url=gray, preview_image_url=gray))
                    message.append(ImageSendMessage(original_content_url=binary, preview_image_url=binary))
                    line_bot_api.reply_message(event.reply_token, message)
            #     elif event.message.type == 'location':
            #         message.append(TextSendMessage(text='位置訊息'))
            #         line_bot_api.reply_message(event.reply_token, message)
            #

            #     elif event.message.type == 'sticker':
            #         message.append(TextSendMessage(text='貼圖訊息'))
            #         line_bot_api.reply_message(event.reply_token, message)
            #
            #     elif event.message.type == 'audio':
            #         message.append(TextSendMessage(text='聲音訊息'))
            #         line_bot_api.reply_message(event.reply_token, message)
            #
            #     elif event.message.type == 'file':
            #         message.append(TextSendMessage(text='檔案訊息'))
            #         line_bot_api.reply_message(event.reply_token, message)
            #     #line_bot_api.reply_message(event.reply_token, message)
            # elif isinstance(event, FollowEvent):
            #     print('加入好友')
            #     line_bot_api.reply_message(event.reply_token, message)
            #
            # elif isinstance(event, UnfollowEvent):
            #     print('取消好友')
            #
            # elif isinstance(event, JoinEvent):
            #     print('進入群組')
            #     line_bot_api.reply_message(event.reply_token, message)
            #
            # elif isinstance(event, LeaveEvent):
            #     print('離開群組')
            #     line_bot_api.reply_message(event.reply_token, message)
            #
            # elif isinstance(event, MemberJoinedEvent):
            #     print('有人入群')
            #     line_bot_api.reply_message(event.reply_token, message)
            #
            # elif isinstance(event, MemberLeftEvent):
            #     print('有人退群')
            #     line_bot_api.reply_message(event.reply_token, message)
            #
            # elif isinstance(event, PostbackEvent):
            #     print('PostbackEvent')
        return HttpResponse()
    else:
        return HttpResponseBadRequest()