from typing import List, Dict, Any

from fastapi import UploadFile
from xlrd import open_workbook


from ...config import settings
from .schemas import DocumentInformation


def read_collection(xls: UploadFile) -> List[DocumentInformation]:
    """Get some information about a FESAD document (DU-Key and, if possible, title)  from the xls file exported by FESAD"""
    with xls.file as file:
        # read to xls file as a list
        # where each item is a dict
        # representing a row, which values can be accessed by
        # column names as keys

        content = file.read()
        workbook = open_workbook(file_contents=content)
        sheet = workbook.sheet_by_index(0)

        # the xls exported by FESAD stores the header data in the second row
        header_row = 1
        column_names: List[str] = [
            str(sheet.cell(header_row, col_index).value)
            for col_index in range(sheet.ncols)
        ]
        items: List[Dict[str, Any]] = []
        for row_index in range(1, sheet.nrows):
            item = {}
            for col_index in range(sheet.ncols):
                item[column_names[col_index]] = sheet.cell(row_index, col_index).value
            items.append(item)

    document_informations: List[DocumentInformation] = list()

    for item in items[1:]:
        du_key = item.get("DU-Key", None)
        if du_key is None:
            continue
        du_key = int(du_key)

        titles = list()
        # we are only interested in the first two title parts
        for i in range(1, 3):
            title = item.get(f"Titel {i}", "").strip()
            if title != "":
                titles.append(str(title.strip()))
        # no title? use label if possible
        title_is_empty = all((title == "" for title in titles))
        if len(titles) == 0 or title_is_empty:
            label = item.get("label", "").strip()
            if label != "":
                titles.append(str(label))
            else:
                # still no title? set default value
                titles.append("unbekannt")

        title = ": ".join(titles)
        document_information = DocumentInformation(du_key=du_key, name=title)
        document_informations.append(document_information)

    return document_informations
