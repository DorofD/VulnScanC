[Вернуться к основному README](../README.md)

Исполняемый модуль загружается с бекенда для выполнения поиска компонентов и уязвимостей в проекте  
Загрузить и запустить модуль можно отдельно:  
```
wget http://<vsc_backend_ip>:5000/binary?action=get_file -O exec_module  
chmod +x exec_module  
./exec_module --project_name=some_project_name --server_address='<vsc_backend_ip>:5000' --pipline_id=some_random_number --output_mode=console/file/json
```

Аргументы:

*-h, --help*  
Вывести подсказку

*-pn, --project_name*  
Название проекта на сервере VulnScanC
Используется для указания указания проекта в выходных документах, json файлах и при отправке данных  
Пример ввода: -pn=project_name

*-sa, --server_address*  
ip адрес и порт сервера VulnScanC, которому нужно отправить результаты  
Пример ввода: -sa='127.0.0.1:5000'

*-pi, --pipeline_id*  
ID пайплайна в GitLab  
Пример ввода: -pi=$CI_PIPELINE_ID

*-om, --output_mode*  
Режим вывода данных: console, file, json. По умолчанию используется console  
Можно указать несколько режимов одновременно:
--output-mode=console/file/json

*-p, --path*  
Директория для выполнения операций. По умолчанию используется текущая директория  
Для изменения директории можно ввести:
--path='./path/to/dir'
