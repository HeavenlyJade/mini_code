import os
from tempfile import NamedTemporaryFile


def create_tmp_file_for_workbook(workbook):
    need_delete = True if os.name == 'posix' else False

    tmp = NamedTemporaryFile(delete=need_delete)
    workbook.save(tmp.name)
    tmp.seek(0)
    return tmp
