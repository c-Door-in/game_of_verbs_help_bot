# Бот для ответа на часто задаваемые вопросы
 В данном проекте представлены два бота для диалога с пользователями в режиме 
 автоответчика по часто задаваемым вопросам.  
 Один бот для Telegram, другой - для Вконтакте.  
 Для распознавания вопросов и формирования ответов применена система 
 [Google DialogFlow](https://cloud.google.com/dialogflow).
 
 ## Примеры
 Для примера выбрана вымышленная компания по оказанию услуг 
 продвижения блогеров "Игра глаголов". В примерах запрограммирован 
 ответ на приветствие и на вопрос о возможности устройства на работу.
 ### Пример [бота для Telegram](https://t.me/game_of_verbs_help_bot)
  <img src="https://github.com/c-Door-in/game_of_verbs_help_bot/blob/main/echo_tg.gif" width="300" />
 
 ### Пример [бота для Вконтакте](https://vk.com/im?sel=-213664954)
  <img src="https://github.com/c-Door-in/game_of_verbs_help_bot/blob/main/echo_vk.gif" width="300" />
 
 ## Установка
 У вас уже должен быть установлен Python3.  
 Подключите зависимости:
 ```
 pip install -r requirements.txt
 ```
 ### Создайте бота у [Bot Father](https://t.me/BotFather)
 
 ### Создайте [группу в VK](https://vk.com/groups?tab=admin&w=groups_create)
 В настройках группы создайте ключ доступа (Управление - Настройки - Работа с API - Создать ключ).
 Разрешите отправку сообщений из группы.

 ### Создайте проект на [https://dialogflow.cloud.google.com/](https://dialogflow.cloud.google.com/#/login)
 Подробная [инструкция](https://cloud.google.com/dialogflow/docs/quick/setup) по регистрации и установке проекта.

 ### [Создайте агент](https://cloud.google.com/dialogflow/docs/quick/build-agent) в проекте DialogFlow
 В агенте установите русский язык.  
 Для распознавания вопросов и подбора необходимых ответов используются Intent. 
 Для добавления Intent необходимо создать json файл со словарем в формате:
 ```json
 {
    "Устройство на работу": {
        "questions": [
            "Как устроиться к вам на работу?",
            "Как устроиться к вам?",
            "Как работать у вас?",
            "Хочу работать у вас",
            "Возможно ли устроиться к вам?",
            "Можно ли мне поработать у вас?",
            "Хочу работать редактором у вас"
        ],
        "answer": "Если вы хотите устроиться к нам, напишите на почту game-of-verbs@gmail.com мини-эссе о себе и прикрепите ваше портфолио."
    },
    "Забыл пароль": {
        "questions": [
            "Не помню пароль",
            "Не могу войти",
            "Проблемы со входом",
            "Забыл пароль",
            "Забыл логин",
            "Восстановить пароль",
            "Как восстановить пароль",
            "Неправильный логин или пароль",
            "Ошибка входа",
            "Не могу войти в аккаунт"
        ],
        "answer": "Если вы не можете войти на сайт, воспользуйтесь кнопкой «Забыли пароль?» под формой входа. Вам на почту придёт письмо с дальнейшими инструкциями. Проверьте папку «Спам», иногда письма попадают в неё."
    }
}
 ```
 где:
 - название каждого раздела - название группы сущностей для распознавания;
 - `questions` - вопросы, которые может задать пользователь, характерные для этой группы;
 - `answer` - фраза, которую пришлёт бот в ответ на эти вопросы.  
 После этого необходимо запустить `create_intent.py`, где в качестве аргумента нужно указать путь к json файлу с данными.
 ```
 python create_intent.py /path/intents.json
 ```
 
 ## Установка переменных среды
 Создайте в корне файл .env  
 Запишите в него следующие переменные:
 ```
 VK_TOKEN=<Ключ доступа вашей группы во Вконтакте>

 TGBOT_TOKEN=<Токен вашего телеграм бота>

 DIALOGFLOW_PROJECT_ID=<ID проекта в DialogFlow>

 GOOGLE_APPLICATION_CREDENTIALS=<Путь к файлу json, созданному для авторизации в проектах Google>
 ```
 Также вы можете указать ID бота в Telegram, который будет присылать вам технические сообщения о работе основных ботов:
 ```
 TG_ADMIN_BOT_TOKEN=<Токен технического бота>

 TG_ADMIN_CHAT_ID=<Ваш ID в телеграм>
 ```
 
 ## Запуск
 Команда для запуска Telegram бота:
 ```
 python tg_bot.py
 ```
 Команда для запуска бота во Вконтакте:
 ```
 python vk_bot.py
 ```

 ## Цель проекта
 Проект создан в учебных целях на портале [Devman](https://dvmn.org/).
