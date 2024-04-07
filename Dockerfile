
FROM python:3.10.8

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/.


# CMD ["sh", "-c", "python3 -m unittest discover && python3 main.py"]
CMD ["python3","main.py"]