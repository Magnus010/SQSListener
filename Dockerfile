FROM apline:edge
RUN apk add --update \
    python \
    python-dev \
    py-pip \
    build-base \
  && pip install virtualenv \
  && rm -rf /var/cache/apk/*
COPY . /SQSListener
WORKDIR /SQSListener
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["SQSListener.py"]