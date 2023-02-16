FROM python:3.9

COPY . my_project/

WORKDIR /my_project

RUN apt-get update
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]
