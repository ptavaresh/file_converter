from PIL import Image
import aiofiles
from docx2pdf import convert


from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse

app = FastAPI()


@app.post("/compress/uploadfile/")
async def create_upload_file(file: UploadFile):
    """
    Compress a JPEG image:

    - **file**: a valid image/jpeg file 

    """
    allowed_types = ["image/jpeg"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=415,
            detail="El tipo de archivo no es válido. Tipos permitidos: {}".format(
                allowed_types
            ),
        )
    async with aiofiles.open("original.jpg", 'wb') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write
        input_img = Image.open("original.jpg")
        input_img.save('compressed.jpg', optimize=True, quality=50)
    return FileResponse('compressed.jpg')


@app.post("/pdf/wordtopdf/")
async def create_file(file: UploadFile):
    """
    Converto word or jpeg file to PDF:

    - **file**: a valid word or jpeg file

    """
    allowed_types = ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
    print(file.content_type)
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=415,
            detail="El tipo de archivo no es válido. Tipos permitidos: {}".format(
                allowed_types
            ),
        )
    async with aiofiles.open("original.docx", 'wb') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write
        file = open("original.docx", "w")
        file.close()

        convert("original.docx", "convertedToPDF.pdf")

    return FileResponse('convertedToPDF')

@app.post("/pdf/jpegtopdf/")
async def create_file(file: UploadFile):
    """
    Converto word or jpeg file to PDF:

    - **file**: a valid word or jpeg file

    """
    allowed_types = ["image/jpeg"]
    print(file.content_type)
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=415,
            detail="El tipo de archivo no es válido. Tipos permitidos: {}".format(
                allowed_types
            ),
        )
    async with aiofiles.open("original", 'wb') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write
        input_img = Image.open("original.jpg")
        input_img.save('compressed.pdf', save_all=True)

    return FileResponse('compressed.pdf')