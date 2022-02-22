from fastapi import FastAPI
from Models.response_models import Profanity, UserRequestIn, Info
from profanity_check import predict

from image.image_recommendation import ImageApi

app = FastAPI()
image_api = ImageApi()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post('/profanity', response_model=Profanity)
async def infer_profanity(user_request: UserRequestIn):
    text = user_request.text
    questionID = user_request.questionID
    result = predict([text])
    print(result)
    if result[0] == 0:
        output = "No profanity"
    else:
        output = "Profanity"

    return {'profanity': output, 'questionID': questionID}


@app.post("/image")
async def read_root(info: Info):
    best_photo_id = image_api.get_image_url(info.question)
    photo_image_url_1 = "https://unsplash.com/photos/"
    photo_image_url_2 = "/download?w=320"
    return {
        "url": photo_image_url_1 + best_photo_id[0] + photo_image_url_2,
        'questionID': info.question_id
    }