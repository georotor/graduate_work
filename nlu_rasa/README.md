# Сервис выделения намерений и сущностей

Так как у `Маруси` отсутствует возможность самостоятельного извлечения намерений и сущностей из запроса пользователя, 
в сервис была добавлена небольшая нейронка, подготовленная на библиотеке `Rasa NLU`.

> `Rasa` построена на `tensorflow` и по умолчанию может использовать CPU, как настроить генерацию на GPU необходимо 
смотреть документацию в зависимости от используемого железа.

Базовое создание модели:
```shell
pip install -r requirements.txt
rasa train nlu --fixed-model-name nlu.tar.gz
```
После выполнения в каталоге `models` появится подготовленная модель.