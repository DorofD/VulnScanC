[Вернуться к основному README](../README.md)

Способ ручной развертки:
```
git clone ssh://git@dso-gitlab.kraftway.ru:2222/secure_development/dev_sec_tool.git
cd VulnScanC && mkdir data && mkdir binary && cp backend/.env.example backend/.env && cp frontend/.env.example frontend/.env
*заполните файлы frontend/.env и backend/.env нужными значениями*
docker compose up -d
```
После развертки можно зайти в приложение по ip адресу сервера под пользователем admin с паролем admin