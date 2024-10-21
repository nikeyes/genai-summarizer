# PoC genai-summarizer
Resume tus videos, audios o documentos


# PoC - sample
```bash
poetry run python src/transcription_extractor.py --url https://www.youtube.com/watch\?v\=w3Q-_i6KSH4

poetry run python src/summarizer.py 

poetry run python src/questions_and_answers.py --question "Crea una lista con los juegos."

poetry run python src/cleaner.py 
```
# Pendiente
- Pendiente de anñadir logging
- Pendiente de crear tests
- Pendiente de refactorizar para usar un patron estrategia:
    - Elegir proveedor de transcripción
    - Elegir proveedor de LLM
- Crear un main con parámetros para llamarlo desde la consola

## Ahora funciona con
- Groq API para acceder a Whisper para las transcripciones de audio a texto (necesitas API key en variable de entorno - GROQ_API_KEY )
- Amazon Bedrock como backend para acceder a LLMs (Necesitas un profile de AWS y uso Claude) 
- ffmpeg para comprimir el audio antes de enviarlo a Groq (tienes que tenerlo instalado en local)
