import http
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import os

from flask import Flask, json, request
from werkzeug.utils import ArgumentValidationError

from scenario import Scenario, scenario

api = Flask(__name__)

@dataclass
class Job:
    id: str = ""
    query_result_id: Optional[int] = None
    status: int = 1
    error: str = ""
    updated_at: int = 0


class RedashSimulator:
    mappings: Dict[str, int]  # query name to query id mapping
    data: Dict[str, Optional[List[Dict[str, Any]]]]

    def __init__(self, mappings: Optional[Dict[str, int]] = None) -> None:
        self.mappings = {**mappings} if mappings else {}
        self.data = {}

    def reset(self) -> None:
        self.mappings = {}
        self.data = {}

    def upsert_query_result(
        self, query_namid: str, rows: Optional[List[Dict[str, Any]]]
    ) -> None:

        query_id = self.get_query_id_or_raise_exception(query_namid)
        self.data[query_id] = rows

    def get_query_id_or_raise_exception(self, query_namid: str) -> str:
        query_id = self.get_query_id_by_namid(query_namid)
        if query_id is None:
            raise ArgumentValidationError("query id not found")
        return query_id

    def get_query_id_by_name(self, name: str) -> Optional[str]:
        return str(self.mappings[name]) if name in self.mappings else None

    def get_query_id_by_namid(self, namid: str) -> Optional[str]:
        if namid.isnumeric():
            return namid  # if namid in self.query_name_id_map.values() else None
        return self.get_query_id_by_name(namid)

    def get_query_name_by_id(self, query_id: str) -> Optional[str]:
        return next(
            (name for name, id in self.mappings.items() if id == query_id),
            None,
        )

    def get_query_name_by_namid(self, namid: str) -> Optional[str]:
        if namid.isnumeric():
            return self.get_query_name_by_id(namid)

        return namid if namid in self.mappings else None

    def get_query_result(self, query_result_id: str) -> Optional[Dict[str, Any]]:
        if query_result_id in self.data:
            rows = self.data[query_result_id]
            return {"id:": query_result_id, "data": {"rows": rows}, "query_hash": ""}
        return None

    def upsert_rows_data(
        self, query_namid: str, data: Optional[List[Dict[str, Any]]]
    ) -> None:
        query_id = self.get_query_id_or_raise_exception(query_namid)
        self.data[query_id] = data

    def setup_scenario(self, scenario: Scenario) -> None:
        mapping = scenario.mapping
        data_rows = scenario.data
        self.reset()
        for query_name, rows in data_rows.items():
            query_id = mapping[query_name]
            simulator.mappings[query_name] = query_id
            simulator.upsert_query_result(query_name, rows)


simulator = RedashSimulator()
simulator.setup_scenario(scenario)

## ######### ##
## ENDPOINTS ##
## ######### ##


@api.route("/api/simulator/mappings")
def get_simulator_mappings():
    return simulator.mappings


@api.route("/api/simulator/mappings", methods=["POST"])
def post_simulator_mappings():
    mappings = request.json
    print(f"mappings={mappings}")
    if (
        not isinstance(mappings, dict)
        or not all(isinstance(key, str) for key in mappings.keys())
        or not all(isinstance(value, int) for value in mappings.values())
    ):
        return "", http.HTTPStatus.BAD_GATEWAY
    simulator.mappings = request.json
    return "", http.HTTPStatus.ACCEPTED


@api.route("/api/simulator/data")
def get_simulator_data():
    return json.dumps(simulator.data)


@api.route("/api/simulator/data/<query_namid>")
def get_simulator_data_by_query_namid(query_namid: str):
    query_namid = simulator.get_query_id_or_raise_exception(query_namid)
    data = simulator.data[query_namid]
    return json.jsonify(data)


@api.route("/api/simulator/data/<query_namid>", methods=["POST"])
def post_simulator_data(query_namid: str):
    rows_data: Optional[List[Dict[str, Any]]] = request.json
    simulator.upsert_rows_data(query_namid, rows_data)
    return "", http.HTTPStatus.ACCEPTED


@api.route("/api/simulator/query_results/<query_result_id>")
def get_simulator_query_result(query_result_id: str):
    query_id = simulator.get_query_id_by_namid(query_result_id)
    if query_id is None:
        return f"{query_result_id}: no query result found", http.HTTPStatus.FOUND

    return simulator.get_query_result(query_id) or (
        "",
        http.HTTPStatus.NOT_FOUND,
    )


@api.route("/api/simulator/scenario")
def get_simulator_scenario():

    rows = {
        query_name: simulator.data[str(query_id)]
        for query_name, query_id in simulator.mappings.items()
    }
    return json.dumps(Scenario(simulator.mappings, rows))


@api.route("/api/simulator/scenario", methods=["POST"])
def put_simulator_scenario():
    body = request.json
    scenario = Scenario(body["mapping"], body["data"])
    simulator.setup_scenario(scenario)
    return "", http.HTTPStatus.ACCEPTED


@api.route("/api/simulator/scenario", methods=["POST"])
def post_simulator_scenario():
    scn: Dict[str, Optional[List[Dict[str, Any]]]] = request.json
    simulator.data.clear()
    for query_namid, rows in scn.items():
        simulator.upsert_query_result(query_namid, rows)
    return "", http.HTTPStatus.ACCEPTED


@api.route("/api/queries/<query_id>/refresh", methods=["POST"])
def post_query_refresh(query_id: str) -> Dict[str, Any]:
    return {"job": Job(id=query_id, query_result_id=int(query_id), status=1)}


@api.route("/api/jobs/<job_id>")
def get_job(job_id: str) -> Dict[str, Any]:
    return {"job": Job(id=job_id, query_result_id=int(job_id), status=3)}


@api.route("/api/queries/<query_id>/results/<query_result_id>.json")
def get_query_result(query_id: str, query_result_id: str) -> Dict[str, Any]:
    query_result = simulator.get_query_result(query_result_id)
    return {"query_result": query_result}

## Admin endpoints

# @api.route("/api/simulator/query_results/<query_namid>", methods=["POST"])
# def post_simulator_query_result(query_namid: str):
#     query_id = simulator.get_query_id_by_namid(query_namid)
#     if query_id is None:
#         return f"{query_namid}: unable to find the query id", http.HTTPStatus.NOT_FOUND
#     simulator.upsert_query_result(query_id, request.json)
#     return "", http.HTTPStatus.CREATED


@api.route("/api/simulator/reset", methods=["POST"])
def reset():
    simulator.reset()
    return "", http.HTTPStatus.NO_CONTENT


if __name__ == "__main__":
    api.run()
