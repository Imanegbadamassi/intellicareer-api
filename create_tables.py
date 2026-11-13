from app.core.database import Base, engine
import app.models

Base.metadata.create_all(engine)
print("Tables créées")