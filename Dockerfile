FROM python:3.12-slim

WORKDIR /app

# Install uv
RUN pip install uv

COPY pyproject.toml requirements.txt .env.example ./
RUN uv pip install --system --no-cache -r requirements.txt

COPY . .

EXPOSE 7860

ENV PORT=7860
ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "environment:app", "--host", "0.0.0.0", "--port", "7860"]
