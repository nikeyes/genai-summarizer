from unittest import TestCase
from assertpy import assert_that

from transcription_extractor import TranscriptionExtractor
from src.cleaner import Cleaner


class TestExtractTranscription(TestCase):
    def tearDown(self) -> None:
        Cleaner()
        return super().tearDown()

    def test_extract_transcription_from_youtube_video_that_has_not_transcription(self):
        info_extractor = TranscriptionExtractor()
        transcription_file, transcription_text = info_extractor.extract(
            filename='https://www.youtube.com/shorts/MwjXxiE9Vh8',
            context='INTELIGENCIA ARTIFICIAL para Mejorar la Ortografía con ChatGPT 🤖 Técnicas para primaria y secundaria',
            audio_language='es',
        )

        assert_that(transcription_file).is_equal_to('src/tmp/transcription.txt')
        assert_that(transcription_file).exists()
        assert_that(transcription_text).is_equal_to(
            ' ¿Te sientes perdido cuando tienes que ayudar a tu hijo o hija con sus deberes? No te preocupes, la inteligencia artificial está aquí para echarte una mano Hoy te enseñamos como usar ChatGPT para ayudar con las asignaturas que más costan en casa como inglés o matemáticas No hace falta ser un experto para ayudarles a aprender Por ejemplo, si necesita apoyo con fracciones equivalentes en cuarto de primaria solo tienes que pedirle a ChatGPT que te genere ejercicios adaptados Además, mira cómo puedes ayudarle a mejorar con los fallos que tenga Corrígeme este ejercicio Le pedimos que nos corrija estos ejercicios en inglés y después que prepare actividades para mejorar los fallos que haya tenido Cada ejercicio se adapta a lo que necesites, ya sea gramática, cálculo o lo que se te ocurra Tú eliges el nivel y la disciplina'
        )

    def test_extract_transcription_from_youtube_video_with_native_transcription(self):
        info_extractor = TranscriptionExtractor()
        transcription_file, transcription_text = info_extractor.extract(
            filename='https://www.youtube.com/watch?v=VTt36VLHmT0',
            context='Necesitamos PATROCINADORES y PARTNERS para seguir AYUDANDO en STEM | ValPat',
            audio_language='es',
        )

        assert_that(transcription_file).is_equal_to('src/tmp/transcription.txt')
        assert_that(transcription_file).exists()
        assert_that(transcription_text).is_equal_to(
            'Hola somos valpat y necesitamos\npatrocinadores para seguir cambiando el\nfuturo danos solo un minuto y te\ncontamos después de 6 años hemos\nalcanzado los 100.000 suscriptores y en\nSolo dos meses mals llegamos a 200.000\nAhora nos ponemos el objetivo de llegar\nal millón de suscriptores para el 2025\npara llegar a ese millón de suscriptores\ny seguir creando contenido de calidad\nnecesitamos apoyo buscamos empresas y\nfundaciones que compartan nuestra visión\ny nos ayuden a llegar a más estudiantes\ncolegios y profesores en nuestro canal\nhemos subido más de 650 vídeos con\nproyectos enseñando robótica\nprogramación y tecnología a jóvenes\ndesde los 5 hasta los 18 años nos\nencanta lo que hacemos hemos dado\ncharlas en varias de las mejores\ncompañías tecnológicas del mundo y nos\nha nombrado dos veces en la prestigiosa\nrevista Forbes nos motiva especialmente\ninspirar y motivar al las niñas a\nsumarse al mundo steam pero nuestro\ncontenido es para todos chicos y chicas\nqueremos que cada Joven se sienta capaz\nde alcanzar sus sueños si conocéis\nalguna persona o organización interesada\nen apoyar o patrocinar proyectos\neducativos como el nuestro ponnos en\ncontacto con vuestra ayuda podemos\nseguir inspirando a la próxima\ngeneración de innovadores Gracias por\nvuestro apoyo y nos vemos en bpa testimo'
        )

    def test_extract_transcription_from_local_video(self):
        info_extractor = TranscriptionExtractor()
        transcription_file, transcription_text = info_extractor.extract(
            filename='tests/integration_tests/valpat_for_test.mp4',
            context='INTELIGENCIA ARTIFICIAL para Mejorar la Ortografía con ChatGPT 🤖 Técnicas para primaria y secundaria',
            audio_language='es',
        )

        assert_that(transcription_file).is_equal_to('src/tmp/transcription.txt')
        assert_that(transcription_file).exists()
        assert_that(transcription_text).is_equal_to(
            ' ¿Te sientes perdido cuando tienes que ayudar a tu hijo o hija con sus deberes? No te preocupes, la inteligencia artificial está aquí para echarte una mano Hoy te enseñamos como usar ChatGPT para ayudar con las asignaturas que más gusten en casa como inglés o matemáticas No hace falta ser un experto para ayudarles a aprender Por ejemplo, si necesita apoyo con fracciones equivalentes en cuarto de primaria solo tienes que pedirle a ChatGPT que te genere ejercicios adaptados Además, mira cómo puedes ayudarle a mejorar con los fallos que tenga Corrígeme este ejercicio Le pedimos que nos corrija estos ejercicios en inglés y después que prepara actividades para mejorar los fallos que haya tenido Cada ejercicio se adapta a lo que necesites, ya sea gramática, cálculo o lo que se te ocurra Tú eliges el nivel y la disciplina'
        )

    def test_extract_transcription_from_local_audio(self):
        info_extractor = TranscriptionExtractor()
        transcription_file, transcription_text = info_extractor.extract(
            filename='tests/integration_tests/valpat_for_test.mp3',
            context='INTELIGENCIA ARTIFICIAL para Mejorar la Ortografía con ChatGPT 🤖 Técnicas para primaria y secundaria',
            audio_language='es',
        )

        assert_that(transcription_file).is_equal_to('src/tmp/transcription.txt')
        assert_that(transcription_file).exists()
        assert_that(transcription_text).is_equal_to(
            ' ¿Te sientes perdido cuando tienes que ayudar a tu hijo o hija con sus deberes? No te preocupes, la inteligencia artificial está aquí para echarte una mano Hoy te enseñamos como usar ChatGPT para ayudar a todas las asignaturas que más gusten en casa como inglés o matemáticas No hace falta ser un experto para ayudarles a aprender Por ejemplo, si necesita apoyo con fracciones equivalentes en cuarto de primaria solo tienes que pedirle a ChatGPT que te genere ejercicios adaptados Además, mira cómo puedes ayudarle a mejorar con los fallos que tenga Corrígeme este ejercicio Le pedimos que nos corrija estos ejercicios en inglés y después que prepara actividades para mejorar los fallos que haya tenido Cada ejercicio se adapta a lo que necesites, ya sea gramática, cálculo o lo que se te ocurra Tú eliges el nivel y la disciplina'
        )