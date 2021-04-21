import io
import pandas as pd


def get_or_none(class_, **kwargs):
    try:
        return class_.objects.get(**kwargs)
    except class_.DoesNotExist:
        pass
    except class_.MultipleObjectsReturned:
        return []
    return None


def export_to_excel(df, col_size=None, sheet_name=None):
    if col_size is None:
        col_size = 25
    if sheet_name is None:
        sheet_name = "Sheet 1"

    excel_file = io.BytesIO()
    xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter', options={'remove_timezone': True})
    df.to_excel(xlwriter, sheet_name, index=False)
    worksheet = xlwriter.sheets[sheet_name]
    worksheet.set_column('A:Z', col_size)
    xlwriter.save()
    excel_file.seek(0)
    return excel_file
