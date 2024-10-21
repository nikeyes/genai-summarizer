# PoC genai-summarizer
Resume tus videos, audios o documentos


# PoC - Ejemplo para resumir tus video o hacer preguntas sobre su contenido
```bash
poetry run python src/transcription_extractor.py --url https://www.youtube.com/watch\?v\=w3Q-_i6KSH4

poetry run python src/summarizer.py 

poetry run python src/questions_and_answers.py --question "Crea una lista con los juegos."

poetry run python src/cleaner.py 
```
# Pendiente
- Pendiente de añadir logging
- Pendiente mejorar la cobertura de tests
- Pendiente de refactorizar para usar un patron estrategia:
    - Elegir proveedor de transcripción
    - Elegir proveedor de LLM

## Ahora funciona con
- Groq API para acceder a Whisper para las transcripciones de audio a texto (necesitas API key en variable de entorno - GROQ_API_KEY )
- Amazon Bedrock como backend para acceder a LLMs (Necesitas un profile de AWS y uso Claude) 
- ffmpeg para comprimir el audio antes de enviarlo a Groq (tienes que tenerlo instalado en local)

## Covertura
```bash
poetry run pytest -v --cov=src --no-cov-on-fail --cov-report=term-missing tests/
```