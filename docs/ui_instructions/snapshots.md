[Веб-интерфейс](../web_ui.md)

В данной вкладке можно ознакомиться со снапшотами (сохраненными состояниями операций поиска), выгрузить отчеты по ним в формате DOCX и удалить при необходимости

Для создания отчета по обычному проекту необходимо выбрать severity уязвимостей, которые попадут в отчет  
В отчет попадут только компоненты со статусом confirmed  
В отчет не попадут компоненты без уязвимостей  


Для создания отчёта по проекту Bitbake необходимо выбрать слои проекта и severity уязвимостей, которые попадут в отчет  
Также в отчёт попадут только уязвимости со статусом Unpatched  
Компонент не попадёт в отчёт, если у него нет Unpatched уязвимостей, либо выбранные уровни критичности имеют только уязвимости со статусом Patched  

В отчёты попадут все комментарии к уязвимостям и компонентам, а также их лицензии