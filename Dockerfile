FROM python:3.11.9
ADD main.py
RUN pip install --no-cache-dir -r requirements.txt
CMD [“python3”, “./main.py”]