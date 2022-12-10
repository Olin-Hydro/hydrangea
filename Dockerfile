FROM python:3.10



# We also copy the required files and folders

COPY ./App /App

# We copy just the requirements.txt first to leverage Docker cache

COPY ./requirements.txt /App/requirements.txt

WORKDIR /App

RUN pip install --no-cache-dir --upgrade -r /App/requirements.txt

ARG PORT
ARG ATLAS_URI
ARG DB_NAME

ENV PORT=$PORT
ENV ATLAS_URI=$ATLAS_URI
ENV DB_NAME=$DB_NAME

RUN echo $ATLAS_URI

RUN printenv

EXPOSE 8000

CMD ["python3", "main.py"]

