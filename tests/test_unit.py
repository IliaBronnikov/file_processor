import pytest
from openpyxl import load_workbook

from src.services import (
    get_column_location,
    get_x_value,
    ExcelColumn,
)


@pytest.fixture()
def workbook():
    return load_workbook("test_files/test.xlsx")


def test_get_column_location(workbook):
    before_column = get_column_location("before", workbook)

    assert before_column.column_name == "C"
    assert before_column.sheet_name == "sheet2"


def test_get_x_values(workbook):
    before_column_info = ExcelColumn(sheet_name="sheet2", column_name="C")
    after_column_info = ExcelColumn(sheet_name="sheet2", column_name="D")
    result = get_x_value(workbook, before_column_info, after_column_info)

    assert result == "removed: 4"
