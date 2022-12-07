FROM python:3.9
RUN pip install flask install flask psycopg2
COPY . /app
WORKDIR /app
EXPOSE 5000
CMD ["flask", "--app", "application.py", "run", "--host=0.0.0.0"]
