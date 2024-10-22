from typing import Any, Dict, List, NotRequired, Optional, TypedDict, Union

type DatasetData = List[Union[int, float, str]]


class Dataset(TypedDict):
    data: DatasetData
    label: NotRequired[Optional[str]]
    order: NotRequired[Optional[int]]
    parsing: NotRequired[Optional[Union[Dict[str, Any], bool]]]
    fill: NotRequired[Optional[bool]]
    borderColor: NotRequired[Optional[str]]
    lineTension: NotRequired[Optional[float]]


class ChartData(TypedDict):
    labels: List[str]
    datasets: List[Dataset]


class ChartOptions(TypedDict):
    type: str
    data: ChartData
    options: Dict[str, Any]


def chart(options: ChartOptions) -> ChartOptions:
    return options
