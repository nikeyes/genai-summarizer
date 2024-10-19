# PoC genai-summarizer
Resume tus videos, audios o documentos

# PoC
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
