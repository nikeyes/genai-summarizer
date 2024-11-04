from unittest import TestCase
import os
from transcription.transcription_extractor import TranscriptionExtractor
from helpers.config import TMP_FOLDER


class TestTranscriptionExtractor(TestCase):
    def test_get_transcription_file_name_youtube_watch(self):
        transcription_extractor = TranscriptionExtractor()
        url = "https://www.youtube.com/watch?v=w3Q-_i6KSH4"
        expected = os.path.join(TMP_FOLDER, 'w3Q-_i6KSH4.txt')
        actual = transcription_extractor.get_transcription_file_name(url)
        assert actual == expected

    def test_get_transcription_file_name_youtube_embed(self):
        transcription_extractor = TranscriptionExtractor()
        url = "https://youtube.com/embed/w3Q-_i6KSH4"
        expected = os.path.join(TMP_FOLDER, 'w3Q-_i6KSH4.txt')
        actual = transcription_extractor.get_transcription_file_name(url)
        assert actual == expected

    def test_get_transcription_file_name_youtube_v(self):
        transcription_extractor = TranscriptionExtractor()
        url = "https://youtube.com/v/w3Q-_i6KSH4"
        expected = os.path.join(TMP_FOLDER, 'w3Q-_i6KSH4.txt')
        actual = transcription_extractor.get_transcription_file_name(url)
        assert actual == expected

    def test_get_transcription_file_name_youtu_be(self):
        transcription_extractor = TranscriptionExtractor()
        url = "https://youtu.be/w3Q-_i6KSH4"
        expected = os.path.join(TMP_FOLDER, 'w3Q-_i6KSH4.txt')
        actual = transcription_extractor.get_transcription_file_name(url)
        assert actual == expected

    def test_get_transcription_file_name_audio(self):
        transcription_extractor = TranscriptionExtractor()
        filename = "example_mp3.mp3"
        expected = os.path.join(TMP_FOLDER, 'example_mp3.mp3.txt')
        actual = transcription_extractor.get_transcription_file_name(filename)
        assert actual == expected

    def test_get_transcription_file_name_video(self):
        transcription_extractor = TranscriptionExtractor()
        filename = "example_mp4.mp4"
        expected = os.path.join(TMP_FOLDER, 'example_mp4.mp4.txt')
        actual = transcription_extractor.get_transcription_file_name(filename)
        assert actual == expected
