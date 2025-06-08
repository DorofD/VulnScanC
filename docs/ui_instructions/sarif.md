[Веб-интерфейс](../web_ui.md)

В данной вкладке можно просмотреть загруженные на сервер отчёты формата .sarif, а также отчёты с локальной машины  
Данный функционал реализован с помощью интеграции React компонента sarif-viewer от Microsoft

Импорт отчётов .sarif на данный момент доступен только через API и делается следующим образом:  
```
curl -X POST http://<vulnscanc_address>:5000/sarif -F "file=@./results.sarif" -F "project_name=test_project" -F "action=upload"
```
