import click
from questions.questions_and_answers import QuestionsAndAnswers

@click.command()
@click.option("--transcription", type=str, default='src/_tmp/transcription.txt', help="Ruta al fichero de la transcripción")
@click.option("--question", type=str, required=True, help="La pregunta que se desea hacer")
@click.option("--response-language", type=str, default='Spanish', help="Idioma de las respuestas")
def main_questions(transcription, question, response_language):
    qa = QuestionsAndAnswers()
    print(qa.ask_things(transcription, response_language, question))

if __name__ == "__main__":
    main_questions()
