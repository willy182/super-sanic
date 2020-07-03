import sqlalchemy


metadata = sqlalchemy.MetaData()

expeditions = sqlalchemy.Table(
    'bc_expedition',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.String(length=10), unique=True, index=True, primary_key=True),
    sqlalchemy.Column('available_for', sqlalchemy.String(length=100), nullable=True),
    sqlalchemy.Column('code', sqlalchemy.String(length=10), nullable=True),
    sqlalchemy.Column('coverage', sqlalchemy.String(length=100), nullable=True),
    sqlalchemy.Column('created_at', sqlalchemy.TIMESTAMP(timezone=True), nullable=True),
    sqlalchemy.Column('image_url', sqlalchemy.Text, nullable=True),
    sqlalchemy.Column('insurance', sqlalchemy.Float, nullable=True),
    sqlalchemy.Column('is_active', sqlalchemy.Boolean, nullable=True, default=False),
    sqlalchemy.Column('is_enabled', sqlalchemy.Boolean, nullable=True),
    sqlalchemy.Column('modified_at', sqlalchemy.TIMESTAMP(timezone=True), nullable=True),
    sqlalchemy.Column('name', sqlalchemy.String(length=50), default=False),
    sqlalchemy.Column('priority', sqlalchemy.Integer, nullable=True),
    sqlalchemy.Column('usage_for', sqlalchemy.String(length=100), nullable=True),
)