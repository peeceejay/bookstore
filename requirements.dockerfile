# creates a layer from the ubuntu:16.04 Docker image 
FROM ubuntu:16.04
# adds files from the Docker client’s current directory
COPY . /app
# builds the application with make 
RUN make /app
# specifies what command to run within the container
CMD pip3 install spacy
CMD python3 -m spacy download en_core_web_md