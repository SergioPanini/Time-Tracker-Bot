# Introdaction
Это бот который помогает отслеживать на что ты уходит твое время.

У тебя есть несколько предустановленых активностей: работа, спорт, отдых. Нажимая на кнопку
активности \"Начать\" ты запускаешь отслеживание, нажимая на кнопку активности \"Остановить\"
ты останавливаешь отслеживание активности.

Несколько активностей могут отслеживатся независимо
друг от друга. Главное не забывай их останавливать.

Бот доступен по сслыке https://t.me/Panini_Tracker_bot

<div>
<img src="https://user-images.githubusercontent.com/47488572/124309723-d539f780-db73-11eb-8b6d-958c6de97609.png" width="24%" style="float: left;">
<img src="https://user-images.githubusercontent.com/47488572/124309956-31048080-db74-11eb-8b78-908bff70c9e7.png" width="24%" style="float: left;">

<img src="https://user-images.githubusercontent.com/47488572/124310576-0bc44200-db75-11eb-9503-a123398cb419.png" width="24%" style="float: left;">
<img src="https://user-images.githubusercontent.com/47488572/124310588-0f57c900-db75-11eb-9e88-204680646d5a.png" width="24%" style="float: left;">
<img src="https://user-images.githubusercontent.com/47488572/124310594-11218c80-db75-11eb-86a0-a3ce3f8c2830.png" width="24%" style="float: left;">
<img src="https://user-images.githubusercontent.com/47488572/124558349-2c292080-de43-11eb-8b08-60026dae7124.png" width="24%" style="float: left;">
</div>


# Install
### Клонирвание репозитория
`git clone https://github.com/SergioPanini/Time-Tracker-Bot.git`

### Перейдите в директорию проекта
`cd Time-Tracker-Bot`

### Создайте файл `envfile` с переменными окружения, содержащий:
`TELEGRAM_BOT_TOKEN` - API токен бота

`SHOW_ACTIVITIES_SIZE` - Сколько активностей выводить в консоль

### Соберите docker-compose и запутстите docker-compose
`sudo docker-compose up --build -d`


# Deploy Release

### Перейдите в директорию проекта
`cd Time-Tracker-Bot`

### Остановите docker-compose
`sudo docker-compose down`

### Создайте бэкап базы
`cp ./source/data/db.sqlite3 backup_db-YYYY-MM-DD.sqlite3`

### Скачайте последнее обновление
`git pull`

### Соберите docker-compose и запустите docker-compose
`sudo docker-compose up --build -d`

# Logs
Логи хранятся в `/home/bot` в docker-compose. Что бы посмотреть логи перейдите в директорию проекта и введите `sudo docker-compose exec bot cat app.log`.




### -> DOTO
- Сделать удаление активностей из консоли
- Сделать сортирвку статистики по месяцам, неделям.
- Сделать оповещение юзеров об нововедениях нового обновления.
- Сделать переклбчение страниц на консоли более явным, т.е. добавить что то типо текста "пеерйти на страницу N".