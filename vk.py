import time
import vk_api
import requests, bs4

from vk_api.longpoll import VkLongPoll, VkEventType
from config import token

rooms = {
    "спальне": "Bedroom",
    "ванной": "Bathroom",
    "коридоре": "Hall",
    "кухне": "Kitchen"
}
topics = {
    "Bedroom": "home/bedroom/",
    "Bathroom": "home/bathroom/",
    "Hall": "home/hall/",
    "Kitchen": "home/kitchen/"
}


# TODO: Добавить тесты

vk_session = vk_api.VkApi(token=token)  # Авторизоваться как сообщество
vk = vk_session.get_api()

longpoll = VkLongPoll(vk_session)

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        command = event.text

        log = str(event.user_id) + ":" + event.text + ";"
        print(log)

        room = command.split(' ')[-1]
        room_name = rooms.get(room, "Room not found")

        #print(room_name)

        topic = topics.get(room_name, "Topic not found")

        if "Включи свет в " in command:
            topic = topic + "light"
            # publish.single(topic, "1", hostname="192.168.1.9")
            print(topic + " " + "1")
            print("Свет в " + room + " включен")
            response = "Свет в " + room + " включен"

        elif "Выключи свет в " in command:
            topic = topic + "light"
            # publish.single(topic, "0", hostname="192.168.1.9")
            print(topic + " " + "0")
            print("Свет в " + room + " выключен")
            response = "Свет в " + room + " выключен"


        elif "Закрой шторы в " in command:
            topic = topic + "curtain"
            # publish.single(topic, "0", hostname="192.168.1.9")
            print(topic + " " + "0")
            print("Шторы в " + room + " закрыты")
            response = "Шторы в " + room + " закрыты"


        elif "Открой шторы в " in command:
            topic = topic + "curtain"
            # publish.single(topic, "1", hostname="192.168.1.9")
            print(topic + " " + "1")
            print("Шторы в " + room + " открыты")
            response = "Шторы в " + room + " открыты"


        elif "Включи телевизор в " in command:
            topic = topic + "tv"
            #publish.single(topic, "1", hostname="192.168.1.9")
            print(topic + " " + "1")
            print("Телевизор в " + room + " включен")
            response = "Телевизор в " + room + " включен"

        elif "Выключи телевизор в " in command:
            topic = topic + "tv"
            # publish.single(topic, "0", hostname="192.168.1.9")
            print(topic + " " + "0")
            print("Телевизор в " + room + " выключен")
            response = "Телевизор в " + room + " выключен"

        elif "Состояние квартиры" in command:
            # TODO: Мониторинг движения
            pass

        elif "Температура в доме" in command:
            # TODO: Считывание данных с топика
            pass

        elif "Температура за окном" in  command:
            s = requests.get('https://sinoptik.com.ru/погода-санкт-петербург')
            b = bs4.BeautifulSoup(s.text, "html.parser")
            p3 = b.select('.temperature .p3')
            pogoda1 = p3[0].getText()
            p4 = b.select('.temperature .p4')
            pogoda2 = p4[0].getText()
            p5 = b.select('.temperature .p5')
            pogoda3 = p5[0].getText()
            p6 = b.select('.temperature .p6')
            pogoda4 = p6[0].getText()
            print('Утром :' + pogoda1 + ' ' + pogoda2)
            print('Днём :' + pogoda3 + ' ' + pogoda4)
            p = b.select('.rSide .description')
            pogoda = p[0].getText()
            print(pogoda.strip())
            response = 'Утром :' + pogoda1 + ' ' + pogoda2 + '\n' + 'Днём :' + pogoda3 + ' ' + pogoda4 + '\n' +pogoda.strip()

        elif "Включи кондиционер в " in command:
            topic = topic + "condition"
            # publish.single(topic, "1", hostname="192.168.1.9")
            print(topic + " " + "1")
            print("Кондиционер в " + room + " включен")
            response = "Кондиционер в " + room + " включен"

        elif "Выключи кондиционер в " in command:
            topic = topic + "condition"
            # publish.single(topic, "0", hostname="192.168.1.9")
            print(topic + " " + "0")
            print("Кондиционер в " + room + " выключен")
            response = "Кондиционер в " + room + " выключен"

        elif "Включи чайник в " in command:
            # TODO: Проверка воды и  уведомление о закипании
            topic = topic + "kettle"
            # publish.single(topic, "0", hostname="192.168.1.9")
            print(topic + " " + "0")
            print("Чайник в " + room + " включен")
            response = "Чайник в " + room + " включен"


        else:
            response = "команда не распознана"

        vk.messages.send(
            user_id=event.user_id,
            message=response
        )

