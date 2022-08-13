version: "3.9"
services:
  postgres:
    image: postgres:14.3
    environment:
      POSTGRES_DB: "test"
      POSTGRES_USER: "docker"
      POSTGRES_PASSWORD: "1111"
      PGDATA: "/var/lib/postgresql/data/pgdata"
    volumes:
      - ../2. Init Database:/docker-entrypoint-initdb.d
      - .:/var/lib/postgresql/data
    ports:
      - "5432:5432"
APP_SETTINGS=config.DevelopmentConfig


docker run --name some-postgres -p 5432:5432 -e POSTGRES_PASSWORD=1111 -d postgres