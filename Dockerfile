FROM python:3.13
RUN mkdir /opt/app
COPY /dist/data_science_service-1.tar.gz /opt/app
RUN pip install --no-cache-dir /opt/app/data_science_service-1.tar.gz
CMD [ "flask", "run", "--host=0.0.0.0", "--port=8010" ]