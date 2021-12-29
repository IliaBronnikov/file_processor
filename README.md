## API для обработки файлов:
- Загрузка файла через Post запрос (получения task_id)
- Получения результата обработки через Get запрос по task_id

### Установка проекта

- Собрать образ 
```
docker-compose up
```
- Образ rabbitmq работает на порту 5672
- Образ postgres работает на порту 5432
- Сервис доступен по адресу http://127.0.0.1:8000/

### Примеры запросов

- POST запрос
  ```
  curl --request POST 'http://127.0.0.1:8000/' -F '@/home/petehouston/test.xlsx' --header "Authorization: Bearer footokenbar"
  ```
- GET запрос
  ```
  curl --request GET 'http://127.0.0.1:8000/status?task_id=c2fa12ce-29a9-4d23-8208-9ab48e7ef1c2'
  ```


