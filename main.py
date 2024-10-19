import telebot
import random
from datetime import datetime

API_TOKEN = 'введите токен'

bot = telebot.TeleBot(API_TOKEN)

quiz_questions = [
    {
        "question": "Какой самый большой океан на земле?",
        "options": ["Атлантический", "Индийский", "Тихий", "Северный ледовитый"],
        "answer": 2
    },
    {
        "question": "Какой планете Солнечной системы соответствует римский бог войны?",
        "options": ["Меркурий", "Венера", "Марс", "Юпитер"],
        "answer": 2
    }
]