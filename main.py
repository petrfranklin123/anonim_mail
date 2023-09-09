import requests
import random
import string
import time
import os

# обозначим ссылку для работы с API сервисом
API = "https://www.1secmail.com/api/v1/"

# создадим список возможных почтовых доменов
domain_list = [
  "1secmail.com",
  "1secmail.org",
  "1secmail.net"
]

# выбираем рандомный домен 
domain = random.choice(domain_list)

# генерация имени почты
def generate_username():
    name = string.ascii_lowercase + string.digits # string.ascii_lowercase - символы в нижнем регистре; string.digits - цифры 
    username = "".join(random.choice(name) for i in range(10)) # создадим почту из рандомных 10 символов 
    return username

# для проверки входящих писем 
def check_mail(mail=""): # принимается сгенерированный mail
    req_link = f"{API}?action=getMessages&login={mail.split('@')[0]}&domain={mail.split('@')[1]}"
    r = requests.get(req_link).json() # отправляем запрос и получаем в json
    length = len(r) # возвращаем количество данных 

    if length == 0:
        print("[-] Пока писем нет! Проверка происходит каждый пять секунд!")
    else:
        id_list = []

        for i in r: 
            for key, value in i.items():
                  if key == "id":
                    id_list.append(value)


        print(f"[+] У вас {length} входящих! Проверка происходит каждый пять секунд!")


        # далее запишем приходящее письмо или письма 
        current_dir = os.getcwd() # текущая директория  
        final_dir = os.path.join(current_dir, "all_mails") # директория, куда все будет записываться

        # сделаем проверку, что если этой директории не существует то создаем ее 
        if not os.path.exists(final_dir):
            os.makedirs(final_dir)

        # далее пробегаемся по списку с id
        for id in id_list:
            read_msg = f"{API}?action=readMessage&login={mail.split('@')[0]}&domain={mail.split('@')[1]}&id={id}"
            r = requests.get(read_msg).json() # получаем сообщение по id 

            # получаем содержимое письма по ключам
            sender = r.get("from")
            subject = r.get("subject")
            date = r.get("date")
            content = r.get("textBody")

            # осталось сохранить сообщения в файл 
            mail_file_path = os.path.join(final_dir, f"{id}.txt") # чтобы избежать перезаписи, будем сохранять по id сообщения
            
            # записываем в файл 
            with open(mail_file_path, "w") as file:
                file.write(f"Sender: {sender}\nTo: {mail}\nSubject: {subject}\nDate: {date}\nContent: {content}")

# для удаления почты
def delete_mail(mail = ""):
    url = "https://www.1secmail.com/mailbox"

    data = {
        'action' : 'deteteMailBox',
        'login' : mail.split("@")[0],
        'domain' : mail.split("@")[1]
    }

    r = requests.post(url, data = data)
    print(f"[X] Почтовый адрес {mail} - удален")

def main():
    try:
        username = generate_username()
        mail = f"{username}@{domain}"
        print(mail)

        # отправим запрос, чтобы залогиниться
        mail_req = requests.get(f"{API}?login={mail.split('@')[0]}&domain={mail.split('@')[1]}")

        while True:
            check_mail(mail=mail) # проверяем почту 
            time.sleep(5)

    except(KeyboardInterrupt): # KeyboardInterrupt - отрабатывает, когда вводится комбинайия клавиш 
        delete_mail(mail = mail)
        print("Программа остановлена!")

if __name__ == "__main__":
    main()