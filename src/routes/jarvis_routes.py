from fastapi import APIRouter, UploadFile,File


router = APIRouter()



@router.post('/upload')
def upload_file(file: UploadFile = File(...)):
    return True