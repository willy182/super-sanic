import sqlalchemy


metadata = sqlalchemy.MetaData()

expeditions = sqlalchemy.Table(
    'bc_expedition',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('available_for', sqlalchemy.String(length=100), nullable=True),
    sqlalchemy.Column('code', sqlalchemy.String(length=10), nullable=True),
    sqlalchemy.Column('coverage', sqlalchemy.String(length=100), nullable=True),
    sqlalchemy.Column('insurance', sqlalchemy.Float, nullable=True),
    sqlalchemy.Column('is_active', sqlalchemy.Boolean, nullable=True, default=False),
    sqlalchemy.Column('name', sqlalchemy.String(length=50), default=False),
    sqlalchemy.Column('priority', sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column('usage_for', sqlalchemy.String(length=100), nullable=False),
)