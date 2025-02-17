
from abc import ABC, abstractmethod

class Person(ABC):
    def __init__(self, id, name):
        self.id = id
        #меняем регистр на нижний и убираем пробелы
        self.name = name.lower().strip()

    @abstractmethod
    def get_info(self):
        #для подклассов
        pass

    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}"


class Client(Person):
    def __init__(self, id_client, name, telegram_id, discount=0):
        super().__init__(id_client, name)
        # проверка telegram_id начинается ли оно с '@'
        self.telegram_id = telegram_id if telegram_id.startswith('@') else '@' + telegram_id
        self.sessions = set()
        self.discount = discount

    def get_info(self):
        return f"Client ID: {self.id}, Name: {self.name}, Telegram ID: {self.telegram_id}, Discount: {self.discount}"

    @staticmethod
    def from_input_cl():
        name = input("Укажите ваше полное имя: ")
        tg_id = input("Введите свой телеграмм тег(@тг): ")
        return name, tg_id

    @staticmethod
    def from_print_cl():
        name, tg_id = Client.from_input_cl()
        print(f"Имя: {name}, Telegram ID: {tg_id} Было записано.")

    def add_session(self, session):
        self.sessions.add(session)


    def remove_session(self, session_id):
        self.sessions = {session for session in self.sessions if session.id != session_id}

    # ср с двумя кл
    def __add__(self, other):
         if isinstance(other, Client):
             new_name = f"{self.name} & {other.name}"
             new_telegram_id = f"{self.telegram_id}, {other.telegram_id}"
             new_discount = max(self.discount, other.discount) # Берет большую скидку
             return Client(id_client=None, name=new_name, telegram_id=new_telegram_id, discount=new_discount)
         else:
             raise TypeError("Можно складывать только объекты Client")

    #ср по скидке
    def __gt__(self, other):
        if isinstance(other, Client):
            return self.discount > other.discount
        else:
            raise TypeError("Можно сравнивать только объекты Client")

    #ср по tg_id
    def __eq__(self, other):
        if isinstance(other, Client):
            return self.telegram_id == other.telegram_id
        else:
            raise TypeError("Можно сравнивать только объекты Client")

class Photographer(Person):
    def __init__(self, photographer_id, name, description, work_time):
        super().__init__(photographer_id, name)
        self.description = description[:100] #описание до 100 символов
        self.work_time = work_time
        self.sessions = set()

    def get_info(self):
         return f"Photographer ID: {self.id}, Name: {self.name}, Description: {self.description}, Work Time: {self.work_time}"

    @staticmethod
    def from_input_ph():
        name = input("Введите имя: ")
        description = input("Введите описание: ")
        work_time = input("Введите рабочие часы: ")
        return name, description, work_time

    @staticmethod
    def from_print_ph():
        name, description, work_time = Photographer.from_input_ph()
        print(f"Имя: {name}, Описание: {description}, Рабочее время: {work_time}")


class Session:
    def __init__(self, id, photographer_id, id_client, start_time, duration_hours, status):
        self.id = id
        self.photographer_id = photographer_id
        self.id_client = id_client
        self.start_time = start_time
        self.duration_hours = duration_hours
        #Обработка строки: Преобразование статуса в верхний регистр.
        self.status = status.upper()

    def __str__(self):
         return f"Session ID: {self.id}, Photographer ID: {self.photographer_id}, Client ID: {self.id_client}, Start Time: {self.start_time}, Duration: {self.duration_hours}, Status: {self.status}"

    def __hash__(self):
         return hash(self.id) # Сессии считаются одинаковыми если у них одинаковый ID

class Price:
    def __init__(self, id, photographer_id, name_serves, description, duration_hours):
        self.id = id
        self.photographer_id = photographer_id
        self.name_serves = name_serves
        self.duration_hours = duration_hours
        self.description = description

    def __str__(self):
        return f"Price ID: {self.id}, Photographer ID: {self.photographer_id}, Service: {self.name_serves}, Duration: {self.duration_hours}, Description: {self.description}"


