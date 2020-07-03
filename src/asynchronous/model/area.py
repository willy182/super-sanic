import sqlalchemy

metadata = sqlalchemy.MetaData()

province = sqlalchemy.Table(
    'bc_province',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, index=True, unique=True, primary_key=True),
    sqlalchemy.Column('created_at', sqlalchemy.TIMESTAMP(timezone=False), nullable=True),
    sqlalchemy.Column('is_deleted', sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column('island_id', sqlalchemy.Integer, nullable=True),
    sqlalchemy.Column('name', sqlalchemy.String(length=255)),
)

city = sqlalchemy.Table(
    'bc_city',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, unique=True, index=True, primary_key=True),
    sqlalchemy.Column('created_at', sqlalchemy.TIMESTAMP(timezone=False), nullable=True),
    sqlalchemy.Column('is_deleted', sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column('legacy_id', sqlalchemy.String(length=10), nullable=True),
    sqlalchemy.Column('name', sqlalchemy.String(length=255)),
    sqlalchemy.Column('province_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('bc_province.id'), nullable=True),
    sqlalchemy.Column('type', sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column('updated_at', sqlalchemy.TIMESTAMP(timezone=False), nullable=True),
)

district = sqlalchemy.Table(
    'bc_district',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, index=True, unique=True),
    sqlalchemy.Column('city_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('bc_city.id')),
    sqlalchemy.Column('created_at', sqlalchemy.TIMESTAMP(timezone=False), nullable=True),
    sqlalchemy.Column('is_deleted', sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column('legacy_id', sqlalchemy.String(length=20), nullable=True),
    sqlalchemy.Column('name', sqlalchemy.String(length=255)),
    sqlalchemy.Column('updated_at', sqlalchemy.TIMESTAMP(timezone=False), nullable=True),
)

subdistrict = sqlalchemy.Table(
    'bc_subdistrict',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, unique=True, index=True),
    sqlalchemy.Column('created_at', sqlalchemy.TIMESTAMP(timezone=False), nullable=True),
    sqlalchemy.Column('district_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('bc_district.id')),
    sqlalchemy.Column('is_deleted', sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column('legacy_id', sqlalchemy.String(length=20), nullable=True),
    sqlalchemy.Column('name', sqlalchemy.String(length=255)),
    sqlalchemy.Column('updated_a', sqlalchemy.TIMESTAMP(timezone=False), nullable=True),
    sqlalchemy.Column('updated_at', sqlalchemy.Integer, nullable=True),
)

subdistrict_zipcode = sqlalchemy.Table(
    'bc_subdistrict_zipcode',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, unique=True, index=True),
    sqlalchemy.Column('created_at', sqlalchemy.TIMESTAMP(timezone=False)),
    sqlalchemy.Column('subdistrict_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('bc_subdistrict.id')),
    sqlalchemy.Column('updated_at', sqlalchemy.TIMESTAMP(timezone=False), nullable=True),
    sqlalchemy.Column('zip_code', sqlalchemy.Integer),
    sqlalchemy.Column('zipcode_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('bc_zipcode.id'), nullable=True),
)