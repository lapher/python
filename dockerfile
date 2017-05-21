FROM python:3.6.1
RUN pip install requests
RUN pip install beautifulsoup4 
RUN pip install lxml
RUN pip install selenium
WORKDIR /home
CMD ["python","SeleniumJS.py"]