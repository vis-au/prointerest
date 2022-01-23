from doi_component.sort_component import SortComponent
from doi_component.outlierness_component import OutliernessComponent
from doi_component.density_component import DensityComponent
from doi_component.averageness_component import AveragenessComponent
from doi_component.scagnostics_component import ScagnosticsComponent


def get_doi_component(doi_label: str, numeric_columns: list[str]):
  return DensityComponent(numeric_columns, bandwidth=5) if doi_label == "density"\
    else SortComponent(numeric_columns) if doi_label == "sort"\
    else OutliernessComponent(numeric_columns) if doi_label == "outlierness"\
    else AveragenessComponent(numeric_columns) if doi_label == "averageness"\
    else ScagnosticsComponent(numeric_columns)