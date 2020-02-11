#FROM pytorch/pytorch:0.4.1-cuda9-cudnn7-runtime
FROM pytorch/pytorch:1.1.0-cuda10.0-cudnn7.5-runtime
#RUN apt-get update && apt-get -y install build-essential && apt-get -y install python3.5

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

#RUN pip install numpy==1.16.gcc#4 numpydoc==0.8.0
RUN pip install cymem==2.0.2 cython==0.29.12 cytoolz==0.9.0.1 allennlp


# Make port 80 available to the world outside this container
#EXPOSE 80

# Run app.py when the container launches
CMD ["python" "/app/src/main.py" "test" "--model-path-base" "/app/models/en_charlstm_dev.93.61.pt" "--test-path /app/data/penn-tree-bank/23.auto.clean"] 
