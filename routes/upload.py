from fastapi import FastAPI, File, UploadFile, responses, APIRouter
from deta import Drive

router = APIRouter()

files = Drive("files")


@router.post("/")
def upload(file: UploadFile = File(...)):
    return files.put(file.filename, file.file)


@router.get("/")
def list_files():
    return files.list()


@router.get("/{name}")
def serve(name):
    img = files.get(name)
    ext = name.split(".")[1]
    return responses.StreamingResponse(img.iter_chunks(), media_type=f"image/{ext}")