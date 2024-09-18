import telebot
from telebot import types
from dotenv import load_dotenv
import os
import random
from gtm_model import get_class

load_dotenv()
TOKEN_TG = os.getenv('TOKEN_TG')
bot = telebot.TeleBot(TOKEN_TG)
texts = ['Посадить дерево.',
'Построить скворечник, синичник.',
'Повесить и своевременно наполнять кормушку, поилку для птиц.',
'Ездить волонтером на проекты по спасению, восстановлению, учету животных.',
'Поддерживать фонды помощи животным.',
'Реже пользоваться кондиционером.',
'Убавлять индивидуальное отопление.',
'Покупать энергосберегающие приборы.',
'Сажать деревья.',
'Выбрать электротранспорт.',
'Больше ездить на велосипеде и ходить пешком.',
'Сортировать мусор.',
'Раздавать и продавать ненужные вещи, уменьшая количество мусора.',
'Устраивать и посещать фримаркеты для обмена вещами.',
'Пустую пластиковую упаковку, остатки ткани и прочее пускать на поделки.',
'В походе ходить только по тропам.',
'Не повреждать и не рвать без нужды растения, не ломать ветки.',
'Не шуметь, не включать громкую музыку.',
'Не кормить диких животных.',
'Не трогать птиц, насекомых.',
'Не оставлять надписи на камнях и прочих природных объектах.',
'Для разведения костра использовать старые кострища.',
'Ненужный костер затушить и засыпать землей.',
'Не разводить костры там, где это запрещено.',
'Не использовать на природе бытовую химию.',
'Закапывать органические отходы. ',
'После отдыха на природе забирать с собой мусор.',
'Собирать мусор в любимых уголках отдыха - в одиночку или с коллективом единомышленников.',
'Отправиться волонтером на уборку мусора в популярных туристических местах.',
'Прививать детям и окружающим любовь к природе - как сделать это интересно и ненавязчиво, расскажем далее.']
random_text = random.choice(texts)

@bot.message_handler(commands=['start'])
def handle_start(mes):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttonGTM = types.KeyboardButton("Распознование мусора") 
    buttonZA = types.KeyboardButton("Актуальные эко-проблемы") 
    buttonVO = types.KeyboardButton("Полезные советы") 
    markup.add(buttonGTM, buttonZA)
    markup.add(buttonVO)
    bot.send_message(mes.chat.id, "Привет, я бот-эколог! Я помогу тебе сохранить планету!")
    bot.send_message(mes.chat.id, "Для того чтобы продожить общение используй кнопки", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def GTMmodel(message):
    if message.text == 'Распознование мусора':
        bot.send_message(message.chat.id, "Для того чтобы воспользоваться распозанием\nтебе необходимо прописать команду /gtm и следовать дальнейшим указаниям!")
    if message.text == 'Актуальные эко-проблемы':
        bot.send_message(message.chat.id, 'Согласно источнику, к наиболее актуальным экологическим проблемам современности относятся:\n1.Изменение химического состава атмосферы, ведущее к глобальному потеплению климата, разрушению озонового слоя, кислотным дождям, фотохимическим смогам и т.д.\n2.Рост дефицита водных ресурсов и ухудшение их качества.\n3.Возрастающее загрязнение различными токсикантами морей и океанов.\n4.Обезлесивание и опустынивание.\n5.Снижение биологического разнообразия планеты.\n6.Проблема опасных отходов (в том числе радиоактивных).\n7.Резкое ухудшение состояния среды обитания человека.')
    if message.text == 'Полезные советы':
        bot.send_message(message.chat.id,text=random_text)

@bot.message_handler(commands=['gtm'])
def gtm(message):
    for attachment in ctx.message.attachments:
                if attachment.filename.endswith(".jpg") or \
                attachment.filename.endswith(".jpeg") or \
                attachment.filename.endswith(".png"):
                    image_path = f'./images/{attachment.filename}'
                    bot.send_message(message.chat.id,attachment.save(image_path))
                    temp_msg = bot.send_message(message.chat.id,'Идет обработка изображения...')
                    class_name, score = get_class(image_path,
                                                    'gtm_model/keras_model.h5',
                                                    'gtm_model/labels.txt')
                    bot.send_message(message.chat.id,temp_msg.delete())
                    bot.send_message(message.chat.id,f'С вероятностью {score}% на фото {class_name.lower()}')
                    os.remove(image_path)
                else:
                    bot.send_message(message.chat.id,"Брат, мне нужна картинка")
                    return
    else:
        bot.send_message(message.chat.id,"Ты забыл загрузить фото(")

bot.polling()
