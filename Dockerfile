FROM python:3.7
COPY . .
RUN pip install -r requirements.txt
CMD ['bash','ls -l']
#ENTRYPOINT ['python','aa-cloud-demo/main.py']