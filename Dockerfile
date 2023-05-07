FROM python:3.11.1

ENV DB_NAME=userDB.json
ENV TABLE_NAME=users

WORKDIR /falconcrudapi/falconcrudapi

COPY requirements.txt . 
RUN pip install -r requirements.txt

COPY ./falconcrudapi ./falconcrudapi

CMD ["waitress-serve", "--port=8000", "falconcrudapi.app:app"]