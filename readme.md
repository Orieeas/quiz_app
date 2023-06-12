1.	Создается подключение к базе данных PostgreSQL с помощью функции create_engine().
2.	Определяется модель данных Question, которая содержит одно поле questions_num.
3.	Создается экземпляр класса FastAPI.
4.	Определяется функция get_quiz_question, которая обрабатывает POST-запросы на адрес /quiz.
5.	Внутри функции get_quiz_question происходит следующее:
•	Сначала создается подключение к базе данных с помощью with engine.connect() as conn.
•	Затем происходит цикл, который продолжается до тех пор, пока не будут получены уникальные вопросы.
•	Внутри цикла отправляется запрос на API https://jservice.io/api/random, чтобы получить случайные вопросы. Количество вопросов определяется значением, переданным в запросе от клиента в поле questions_num.
•	Затем для каждого полученного вопроса проверяется его уникальность в базе данных. Если вопрос уже есть в базе данных, то выполняется дополнительный запрос к API, чтобы получить новый уникальный вопрос.
•	Если удалось получить уникальные вопросы, то они сохраняются в базе данных с помощью SQL-запроса insert() из библиотеки SQLAlchemy.
•	Далее из базы данных выбирается последний добавленный вопрос с помощью SQL-запроса select(), который сортирует записи по дате создания вопроса и выбирает последнюю запись. Это делается для того, чтобы вернуть пользователю самый последний добавленный вопрос.
•	Наконец, выбранный вопрос возвращается в виде словаря в ответ на запрос. Словарь содержит поля id, question, answer и created_at, которые представляют собой соответствующие поля в базе данных.
Таким образом, программа получает запрос на получение вопросов для викторины, проверяет уникальность вопросов в базе данных, сохраняет уникальные вопросы в базе данных и возвращает пользователю последний добавленный вопрос.

Полное техническое задание:
1. В сервисе должно быть реализован POST REST метод, принимающий на вход запросы с содержимым вида {"questions_num": integer}.
2. После получения запроса сервис, в свою очередь, запрашивает с публичного API (англоязычные вопросы для викторин) https://jservice.io/api/random?count=1 указанное в полученном запросе количество вопросов.
3. Далее, полученные ответы должны сохраняться в базе данных из п. 1, причем сохранена должна быть как минимум следующая информация (название колонок и типы данный можете выбрать сами, также можете добавлять свои колонки): 1. ID вопроса, 2. Текст вопроса, 3. Текст ответа, 4. - Дата создания вопроса. В случае, если в БД имеется такой же вопрос, к публичному API с викторинами должны выполняться дополнительные запросы до тех пор, пока не будет получен уникальный вопрос для викторины.
4. Ответом на запрос из п.2.a должен быть предыдущей сохранённый вопрос для викторины. В случае его отсутствия - пустой объект.



Инструкция к запуску:

1.	Установите Docker и Docker Compose на вашу машину, если они не установлены.
2.  Запустите контейнеры с помощью команды:
docker-compose up
3. Создайте небходимые таблицы, используя код из файла "postgres" 
4. Запускайте файл с post-запросом ost-requests.py, изменяя число вопросов в строке data = {'questions_num': 3}