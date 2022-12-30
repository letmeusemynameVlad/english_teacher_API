from fastapi import FastAPI, Path
import uvicorn
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from helper import Helper
from models import AnswerRequestBody, LetterRequestBody, UserLoginBody

# Endpoints:
# word/guess,   word/check,    word/result
# letter/guess,   letter/check,    letter/result

api_app = FastAPI(title="English Teacher API",
                docs_url="/swagger",
                version="1.0")  # create API service
helper = Helper()  # database, questions


#   =================== WORD ======================


@api_app.get("/word/guess", tags=['word'])
def guess_word():
    return helper.generate_question_word()  # {"question_id": question_id, "variance": var, "english": en_word}


@api_app.get("/word/result/{question_id}", tags=['word'])
def guess_word_result(question_id: int):
    return helper.get_correct_result(question_id)


@api_app.post("/word/check", tags=['word'])
def guess_word_check(user_answer: AnswerRequestBody):
    return helper.check_answer(user_answer.question_id, user_answer.answer, user_answer.user_email)


#   =================== LETTER ======================

@api_app.get("/letter/guess", tags=['letter'])
def guess_letter():
    return helper.generate_question_letter()


@api_app.get("/letter/result/{question_id}", tags=['letter'])
def guess_letter_result(question_id: int = Path(1000, gt=0, description="question id from response")):
    return helper.get_correct_result(question_id)


@api_app.post("/letter/check", tags=['letter'])
def guess_letter_check(user_answer: LetterRequestBody):
    return helper.check_answer(user_answer.question_id, user_answer.letter,
                               user_answer.user_email)

#   =================== AUTH ======================


@api_app.get("/auth/login/{email}", tags=['auth'])
def login(email):
    return helper.login(email)


#   =================== RUN ======================

@api_app.get("/")
def root():
    return FileResponse("static/auth.html")


@api_app.get("/play")
def root():
    return FileResponse("static/index.html")


app = FastAPI(title="main app")

app.mount("/", api_app)
app.mount("/", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

