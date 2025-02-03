class Client:
    def init(self, id_client, name, telegram_id):
        self.id_client = id_client
        self.name = name
        self.telegram_id = telegram_id
        self.sessions = []

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
        self.sessions.append(session)


    def remove_session(self, session_id):
        self.sessions = [session for session in self.sessions if session.id != session_id]


class Photographer:
    def init(self, photographer_id, name, description, work_time):
        self.photographer_id = photographer_id
        self.name = name
        self.description = description
        self.work_time = work_time
        self.sessions = []

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
    def init(self, id, photographer_id, id_client, start_time, duration_hours, status):
        self.id = id
        self.photographer_id = photographer_id
        self.id_client = id_client
        self.start_time = start_time
        self.duration_hours = duration_hours
        self.status = status


class Price:
    def init(self, id, photographer_id, name_serves, description, duration_hours):
        self.id = id
        self.photographer_id = photographer_id
        self.name_serves = name_serves
        self.duration_hours = duration_hours
        self.description = description


class Studio:
    def init(self, photographers):
        self.photographers = photographers
        self.clients = {}
        self.sessions = {}

    def get_photographer_by_id(self, photographer_id):
        for i in self.photographers:
            if i.photographer_id == photographer_id:
                return i
        return None

    def get_client_by_telegram_id(self, telegram_id):
        return self.clients.get(telegram_id)
    def add_client(self, client):
        self.clients[client.telegram_id] = client

    def add_session(self, session):
        self.sessions[session.id] = session

    def remove_session(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]
        else:
            print("Сессия с id {session_id} не найдена в студии.")



photographer1 = Photographer(1, "Артемий Фефелов", "Пикми", "Пн-пт; 15-21")

studio = Studio([photographer1])

#проверка

print("Укажите информацию для записи на съемку")
Client.from_print_cl()
name, telegram_id = Client.from_input_cl()
client1 = Client(1, name, telegram_id)
studio.add_client(client1)


print("Клиент записан", studio.clients)

session1 = Session(1, 1, 1, "2024-03-15 14:00", 2, "Запланировано")
studio.add_session(session1)

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
print("Действующая сессия клиента:", client1.sessions)

#удаляем клиента из сессии
client1.remove_session(1)
print("Сессия для удаления:", client1.sessions)


# Удаляем сессию из студии
studio.remove_session(2)
print("Сессия после удаления:", studio.sessions)