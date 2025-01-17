import telebot
from faker import Faker
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random

# Создаем объект Faker для генерации номеров кредитных карт
fake = Faker()

# Токен вашего бота (получите его у @BotFather)
TOKEN = '7922612476:AAHDXqtZZgwvRtmmFich5FgMB-BPOznI5DI'

# Идентификатор стикера
STICKER_ID = 'CAACAgUAAxkBAAN1Z4p1GRXM4XeSzvPvqryo9G4YruMAAnADAALpCsgD1gZUND89raQ2BA'

# Инициализируем бота
bot = telebot.TeleBot(TOKEN)

def generate_unionpay_card():
    """Генератор номера карты UnionPay"""
    # Номер карты UnionPay начинается с 62
    prefix = '62'
    return prefix + ''.join(str(random.randint(0, 9)) for _ in range(14))

def generate_jcb_card():
    """Генератор номера карты JCB"""
    # Номер карты JCB начинается с 3528...35
    prefix = '3528'
    return prefix + ''.join(str(random.randint(0, 9)) for _ in range(11))

def generate_maestro_card():
    """Генератор номера карты Maestro"""
    # Номер карты Maestro начинается с 50...55, 56...58, 60...69
    prefixes = ['5018', '5020', '5038', '5612', '5893', '6304']
    prefix = random.choice(prefixes)
    return prefix + ''.join(str(random.randint(0, 9)) for _ in range(10))

def generate_mir_card():
    """Генератор номера карты МИР"""
    # Номер карты МИР начинается с 2200...22
    prefix = '2200'
    return prefix + ''.join(str(random.randint(0, 9)) for _ in range(12))

def create_keyboard():
    """Создаём клавиатуру с кнопками выбора карт"""
    markup = InlineKeyboardMarkup(row_width=3)
    mastercard_button = InlineKeyboardButton('MasterCard 🇺🇳', callback_data='mastercard')
    visa_button = InlineKeyboardButton('Visa 🇺🇸', callback_data='visa')
    mir_button = InlineKeyboardButton('Мир 🇷🇺', callback_data='mir')
    jcb_button = InlineKeyboardButton('JCB 🇯🇵', callback_data='jcb')
    maestro_button = InlineKeyboardButton('Maestro 🌎', callback_data='maestro')
    unionpay_button = InlineKeyboardButton('UnionPay 🇹🇷', callback_data='unionpay')
    markup.row(mastercard_button, visa_button, mir_button)
    markup.row(jcb_button, maestro_button, unionpay_button)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_msg = "Привет! Я сгенерирую для тебя номер тестовой банковской карты🤙"
    bot.send_sticker(message.chat.id, STICKER_ID)
    bot.send_message(message.chat.id, welcome_msg)
    
    keyboard = create_keyboard()
    bot.send_message(
        message.chat.id,
        "Выберите тип карты:",
        reply_markup=keyboard
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == 'mastercard':
        card_number = fake.credit_card_number(card_type="mastercard")
    elif call.data == 'visa':
        card_number = fake.credit_card_number(card_type="visa")
    elif call.data == 'mir':
        card_number = generate_mir_card()
    elif call.data == 'jcb':
        card_number = generate_jcb_card()
    elif call.data == 'maestro':
        card_number = generate_maestro_card()
    elif call.data == 'unionpay':
        card_number = generate_unionpay_card()
        
    bot.send_message(
        call.message.chat.id,
        f"Вот ваш номер карты: {card_number}"
    )
    
    keyboard = create_keyboard()
    bot.send_message(
        call.message.chat.id,
        "Выберите ещё одну карту:",
        reply_markup=keyboard
    )

if __name__ == '__main__':
    bot.polling(none_stop=True)