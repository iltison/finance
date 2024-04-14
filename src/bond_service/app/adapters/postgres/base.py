import sqlalchemy as sa
from sqlalchemy.orm import registry

metadata = sa.MetaData()
mapper_registry = registry(metadata=metadata)
