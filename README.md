# TRAIN RASA_NLU

Train
```
python -m rasa_nlu.train -c config/config_spacy.json -d data/diego.md --path models/nlu --fixed_model_name current_sp
```

Evaluate
```
python -m rasa_nlu.evaluate -c config/config_spacy.json -d data/diego.md -m models/nlu/default/current_sp```
```

# START RASA_NLU SERVER

Start

```
python -m rasa_nlu.server -c config/config_spacy.json --path models/nlu/
```

Access with this query

```
curl -XPOST localhost:5000/parse -d '{"q":"bye", "model" : "current_sp"}'
```


# TRAIN RASA_CORE

Train core

```
python -m rasa_core.train -s data/stories.md -d domain.yml -o models/dialogue --epochs 200
```

# RUN RASA_CORE

Command line

```
python -m rasa_core.run -d models/dialogue -u models/nlu/default/current_sp --debug
```

Server

```
python simple_web_bot.py --fixed_model_name current_sp
```

Query

```
curl -H "Content-Type: application/json" -X POST localhost:5005/chat/ -d '{ "sender": "default", "message": "Hello"}'
```

# DOCKER

```
docker build -t diego-bot-base --file Dockerfile_base .
docker build -t diego-bot-modelrun --file Dockerfile_modelrun .
docker run -p 5004:5004 diego-bot-modelrun
```
