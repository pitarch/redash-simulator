from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from werkzeug.utils import ArgumentValidationError

from .scenario import Scenario, scenario


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
