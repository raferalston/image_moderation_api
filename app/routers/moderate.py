from fastapi import APIRouter, UploadFile, File, HTTPException
from services.moderate import moderate_image


router = APIRouter()

@router.post("/moderate")
async def moderate(file: UploadFile = File(...)):
    """
    Принимает изображение (файл) и отправляет его на модерацию.
    
    Параметры:
        file (UploadFile): Загружаемый файл изображения.
        #TODO: url - Добавить функционал исползования ссылки на изображение.
     
    Возможные ошибки:
        500 Internal Server Error — если возникла ошибка при обработке файла или обращении к сервису модерации.
    """
    try:
        filename = file.filename
        contents = await file.read()
        result = await moderate_image(contents, filename)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
