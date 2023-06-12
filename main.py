from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import requests
import ujson

# Создаем экземпляр приложения FastAPI
app = FastAPI(debug=True)

# Создаем подключение к базе данных
engine = create_engine('postgresql://user:user@localhost:5432/quiz_questions')
Session = sessionmaker(bind=engine)

# Создаем базовую модель вопроса для сохранения в базе данных
Base = declarative_base()
class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, unique=True)
    question = Column(String)
    answer = Column(String)
    created_date = Column(DateTime)

    def __init__(self, question_id, question, answer, created_date):
        self.question_id = question_id
        self.question = question
        self.answer = answer
        self.created_date = created_date

# Определяем модель запроса
class QuizRequest(BaseModel):
    questions_num: int

# Функция для получения уникального вопроса из API
def get_unique_question():
    while True:
        response = requests.get("https://jservice.io/api/random?count=1")
        question = response.json()[0]
        with Session() as session:
            # Проверяем, что вопрос уникальный
            if not session.query(Question).filter(Question.question_id == question["id"]).first():
                return question

# Определяем обработчик POST запросов
@app.post("/quiz")
async def generate_quiz(quiz_request: QuizRequest):
    questions_num = quiz_request.questions_num

    questions = []
    for i in range(questions_num):
        unique_question = get_unique_question()

        with Session() as session:
            question = session.query(Question).filter(Question.question_id == unique_question["id"]).first()

            if not question:
                question = Question(
                    question_id=unique_question["id"],
                    question=unique_question["question"],
                    answer=unique_question["answer"],
                    created_date=datetime.now()
                )
            session.add(question)
            session.commit()

    else:
        question = session.merge(question)

                # Обновляем поле
        question.created_date = datetime.now()

        session.commit()

# Возвращаем предыдущий сохраненный вопрос
    last_question = session.query(Question).order_by(Question.id.desc()).first()
    return ujson.dumps({
        "question": last_question.question if last_question else "",
        "answer": last_question.answer if last_question else ""
    })