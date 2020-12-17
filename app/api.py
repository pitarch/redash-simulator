import http
from typing import Any, Dict, List, Optional

from flask import Flask, json, request

from .scenario import Scenario
from .simulator import Job, simulator

api = Flask(__name__)


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


@api.route("/api/simulator/reset", methods=["POST"])
def reset():
    simulator.reset()
    return "", http.HTTPStatus.NO_CONTENT
