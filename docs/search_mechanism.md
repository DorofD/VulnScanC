[Вернуться к основному README](../README.md)

Поиск компонентов:  
> Исполняемый модуль хеширует файлы в директориях проекта и отправляет в эндпоинт OSV:  
https://google.github.io/osv.dev/post-v1-determineversion/  
Из эндпоинта в ответ приходит информация о предполагаемых версиях сторонних компонентов, которые были найдены

Поиск CVE:  
> По компонентам, найденным с помощью OSV determineversion, производится поиск уязвимостей в другом эндпоинте OSV:  
https://google.github.io/osv.dev/post-v1-query/  
Из эндпоинта приходит информация о найденных в компоненте уявзимостях  

Поиск лицензий:  
> На данный момент можно осуществить автоматический поиск лицензий для компонентов, исходники которых лежат на GitHub  
Для компонентов, располагающихся в других местах, лицензии необходимо добавлять вручную

Поиск уязвимостей по БДУ ФСТЭК:  
> Уязвимости в БДУ ФСТЭК ищутся с помощью сопоставления по CVE id  
После выполнения стандартного поиска CVE в компонентах можно запустить механизм сопоставления,  
в результате работы которого будут найдены уязвимости из БДУ с совпадающими CVE id

Поиск компонентов, уязвимостей и лицензий в Bitbake:  
> Поиск компонентов, уязвимостей и лицензий в Bitbake осуществляется с помощью окружения Bitbake во время сборки  
Для этого необходимо указать ряд флагов при сборке, после чего загрузить полученные файлы через API 