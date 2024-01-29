from information_gatherer import Gather

from fastapi import FastAPI, Form

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/query/")
async def query(product: str = Form(...)):
    return {"product": Gather(product=product, verbose=True).run()}
