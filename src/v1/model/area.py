import sqlalchemy


metadata = sqlalchemy.MetaData()

subdistrict = sqlalchemy.Table(
    'bc_subdistrict',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('name', sqlalchemy.String(length=255)),
    sqlalchemy.Column('district_id', sqlalchemy.Integer),
    sqlalchemy.Column('legacy_id', sqlalchemy.String(length=20), nullable=True),
)

subdistrict_zipcode = sqlalchemy.Table(
    'bc_subdistrict_zipcode',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('subdistrict_id', sqlalchemy.Integer),
    sqlalchemy.Column('zipcode', sqlalchemy.Integer),
    sqlalchemy.Column('zipcode_id', sqlalchemy.Integer),
)

zipcode = sqlalchemy.Table(
    'bc_zipcode',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('zip_code', sqlalchemy.Integer),
)