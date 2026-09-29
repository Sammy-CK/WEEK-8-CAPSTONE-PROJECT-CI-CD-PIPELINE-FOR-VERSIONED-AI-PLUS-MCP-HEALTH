FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY prompts/ /app/prompts/
COPY config/ /app/config/
COPY prompt_app.py clinics.json logistics_mcp_versioned.py ./
ENV PROMPT_VERSION=1.2.0
EXPOSE 8000
CMD ["uvicorn", "prompt_app:app", "--host", "0.0.0.0", "--port", "8000"]
