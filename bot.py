import configure
import ImagePreparation
import telebot
from telebot import types
import TextRecognition
import TextTranslate

client = telebot.TeleBot(configure.config['token'])
a = -1
lang_1 = "eng"
lang_2 = "rus"

@client.message_handler(commands= ['start'])
def get_text(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Текст фото")
    btn2 = types.KeyboardButton("Текст с комикса")
    btn3 = types.KeyboardButton("Перевод текста")
    btn4 = types.KeyboardButton("Перевод комикса/манги")
    btn5 = types.KeyboardButton("info")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    client.send_message(message.chat.id, text="Привет, {0.first_name}! Я переводчик, если нужна информация о боте, напиши 'info' или нажми на кнопу 'info'".format(message.from_user), reply_markup=markup)

@client.message_handler(content_types=['text'])
def func(message):
    global a
    a = -2
    if(message.text == "Текст фото"):
        a = 1
        client.reply_to(message, "Фото жду Я")
    elif(message.text == "Текст с комикса"):
        a = 2
        client.reply_to(message, "Фото жду Я")
    elif message.text == "Перевод текста":
        a = 3
        client.reply_to(message, "Фото жду Я")
    elif message.text == "Перевод комикса/манги":
        a = 4
        client.reply_to(message, "Фото жду Я")
    elif message.text == "info":
        a = 5
        txt = "1) Текст фото: Присылает текст с фотографии и саму фотографию, с отмеченными кусками текста;\n"
        txt += "2) Текст с комикса: Присылает текст с окон диалога и саму фотографию, с отмеченными текстами из окон;\n"
        txt += "3) Перевод текста: Присылает текст перевода с фотографии и саму фотографию, с отмеченными кусками текста;\n"
        txt += "4) Текст с комикса: Присылает перевод с окон диалога и саму фотографию, с отмеченными текстами из окон;\n----------------\n"
        txt += "-> В боте реализованны два нахождения текста: нахождение текста через easyocr и Tesseract. В первом методе мы находим блоки текста и объеденяем их в смысловые абзацы, что визуализируем через opencv. Во втором же, текст находит Tesseract OCR, предварительно скачанный для нужных языков.\n"
        txt += "-> Для нахождения текста только в окнах диалога комикса использовался opencv - выделение нужного контура (-2) и удаление с изображения всех остальных деталей (закраска в белый)\n"
        txt += "-> Для перевода использовали DeepL, так как он умеет хорошо обрабатывать плохой текст, но для того, чтобы не покупать лицензию, парсим сайт с помощью Selenium и fake-useragent;"
        client.reply_to(message, txt)
    else:
        client.reply_to(message, "Запрос повторите Вы")
    
        

@client.message_handler(content_types=['photo'])
def handle_docs_document(message):
    file_info = client.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = client.download_file(file_info.file_path)
    # src = 'C:\\Users\\123\Desktop\\progs\\Python\\Projects\\Text_recognition\\content_test\\' + message.photo[1].file_id
    src = 'C:\\Users\\123\Desktop\\progs\\Python\\Projects\\Text_recognition\\content_test\\photo.jpg'
    # fl = open(message.photo[1].file_id, "rb")
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    print(a)
    if a == 1:
        client.reply_to(message, "Фото добавлено мною")
        txt = "Method1:\n----------------\n"
        tx = TextRecognition.recognize_text(src, True, True)
        for i in tx:
            txt += i[1] + '\n----------------\n'
        client.reply_to(message, txt)
        client.reply_to(message, "Method2:\n----------------\n" + TextRecognition.just_tesseract(src))
        client.send_photo(message.chat.id, photo=open(src, 'rb'))
    elif a == 2:
        ImagePreparation.clear_contours(src, "ans.jpg")
        client.reply_to(message, "Фото добавлено мною")
        txt = "Method1:\n----------------\n"
        tx = TextRecognition.recognize_text("ans.jpg", True, True)
        for i in tx:
            txt += i[1] + '\n----------------\n'
        client.reply_to(message, txt)
        client.reply_to(message, "Method2:\n----------------\n" + TextRecognition.just_tesseract("ans.jpg"))
        client.send_photo(message.chat.id, photo=open("ans.jpg", 'rb'))
    elif a == 3:
        client.reply_to(message, "Фото добавлено мною")
        txt = "Method1:\n----------------\n"
        tx = TextRecognition.recognize_text(src, True, True)
        for i in tx:
            txt += TextTranslate.translate(i[1]) + '\n----------------\n'
        client.reply_to(message, txt)
        client.reply_to(message, "Method2:\n----------------\n" + TextTranslate.translate(TextRecognition.just_tesseract(src)))
        client.send_photo(message.chat.id, photo=open(src, 'rb'))
    elif a == 4:
        ImagePreparation.clear_contours(src, "ans.jpg")
        client.reply_to(message, "Фото добавлено мною")
        txt = "Method1:\n----------------\n"
        tx = TextRecognition.recognize_text("ans.jpg", True, True)
        for i in tx:
            txt += TextTranslate.translate(i[1]) + '\n----------------\n'
        client.reply_to(message, txt)
        client.reply_to(message, "Method2:\n----------------\n" + TextTranslate.translate(TextRecognition.just_tesseract("ans.jpg")))
        client.send_photo(message.chat.id, photo=open("ans.jpg", 'rb'))
            

client.infinity_polling()