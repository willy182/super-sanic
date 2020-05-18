import sqlalchemy

metadata = sqlalchemy.MetaData()

province = sqlalchemy.Table(
    'bc_province',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('name', sqlalchemy.String(length=255)),
)

city = sqlalchemy.Table(
    'bc_city',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('name', sqlalchemy.String(length=255)),
    sqlalchemy.Column('type', sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column('province_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('bc_province.id')),
)

district = sqlalchemy.Table(
    'bc_district',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('name', sqlalchemy.String(length=255)),
    sqlalchemy.Column('city_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('bc_city.id')),
)

subdistrict = sqlalchemy.Table(
    'bc_subdistrict',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('name', sqlalchemy.String(length=255)),
    sqlalchemy.Column('district_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('bc_district.id')),
)

subdistrict_zipcode = sqlalchemy.Table(
    'bc_subdistrict_zipcode',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('subdistrict_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('bc_subdistrict.id')),
    sqlalchemy.Column('zip_code', sqlalchemy.Integer),
)