FROM python:3.9

WORKDIR /code

ENV VIRTUAL_ENV "/venv"
RUN python -m venv $VIRTUAL_ENV
ENV PATH "$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt /code/requirements.txt
COPY csv_transformator /code/csv_transformator

RUN pip install --no-cache-dir --upgrade -r requirements.txt
CMD ["uvicorn", "csv_transformator.main:app", "--host", "0.0.0.0", "--port", "80"]
