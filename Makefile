TRANSCRIPT_FILE = src/_tmp/meeting-minutes.txt

.PHONY: test
test:	
	@ poetry run pytest -v --cov=src --no-cov-on-fail --cov-report=term-missing tests/

.PHONY: meeting-minutes
meeting-minutes: transcribe
	@ poetry run python src/main_meeting_minutes.py --transcription $(TRANSCRIPT_FILE)

.PHONY: ask
ask: transcribe
	@ poetry run python src/main_questions.py --transcription $(TRANSCRIPT_FILE) --question "$(Q)"

.PHONY: transcribe
transcribe:
	@ [ -f $(TRANSCRIPT_FILE) ] || poetry run python src/main_transcription.py --url $(URL) --output-filename $(TRANSCRIPT_FILE)

.PHONY: clean
clean:
	@ poetry run python src/main_cleaner.py