from io import StringIO

import pandas as pd
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import StreamingResponse

from csv_transformator.utils import transform

app = FastAPI()


@app.post("/upload")
async def transform_file(file: UploadFile):
    try:
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode('utf-8')), header=None)
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="File is empty")

    try:
        df = transform(df)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Wrong file format: {e}")

    stream = StringIO()
    df.to_csv(stream, index=False, date_format='%d.%m.%Y')
    response = StreamingResponse(
        iter([stream.getvalue()]),
        media_type="text/csv"
    )
    response.headers["Content-Disposition"] = "attachment; filename=transformed.csv"
    return response
