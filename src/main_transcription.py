import click
from typing import Optional
from transcription.transcription_extractor import TranscriptionExtractor

@click.command()
@click.option("--url", type=str, required=True, help="URL del contenido a resumir")
@click.option("--context", type=str, required=False, help="Contexto adicional para la transcripción")
@click.option("--language", type=str, required=False, default='es', help="Idioma del contenido")
@click.option("--output-filename", type=str, required=False, default='', help="Fichero con la transcripción")
def main_transcription(url: str, context: Optional[str], language: str, output_filename: Optional[str]) -> None:
    transcription_extractor = TranscriptionExtractor()
    transcription_extractor.extract(url, context, language, output_filename)

if __name__ == "__main__":
    main_transcription()