FROM python:3.10.6
WORKDIR /VCMS_API

# COPY ./app /VCMS_API/app
COPY app /VCMS_API/app
COPY requirements.txt /VCMS_API
RUN pip install -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]