class Studio:
    MAX_SESSIONS = 50  #ст.п макс кол-во сессий
    session_count = 0  # действительные сессии

    def __init__(self, photographers):
      
        self.photographers = {p.id: p for p in photographers}  #из списка в словарь
        self.clients = {}
        self.sessions = {}

    def get_photographer_by_id(self, photographer_id):
        return self.photographers.get(photographer_id)

    def get_client_by_telegram_id(self, telegram_id):
        return self.clients.get(telegram_id)
    def add_client(self, client):
        self.clients[client.telegram_id] = client

    def add_session(self, session):
        if Studio.session_count < Studio.MAX_SESSIONS:  #не привысилось ли кол во записей
            self.sessions[session.id] = session
            Studio.session_count += 1
            print(f"Сессия добавлена. Всего сессий: {Studio.session_count}")
        else:
            print("Превышено максимальное количество сессий в студии.")

    def remove_session(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]
            Studio.session_count -= 1
            print(f"Сессия удалена.  Всего сессий: {Studio.session_count}")
        else:
            print("Сессия с id {session_id} не найдена в студии.")

    @staticmethod
    def get_max_sessions():
        #Стат метод для макс кол ва сессий.
        return Studio.MAX_SESSIONS

    @staticmethod
    def reset_session_count():
        #Стат метод сброса записей.
        Studio.session_count = 0
        print("Счетчик сессий сброшен.")


photographer1 = Photographer(1, "Артемий Фефелов", "Пикми", "Пн-пт; 15-21")
photographer2 = Photographer(2, "Иван Иванов", "Хорошие фото", "Сб-Вс")

studio = Studio([photographer1, photographer2])

#проверка

print("Укажите информацию для записи на съемку")
Client.from_print_cl()
name, telegram_id = Client.from_input_cl()
client1 = Client(1, name, telegram_id, discount=10)
studio.add_client(client1)


print("Клиент записан", studio.clients)

session1 = Session(1, 1, 1, "2024-03-15 14:00", 2, "Запланировано")
session2 = Session(2, 1, 1, "2024-03-16 14:00", 2, "Запланировано")
studio.add_session(session1)
studio.add_session(session2)

print("Сессии в студии:", studio.sessions)

client_found = studio.get_client_by_telegram_id(telegram_id)
if client_found:
    print(f"Найден клиент: {client_found.name}")
else:
    print("Клиент не найден.")

photographer_found = studio.get_photographer_by_id(1)
if photographer_found:
    print(f"Найден фотограф: {photographer_found.name}")
else:
    print("Фотограф не найден")

client1.add_session(session1)
client1.add_session(session1) #Попытка добавить дубликат
print("Действующая сессия клиента:", client1.sessions)

#удаляем клиента из сессии
client1.remove_session(1)
print("Сессия для удаления:", client1.sessions)


# Удаляем сессию из студии
studio.remove_session(2)
print("Сессия после удаления:", studio.sessions)

# Добавим вывод информации о клиенте и фотографе
print(client1.get_info())
print(photographer1.get_info())
print(session1)
price1 = Price(1, 1, "Стандартная фотосессия", "Описание стандартной фотосессии", 1)
print(price1)

#  использованиe статических полей и методов
print(f"Максимальное количество сессий: {Studio.get_max_sessions()}")
print(f"Текущее количество сессий: {Studio.session_count}")

Studio.reset_session_count()  # Сброс счетчика сессий
print(f"После сброса, текущее количество сессий: {Studio.session_count}")

photographer3 = studio.get_photographer_by_id(2) # поиск второго фотографа по ID
if photographer3:
    print(f"Найден фотограф: {photographer3.name}")
else:
    print("Фотограф не найден")

#перегруженние операторов
client2 = Client(2, "eлена", "@елена", discount=15)

#  Объединение клиентов
client3 = client1 + client2
print(f"Объединенный клиент: {client3.get_info()}")

# > Сравнение по скидке
print(f"У {client1.name} скидка больше, чем у {client2.name}? {client1 > client2}")

# Сравнение по telegram_id
client4 = Client(4, "Какой-то человек", client1.telegram_id) # Создаем клиента с тем же telegram_id
print(f"{client1.name} и {client4.name} имеют одинаковый telegram_id? {client1 == client4}")
