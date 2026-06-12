COPY news-rag/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY news-rag/ ./