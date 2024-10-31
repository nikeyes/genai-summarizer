import click
from meeting_minutes.meeting_minutes_sumarizer import Summarizer

@click.command()
@click.option("--transcription", type=str, default='src/_tmp/transcription.txt', help="Ruta al fichero de la transcripción") 
@click.option("--summary-language", type=str, default='Spanish', help="Idioma del resumen")
def main_meeting_minutes(transcription: str, summary_language: str):
    summarizer = Summarizer()
    summary = summarizer.summarize(transcription, summary_language)
    print(summary)

if __name__ == "__main__":
    main_meeting_minutes()
