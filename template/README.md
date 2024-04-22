# Создание нового сервиса

1. создать сервис на основе шаблона
```commandline
cookiecutter C:\finance\template
```
2. прописать игнорирование и включение путей в ruff.toml
```toml
include = [
   "src/bond_service/**.py",
   "src/portfolio_service/**.py",
]
exclude = [
   "src/bond_service/app/adapters/postgres/migration/**.py",
   "src/portfolio_service/app/adapters/postgres/migration/**.py",
   "template/**"
]
```
3. в docker-multiple-databases.sh и docker-compose.yaml добавить бд для приложения и тестов
4. изменить базу по умолчанию в config
5. изменить тестовую базу по умолчанию в test/integrations/config


# Добавление новых хендлеров 

1. создать хендлер
2. создать схемы
3. добавить зависимости в ioc.py
4. в app.py добавить созданные хендлеры

# Добавление таблиц postgres 

1. создать таблицы в postrgres/tables
2. в map.py добавить маппер в функцию run_mapper()
3. в meta.py добавить таблицы 