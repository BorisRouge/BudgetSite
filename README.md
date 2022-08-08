# BudgetSite
[Screencast from 20.07.2022 14_50_31.webm](https://user-images.githubusercontent.com/103374481/179931121-ce77014d-8d4a-4291-a767-b4f674a1f986.webm)

Веб-сайт на django, может регистрировать и аутентифицировать пользователей. Основная функция - ведение бюджета: пользователь создаёт категории расходов, записывает в них операции с внесением и снятием средств и комментарии к ним. При выборе категории в выпадающем окне отображается ее ведомость с операциями, асинхронно и без перезагрузки страницы с помощью скрипта на базе JS. Также JS-скрипт отображает диаграмму общей композиции бюджета по категориям.

Использованы Django (UserAuth, CBV, MVC, ORM), расчеты в отдельном модуле Python через классы, базовый JS во фронтенде.


A training project of a website with personal budgeting features./Тренировочный проект сайта с возможностями организации персонального бюджета.

This is a work in progress./Незавершенная работа.




