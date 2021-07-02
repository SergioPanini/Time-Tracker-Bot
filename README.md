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
<img src="https://user-images.githubusercontent.com/47488572/124310599-1383e680-db75-11eb-9b0b-80968f10ba31.png" width="24%" style="float: left;">
  
</div>

# Install
### Создайте файл с переменными окружения, содержащий:
`TELEGRAM_BOT_TOKEN` - API токен бота

`SHOW_ACTIVITIES_SIZE` - Сколько активностей выводить на главной панели

### Соберите docker image из dockerfile

`sudo docker build --tag time-tracket-bot .`

### Запустите контейнер на основе только что созданого образа

`sudo docker run --rm -it --env-file <файл с переменными окружения> time-tracket-bot`
