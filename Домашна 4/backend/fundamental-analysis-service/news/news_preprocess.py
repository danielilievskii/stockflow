import pandas as pd
from models.news import CompanyNewsData

def preprocess_data(data: pd.DataFrame, company_name, db):
    cyrillic_data = data[data['content'].str.contains('[а-шА-Ш]', regex=True)]
    cyrillic_ids = cyrillic_data['id'].tolist()

    data = data[~data['content'].str.contains('[а-шА-Ш]', regex=True)]

    data = data.sort_values(by='date')
    data = data.set_index("date")

    # Remove corrupted data in database
    if cyrillic_ids:
        db.query(CompanyNewsData).filter(
            CompanyNewsData.company == company_name,
            CompanyNewsData.id.in_(cyrillic_ids)
        ).delete(synchronize_session=False)
        db.commit()

    return data


