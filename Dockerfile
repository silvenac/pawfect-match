FROM ubuntu:latest

RUN apt-get update && apt-get install python3 python3-pip -y
RUN pip3 install pipenv

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV FLASK_APP pawfect-match.py

RUN mkdir /pawfect/
COPY Pipfile /pawfect/
COPY Pipfile.lock /pawfect/

WORKDIR /pawfect/
RUN pipenv install --deploy --system

# CMD ["flask", "run"]
CMD ["/bin/sh"]
