
FROM python:3.10-slim


WORKDIR /app


COPY . .


RUN pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 8501

# Define environment variable for streamlit
ENV STREAMLIT_SERVER_PORT=8501

# Run streamlit app when the container is started
CMD ["streamlit", "run", "app.py"]
