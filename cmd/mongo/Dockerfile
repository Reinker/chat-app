FROM mongo:latest
COPY ./mongojs/createUser.js /docker-entrypoint-initdb.d/
COPY ./test-data /tmp/
EXPOSE 27017
CMD ["mongod", "--auth"]
