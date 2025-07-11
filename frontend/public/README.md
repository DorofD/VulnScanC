VulnScanC - это SCA инструмент для централизованного сбора и обработки данных о сабмодульных (submoduled) и поставляемых (vendoring) компонентах, их уязвимостях и лицензиях в проектах на C/C++

Основной функционал:
- Поиск сторонних компонентов в проектах на C/C++ при отсутствии в них пакетного менеджера
- Поиск уязвимостей и лицензий в сторонних компонентах
- Генерация отчётов о найденных уязвимостях

Дополнительный функционал:
- Поиск уязвимостей по БДУ ФСТЭК
- Интеграция с Dependency-Track, создание отчётов по проектам из DT 
- Интеграция со Svacer 8.x.x, создание отчётов по проектам из Svacer 
- Загрузка и просмотр .sarif отчётов 
- Обработка данных проектов, использующих Bitbake, аналогично с основным функционалом

Подробно проблематика, решаемая данным инструментом, описана здесь: https://osv.dev/blog/posts/using-the-determineversion-api/. Вкратце она заключается в отсутствии информации о сторонних компонентах в проектах без пакетных менеджеров и, как следствие, информации об их уязвимостях, а также отсутствии возможности централизированного сбора и обработки этих данных

Сервис включает в себя 3 основных элемента:
- Бекенд, предназначен для хранения и обработки данных
- Фронтенд, служит для взаимодействия с данными
- Исполняемый модуль, предназначен для сбора данных и отправки их на бекенд


Подробнее:  
- [Установка](docs/installation.md)  
- [Интеграция в CI](docs/ci_integration.md)  
- [Механизмы поиска](docs/search_mechanism.md)  
- [Веб-интерфейс](docs/web_ui.md)  
- [Исполняемый модуль](docs/executable_module.md)  
