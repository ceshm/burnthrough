# BurnThrough

Task management system. live demo at <a href="https://burnthrough.ceshm.com" target="_blank">burnthrough.ceshm.com</a>


## Functionalities
 - Add and move around tasks in a tree structure
 - Estimate time for each task
 - Register time spent on each task
 - Keep track of the burndown of each node (not impleneted yet)
 - Keep track of your weekly throughput (not impleneted yet)


## Requirements

#### Python >= 3.6

Developed using:
- Python 3.7.1
- Starlette 0.12.9
- uvicorn 0.9.0
- Jinja 2.10.1


## Project configuration

Add a config.json file at the root folder, with the following structure:

```json
{
  "database": {
    "name": "",
    "user": "",
    "password": "",
    "host": "127.0.0.1",
    "port": 5432
  }
}
```

## Run initial migration
```
$ python initial_migration.py
```

## Running
Start the server, using the uvicorn command:
```
$ uvicorn burnthrough:app --port 3000
```
