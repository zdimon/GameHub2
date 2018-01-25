Используем Tornado как WSGI сервер. 


Клиент отправляет запрос, если это не WebSocket отдаем на обработку джанге, если ws - Tornado.websocket

** предлагаю не мешать все в торнадо а использовать uwsgi для джанги **

Для вебсокетов https://github.com/peterbe/django-sockjs-tornado.

При старте игры клиент отправляет ws запрос серверу в виде json

    {   
        "game": "сервервное название игры", 
        "name": "название лобби", 
        "player": "информация о игроке"
    }
    
    
    
Торнадо сервер создает "комнату" в редисе, к которой подключает клиента и отправляет ему все сообщения которые туда приходят.

Для редиса не будет комнат, а будут каналы (по ид пользователя).

Комнаты создаются и обслуживаются на уровне сервера торнадо и так же могут быть использованы в приложении джанги.

В базе храним комнату с пользователями внутри них.

При коннекте пользователя к сокету и отправки информации о пользователе.

    { 
        "action": "connect",
        "id": 23,
        "name": "bogdan"
    }

Торнадо подписывает его на канал редиса (c именем id).

Все сообщения, поступающие в этот канал автоматически отсылаются торнадой по сокету в браузер.

Сообщения могут быть посланы как из торнады так и с джанги.

Для отсылки можно использовать клиент brukva.

После прихода сообщений с "action": "connect" отмечаем пользователя что он в онлайне и разсылаем широковещательный запрос всем пользователя онлайн с данными по новому юзеру.

    {
        "action": "someone_connected",
        "id": "...",
        "name": "..."
    }
    
Аналогично с дисконнектом.  

    {
        "action": "someone_disconnected",
        "id": "...",
        "name": "..."
    }  

Для каждой игры использовать свою модель для хранения данных в базе.

По возможности каждое действие, будь то редактирование профиля и пр. реализовывать в виде апи запросов с защитой токеном в хедере.

Так мы сможем подключать разных клиентов, не только браузерных.

Первое что нужно.

1. [Регистрация](/docs/registration.md).

2. Логин.

3. Редактирование профиля.

4. Сброс пароля.

5. Вход в игровую комнату.

6. Выход из комнаты.

[Викторина](https://github.com/Dj-Denis/GameHub/wiki/Викторина)