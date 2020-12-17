from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

now = datetime.now()

mapping: Dict[str, int] = {
    "latest_availability_data_id": 11,
    "mean_revenue": 2,
    "app_hash_id": 3,
    "ad_unit": 4,
    "ad_unit_country": 5,
    "ad_unit_country_app": 6,
}
rows_data: Dict[str, Optional[List[Dict[str, Any]]]] = {
    "latest_availability_data_id": [
        {
            "latest": f"{now.date().isoformat()} {now.time().replace(microsecond=0).isoformat()}"
        }
    ],
    "mean_revenue": [{"mean_revenue": 1.23}],
    "app_hash_id": [{"name": "foocka2"}, {"name": "foocka1"}],
    "ad_unit": [
        {"net_revenue_per_million": 5.1, "ad_unit": "banner"},
        {"net_revenue_per_million": 4.23, "ad_unit": "video"},
    ],
    "ad_unit_country": [
        {
            "ad_unit": "banner",
            "country": "US",
            "net_revenue_per_million": 2.1,
            "instances": 8141107,
        },
        {
            "ad_unit": "video",
            "country": "GB",
            "net_revenue_per_million": 1.8408565733825668,
            "instances": 3893404,
        },
    ],
    "ad_unit_country_app": [
        {
            "ad_unit": "banner",
            "country": "US",
            "net_revenue_per_million": 1.453569696001622,
            "name": "app1",
            "instances": 4367329,
        },
        {
            "ad_unit": "video",
            "country": "GB",
            "net_revenue_per_million": 1.453569696001622,
            "name": "app1",
            "instances": 4367329,
        },
        {
            "ad_unit": "video",
            "country": "GB",
            "net_revenue_per_million": 1.453569696001622,
            "name": "app2",
            "instances": 4367329,
        },
        {
            "ad_unit": "banner",
            "country": "US",
            "net_revenue_per_million": 1.453569696001622,
            "name": "app3",
            "instances": 4367329,
        },
        {
            "ad_unit": "banner",
            "country": "US",
            "net_revenue_per_million": 1.453569696001622,
            "name": "app4",
            "instances": 4367329,
        },
    ],
}


@dataclass
class Scenario:
    mapping: Dict[str, int]
    data: Dict[str, Optional[List[Dict[str, Any]]]]


scenario = Scenario(mapping, rows_data)
