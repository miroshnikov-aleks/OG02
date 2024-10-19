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

user_quiz_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать! Я ваш новый бот. Чем могу помочь?")

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "Я могу выполнять следующие команды:\n"
        "/start - Начать общение со мной\n"
        "/help - Получить список доступных команд\n"
        "/weather - Узнать текущую погоду\n"
        "/motivate - Получить мотивирующую цитату\n"
        "/quiz - Пройти викторину\n"
    )
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['weather'])
def send_weather(message):
    weather_info = "Сейчас солнечно, 25°C."
    bot.reply_to(message, f"Текущая погода: {weather_info}")

@bot.message_handler(commands=['motivate'])
def send_motivation(message):
    motivations = [
        "Верь в себя и все получится.",
        "Каждый день — это новый шанс.",
        "Ты способен на большее, чем думаешь.",
        "Смелость — это начало победы."
    ]
    bot.reply_to(message, random.choice(motivations))

@bot.message_handler(commands=['quiz'])
def start_quiz(message):
    if message.chat.id not in user_quiz_data:
        user_quiz_data[message.chat.id] = {
            "questions": random.sample(quiz_questions, 2),
            "current_question_index": 0,
            "correct_answers": 0
        }
    user_data = user_quiz_data[message.chat.id]
    send_next_question(message)

def send_next_question(message):
    user_data = user_quiz_data[message.chat.id]
    if user_data["current_question_index"] < len(user_data["questions"]):
        question =user_data["questions"][user_data["current_question_index"]]
        options = "\n".join([f"{i+1}. {option}" for i, option in enumerate(question["options"])])
        bot.send_message(message.chat.id, f"{question['question']}\n{options}")
    else:
        bot.send_message(message.chat.id, f"Вы ответили правильно на {user_data['correct_answers']} из 2 вопросов.")
        del user_quiz_data[message.chat.id]

@bot.message_handler(func=lambda message: message.chat.id in user_quiz_data)
def check_quiz_answer(message):
    user_data = user_quiz_data[message.chat.id]
    question = user_data["questions"][user_data["current_question_index"]]
    try:
        user_answer = int(message.text) - 1
        if user_answer == question["answer"]:
            bot.reply_to(message, "Правильно!")
            user_data["correct_answers"] += 1
        else:
            bot.reply_to(message, "Неверно.")
        user_data["current_question_index"] += 1
        send_next_question(message)
    except ValueError:
        bot.reply_to(message, "Пожалуйста, введите номер варианта ответа.")

bot.polling()