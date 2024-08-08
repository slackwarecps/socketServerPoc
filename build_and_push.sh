#!/bin/bash


# Nome da imagem e tags
IMAGE_NAME="fabioalvaro/socketserver"
IMAGE_TAG="v1.0.2"
LATEST_TAG="latest"

# Build do projeto Maven
echo "Construindo o projeto com o Maven..."
#mvn clean install -DskipTests

# Verifique se o build foi bem-sucedido
if [ $? -ne 0 ]; then
  echo "Falha na construção do Maven. Saindo..."
  exit 1
fi

# Build da imagem Docker
echo "Construindo a imagem Docker..."
docker build . -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:${LATEST_TAG}

# Verifique se o build da imagem foi bem-sucedido
if [ $? -ne 0 ]; then
  echo "Falha na construção da imagem Docker. Saindo..."
  exit 1
fi

# Login no Docker Hub (assumindo que as credenciais já estão configuradas)
echo "Fazendo login no Docker Hub..."
docker login

# Verifique se o login foi bem-sucedido
if [ $? -ne 0 ]; then
  echo "Falha no login do Docker. Saindo..."
  exit 1
fi

# Push da imagem para o Docker Hub
echo "Enviando a imagem Docker para o Docker Hub..."
docker push ${IMAGE_NAME}:${IMAGE_TAG}
docker push ${IMAGE_NAME}:${LATEST_TAG}

# Verifique se o push foi bem-sucedido
if [ $? -ne 0 ]; then
  echo "Falha no envio para o Docker Hub. Saindo..."
  exit 1
fi

echo "Imagem Docker enviada com sucesso!"