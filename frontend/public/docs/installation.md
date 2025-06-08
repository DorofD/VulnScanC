[Вернуться к основному README](../README.md)

Способ ручной развертки:
```
git clone https://github.com/DorofD/VulnScanC
cd VulnScanC && mkdir data binary nginx nginx/conf.d nginx/ssl
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env 
cp docker/vsc.conf nginx/conf.d/vsc.conf
*заполните файлы frontend/.env и backend/.env нужными значениями*
*скорректируйте файл nginx/conf.d/vsc.conf в зависимости от использования HTTPS и TLS*
docker compose up -d
```
После развертки можно зайти в приложение по ip адресу сервера либо доменному имени под пользователем admin с паролем admin