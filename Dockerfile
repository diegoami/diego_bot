FROM python:3.6-slim
#
ENV DIEGO_BOT_DOCKER="YES" \
    DIEGO_BOT_HOME=/app \
    DIEGO_BOT_PYTHON_PACKAGES=/usr/local/lib/python3.6/dist-packages

RUN apt-get update -qq \
    && apt-get install -y --no-install-recommends build-essential git-core \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR ${DIEGO_BOT_HOME}

COPY . ${DIEGO_BOT_HOME}
COPY ./data ${DIEGO_BOT_HOME}/data
COPY ./config ${DIEGO_BOT_HOME}/config

RUN mkdir -p models/nlu

RUN pip install -r requirements_nc.txt

RUN python -m spacy download en

RUN python -m rasa_nlu.train -c config/config_spacy.json -d data/diego.md --path models/nlu --fixed_model_name current_nc

RUN python -m rasa_core.train -s data/stories.md -d domain.yml -o models/dialogue --epochs 200

VOLUME ["/app/projects", "/app/logs", "/app/models/"]

EXPOSE 5004

CMD ["python","simple_web_bot.py","--fixed_model_name", "current_nc"]