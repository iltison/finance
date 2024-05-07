import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, registry

metadata = sa.MetaData()
mapper_registry = registry(metadata=metadata)
Base = declarative_base()
