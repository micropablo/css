# Reserva project on Docker (Ubuntu 24.04)

This repository replicates your VM setup using Docker with an Ubuntu 24.04 container running Apache + PHP.

## Prerequisites
- Docker Engine
- Docker Compose plugin

## Project structure
- `Dockerfile`: Ubuntu 24.04 + Apache + PHP image
- `docker-compose.yml`: local orchestration
- `reserva/clientForm.html`: reservation form
- `reserva/formValidation.php`: form processing and validation

## Run the project
```bash
docker compose up --build -d
```

Open in browser:
- Form: `http://localhost:8080/reserva/clientForm.html`

## Stop the project
```bash
docker compose down
```
