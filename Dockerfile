FROM python:3.12

# 
WORKDIR /code

# 
COPY ./requirements.txt requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 
COPY ./src src

WORKDIR src
# 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000","--loop", "asyncio"]