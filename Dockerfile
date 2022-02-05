FROM python:3.7.3
 
RUN mkdir /application
WORKDIR "/application"

ADD requirements.txt /application/
ADD app/main.py /application/

RUN pip install -r /application/requirements.txt
 
ENTRYPOINT ["python", "main.py"]