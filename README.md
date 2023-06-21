# Coffee_shop - FastAPI Web App

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
Simple API, implementing the functionality of an online store, created with FastAPI, PostgreSQL, MongoDB, Docker.
P.S In the future, it is planned to develop the frontend part of the application using react

Functional:
- Show information about product;
- JWT authentification;
- User can add and remove products to his cart.

## Technologies
- FastAPI
- Sqlachemy v.2
- Alembic
- Beanie
- Pydantic

## Setup
Docker-compose was used to quickly deploy the application. To deploy this app you need:
- copy repo
- Then run this command:
```
  docker-compose up --build
```
If you need to kill application, run  this command:
```
  docker-compose down --volumes
```








