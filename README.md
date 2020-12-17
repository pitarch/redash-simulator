# REDASH SIMULATOR

The _Redash Simulator_ is a python application to simulate fake responses of a redash server.
It uses the [flask framework](https://flask.palletsprojects.com/en/1.1.x/).

The simulator manages a set of queries. There will be only one query result for each query.
Every time a query execution is requested, the same job will be returned and its
`job_id` will be the `query_id`. The `query_result_id` for that query execution will be also identified
with the `query_id`.

The simulator manages two data structures:

- mappings between query names to query ids
- data rows for each query

This application is targeted to run as a docker container in the local development laptop and
in staging.

## DEVELOPMENT

- create the virtual environment

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

- run the application

```sh
./run-simulator.sh
```

The application will accept requests at local port 5000.

## DOCKER BUILD

```sh
./build-docker.sh
```

A new image will be created with the name `axonix/redash-simulator`.

## RUN

* To run the docker image:

```sh
./run-docker.sh
```

By default, a docker container of the redash simulator will accept requests at port 5000.

## Endpoint Operations

These are the main endpoints:

- `POST /api/queries/<query_id>/refresh`: apply to run a query identified by a `query_id`. It returns a `job_id`.
- `GET /api/jobs/<job_id>`: get the execution status of job. It returns an `status=1` with the result is ready. The field `query_results_id` contains the `id` of the result.
- `GET /api/queries/<query_id>/results/<query_result_id>.json`: returns the result of a query.

These other endpoints are used to manage the simulator:

- `POST /api/simulator/reset`: resets the simulator.
- `GET /api/simulator/mappings`: gets the list of mappings between query names to query id.
- `POST /api/simulator/mappings`: create a new mapping of query names to query ids.
- `GET /api/simulator/data`: gets all the fake data.
- `GET /api/simulator/data/<query_namid>`: gets the data of a single query identifier by either its name or id.
- `POST /api/simulator/data/<query_namid>`: replace the data of a single query identified by either its name or id.
- `GET /api/simulator/scenario`: get the scenario of fake responses
- `POST /api/simulator/scenario`: set the scenario of fake responses
- `GET /api/simulator/query_results/<query_namid>`: gets the rows data of a query result.

### POST /api/simulator/reset

This operations resets the simulator. So mappings and data rows will be emptied.

```http
HTTP/1.0 204 NO CONTENT
Content-Type: text/html; charset=utf-8
Server: Werkzeug/1.0.1 Python/3.7.3
Date: Thu, 17 Dec 2020 11:04:15 GMT
```

### GET /api/simulator/mappings

This operation returns the list of mappings. Example:

```http
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 154
Server: Werkzeug/1.0.1 Python/3.7.3
Date: Thu, 17 Dec 2020 10:42:05 GMT

{
  "ad_unit": 4,
  "ad_unit_country": 5,
  "ad_unit_country_app": 6,
  "app_hash_id": 3,
  "latest_availability_data_id": 11,
  "mean_revenue": 2
}
```

The query name `ad_unit` is identified with the query id 4.

### POST /api/simulator/mappings

This operation recreates the mappings. Example:

```http
POST /api/simulator/mappings
Content-Type: application/json

{
  "ad_unit": 4,
  "ad_unit_country": 5,
  "ad_unit_country_app": 6,
  "app_hash_id": 3,
  "latest_availability_data_id": 11,
  "mean_revenue": 2,
}
```

### GET /api/simulator/data

This operations returns the list of all data rows. The response body will consists
of a json object having the query_id as the key and the data row as the value. The
query_id is a string in the keys instead of being a number.

Example:

```http
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 1074
Server: Werkzeug/1.0.1 Python/3.7.3
Date: Thu, 17 Dec 2020 10:47:50 GMT

{
  "11": [
    {
      "latest": "2020-12-17 10:41:23"
    }
  ],
  "2": [
    {
      "mean_revenue": 1.23
    }
  ],
  "3": [
    {
      "name": "foocka2"
    },
    {
      "name": "foocka1"
    }
  ],
  "4": [
    {
      "ad_unit": "banner",
      "net_revenue_per_million": 5.1
    },
    {
      "ad_unit": "video",
      "net_revenue_per_million": 4.23
    }
  ],
  "5": [
    {
      "ad_unit": "banner",
      "country": "US",
      "instances": 8141107,
      "net_revenue_per_million": 2.1
    },
    {
      "ad_unit": "video",
      "country": "GB",
      "instances": 3893404,
      "net_revenue_per_million": 1.8408565733825668
    }
  ],
  "6": [
    {
      "ad_unit": "banner",
      "country": "US",
      "instances": 4367329,
      "name": "app1",
      "net_revenue_per_million": 1.453569696001622
    },
    {
      "ad_unit": "video",
      "country": "GB",
      "instances": 4367329,
      "name": "app1",
      "net_revenue_per_million": 1.453569696001622
    },
    {
      "ad_unit": "video",
      "country": "GB",
      "instances": 4367329,
      "name": "app2",
      "net_revenue_per_million": 1.453569696001622
    },
    {
      "ad_unit": "banner",
      "country": "US",
      "instances": 4367329,
      "name": "app3",
      "net_revenue_per_million": 1.453569696001622
    },
    {
      "ad_unit": "banner",
      "country": "US",
      "instances": 4367329,
      "name": "app4",
      "net_revenue_per_million": 1.453569696001622
    }
  ]
}
```

### GET /api/simulator/data/<query_namid>

This operation returns the rows data of a query.

### Example:

request:

```http
GET /api/simulator/data/latest_availability_data_id
```

response:

```http
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 48
Server: Werkzeug/1.0.1 Python/3.7.3
Date: Thu, 17 Dec 2020 13:48:46 GMT

[
  {
    "latest": "2020-12-17 11:16:15"
  }
]
```

### GET /api/simulator/scenario

```http
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 1315
Server: Werkzeug/1.0.1 Python/3.7.3
Date: Thu, 17 Dec 2020 11:16:14 GMT

{
  "data": {
    "ad_unit": [
      {
        "ad_unit": "banner",
        "net_revenue_per_million": 5.1
      }
    ],
    "ad_unit_country": [
      {
        "ad_unit": "banner",
        "country": "US",
        "instances": 8141107,
        "net_revenue_per_million": 2.1
      }
    ],
    "ad_unit_country_app": [
      {
        "ad_unit": "video",
        "country": "GB",
        "instances": 4367329,
        "name": "app2",
        "net_revenue_per_million": 1.453569696001622
      }
    ],
    "app_hash_id": [
      {
        "name": "foocka2"
      }
    ],
    "latest_availability_data_id": [
      {
        "latest": "2020-12-17 11:16:14"
      }
    ],
    "mean_revenue": [
      {
        "mean_revenue": 1.23
      }
    ]
  },
  "mapping": {
    "ad_unit": 4,
    "ad_unit_country": 5,
    "ad_unit_country_app": 6,
    "app_hash_id": 3,
    "latest_availability_data_id": 11,
    "mean_revenue": 2
  }
}
```

### POST /api/simulator/scenario

request:

```http
POST http://{{host}}/api/simulator/scenario
Content-Type: application/json

{
    "data": [...],
    "mapping: {...}
}
```

response:

```http
HTTP/1.0 202 ACCEPTED
Content-Type: text/html; charset=utf-8
Content-Length: 0
Server: Werkzeug/1.0.1 Python/3.7.3
Date: Thu, 17 Dec 2020 11:26:42 GMT
```

### GET /api/simulator/query_results/<query_namid>

This operation returns the redash response for a single query result identified by either a `query_id` or a `query_name`

#### Example

request using the query_id

```http
GET /api/simulator/query_results/2
```

request using the query name:

```http
GET /api/simulator/query_results/mean_revenue
```

response:

```http
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 121
Server: Werkzeug/1.0.1 Python/3.7.3
Date: Thu, 17 Dec 2020 10:57:03 GMT

{
  "data": {
    "rows": [
      {
        "mean_revenue": 1.23
      }
    ]
  },
  "id:": "2",
  "query_hash": ""
}
```
