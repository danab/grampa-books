# FROM python:3.7

# ENV PROJECT_NAME api-isp
# ENV PROJECT_DIR /usr/local/src/${PROJECT_NAME}

# WORKDIR ${PROJECT_DIR}

# RUN pip install pipenv 

# COPY ./Pipfile ./Pipfile.lock ${PROJECT_DIR}/

# RUN ls

# EXPOSE 80

# COPY ./src /app

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

FROM python:3.8.2-slim-buster

WORKDIR /opt/api

RUN pip install pipenv 

COPY ./Pipfile.lock  /opt/api
COPY ./Pipfile  /opt/api

RUN pipenv install --system --deploy

COPY ./docker-entrypoint.sh /opt/api
COPY ./src /opt/api/src

# Remove carriage returns (developing from a WIN based system)
RUN sed -i -e 's/\r$//' /opt/api/docker-entrypoint.sh && chmod +x /opt/api/docker-entrypoint.sh


EXPOSE 5042

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD [""]
