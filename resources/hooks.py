from flask import Flask, request, current_app
import json
import requests
import os
from . import bot
from .utilities import (import_questions, make_response, make_quiz_response, find_user, check_answers, get_index, send_carousel, send_postback_replies)

PAT = os.environ.get('PAT', None)
verify_token = os.environ.get('VERIFY_TOKEN', None)

letters = ["A", "B", "C", "D"]

answers = os.path.abspath("answers.txt")
quizzing = False

@bot.route('/', methods = ['GET'])
def worker_verification():
    if PAT is not None and verify_token is not None:
        if request.args.get('hub.verify_token', '') == verify_token:
            print("Verification successful!")
            return request.args.get('hub.challenge', '')
        else:
            print("Verification failed!")
            return 'Error, wrong validation token'
    else:
        return "Could not get verification tokens."

#idx = get_index()

@bot.route('/', methods = ['POST'])
def worker_messaging():
    global quizzing
    try:
        messages = request.get_json()
        if messages['object'] == 'page':
            for message in messages['entry']:
                for msg in message['messaging']:
                    print(msg)
                    idx = get_index()
                    if (msg.get('message')) or  (msg.get('postback')):
                        sender_id = msg['sender']['id']
                        user = find_user(sender_id, PAT)

                        if (msg.get('message', None)):
                            received = msg['message']
                            if (received.get('quick_reply', None)):
                                txt = received['quick_reply']['payload']
                                print(txt)
                                if txt == 'quiz':
                                    quizzing = True
                                    print("Creating quiz!")
                                    make_quiz_response(sender_id, idx, PAT)
                                elif txt in letters:
                                    score = check_answers(idx, txt)

                                    with open(answers, "a") as store:
                                        print("Write to file %d", score)
                                        line = '{} {}\n'.format(txt, score)
                                        store.write(line)
                                        store.close()
                                    with open(answers, "r") as xx:
                                        lines = xx.readlines()
                                        print(lines)
                                    #print(answers)
                                    make_quiz_response(sender_id, idx, PAT)
                                elif txt == 'guides':
                                    send_postback_replies(
                                        sender_id,
                                        "Here are a few steps to follow to get ready to export to the US",
                                        [
                                            {
                                                "type": "web_url",
                                                "url": "f8-2019.firebaseapp.com/guide",
                                                "title": "Open the guide",
                                                "webview_height_ratio": "tall",
                                                "messenger_extensions": "false",
                                                "fallback_url": "agoa.org"
                                            }]
                                        )
                                elif txt == 'categories':
                                    send_carousel(sender_id,
                                                  [
                                                      {
                                                          "title": "Apparel Manufacturing",
                                                          "image_url": "https://agoa.info/images/articles/5183/_thumb4/southafrica_textileworker.jpg",
                                                        #   "subtitle": "We have the right hat for everyone.",
                                                          "default_action": {
                                                              "type": "web_url",
                                                              "url": "f8-2019.firebaseapp.com/regulations/apparel",
                                                              "webview_height_ratio": "tall",
                                                          },
                                                          "buttons": [
                                                              {
                                                                  "type": "web_url",
                                                                  "url": "f8-2019.firebaseapp.com/regulations/apparel",
                                                                  "title": "View regulations"
                                                              }
                                                          ]
                                                      },
                                                      {
                                                          "title": "Cashews",
                                                          "image_url": "https://agoa.info/images/articles/5183/_thumb4/southafrica_textileworker.jpg",
                                                        #   "subtitle": "We have the right hat for everyone.",
                                                          "default_action": {
                                                              "type": "web_url",
                                                              "url": "f8-2019.firebaseapp.com/regulations/cashew",
                                                              "webview_height_ratio": "tall",
                                                          },
                                                          "buttons": [
                                                              {
                                                                  "type": "web_url",
                                                                  "url": "f8-2019.firebaseapp.com/regulations/cashew",
                                                                  "title": "View regulations"
                                                              }
                                                          ]
                                                      },
                                                      {
                                                          "title": "Coffee",
                                                          "image_url": "https://agoa.info/images/articles/5156/_thumb4/coffee_tasters_ethiopia600_400.jpg",
                                                        #   "subtitle": "We have the right hat for everyone.",
                                                          "default_action": {
                                                              "type": "web_url",
                                                              "url": "https://f8-2019.firebaseapp.com/regulations/coffee",
                                                              "webview_height_ratio": "tall",
                                                          },
                                                          "buttons": [
                                                              {
                                                                  "type": "web_url",
                                                                  "url": "https://f8-2019.firebaseapp.com/regulations/coffee",
                                                                  "title": "View regulations"
                                                              }
                                                          ]
                                                      },
                                                      {
                                                          "title": "Foodstuff",
                                                          "image_url": "https://agoa.info/images/articles/6214/_thumb4/foodagoa.jpg",
                                                        #   "subtitle": "We have the right hat for everyone.",
                                                          "default_action": {
                                                              "type": "web_url",
                                                              "url": "https://f8-2019.firebaseapp.com/regulations/foodstuff",
                                                              "webview_height_ratio": "tall",
                                                          },
                                                          "buttons": [
                                                              {
                                                                  "type": "web_url",
                                                                  "url": "https://f8-2019.firebaseapp.com/regulations/foodstuff",
                                                                  "title": "View regulations"
                                                              }
                                                          ]
                                                      },
                                                      {
                                                          "title": "Textiles",
                                                          "image_url": "https://agoa.info/images/articles/5159/_thumb4/ethiopia_trad_textiles_collage_small.jpg",
                                                        #   "subtitle": "We have the right hat for everyone.",
                                                          "default_action": {
                                                              "type": "web_url",
                                                              "url": "https://f8-2019.firebaseapp.com/regulations/textiles",
                                                              "webview_height_ratio": "tall",
                                                          },
                                                          "buttons": [
                                                              {
                                                                  "type": "web_url",
                                                                  "url": "https://f8-2019.firebaseapp.com/regulations/textiles",
                                                                  "title": "View regulations"
                                                              }
                                                          ]
                                                      },
                                                  ]
                                                  )

                            else:
                                txt = received["text"]
                                if txt in letters and quizzing is True:
                                    score = check_answers(idx, txt)

                        if msg.get('postback'):
                            received = msg['postback']['payload']
                            if received == 'start':
                                make_response(sender_id, 'message', 'greeting', PAT)
                                make_response(sender_id, 'quick', 'introduction', PAT)
    except Exception as e:
        raise e

    return 'OK', 200

@bot.errorhandler(404)
def handle_error(ex):
    print(ex)
    print(request.url_rule.rule)


def make_quiz():
    quizzing = True
