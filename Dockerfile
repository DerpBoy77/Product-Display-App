FROM python:alpine
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY data/images/.gitkeep ./data/images/.gitkeep
COPY .streamlit ./.streamlit

EXPOSE 8501
CMD ["streamlit", "run", "src/streamlit_app.py", "--server.port=8501"]