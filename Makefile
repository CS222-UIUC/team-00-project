# .PHONY: run

# run:
# 	@echo "⏳ Starting LaTeX compile server (Flask) on 5050…"
# 	@cd LaTex_editor_Tectonic_ver && \
# 	  python3 -m backend.server &

# 	@echo "⏳ Starting handwriting classifier (FastAPI) on 7000…"
# 	@cd Final_Handwritting_Recognizer_Model && \
# 	  uvicorn server:app --host 0.0.0.0 --port 7000 --reload &

# 	@echo "⏳ Starting static file server on 9000…"
# 	@cd LaTex_editor_Tectonic_ver && \
# 	  python3 -m http.server 9000 &

# 	@echo "🚀 Starting Django on 8000 (foreground)…"
# 	@cd django-demo-project && \
# 	  python3 manage.py runserver
.PHONY: run

run:
	@echo "Installing local recognizer…"
	@python3 -m pip install -e Final_Handwritting_Recognizer_Model

	@echo "⏳ Starting LaTeX compile server (Flask) on 5050…"
	@cd LaTex_editor_Tectonic_ver && \
	  python3 -m backend.server &

	# @echo "⏳ Starting handwriting classifier (FastAPI) on 7000…"
	# @cd Final_Handwritting_Recognizer_Model && \
	#   uvicorn server:app --host 0.0.0.0 --port 7000 --reload &

	@echo "🚀 Starting Django on 8000 (foreground)…"
	@cd main_project/django-demo-project && \
	  python3 manage.py runserver