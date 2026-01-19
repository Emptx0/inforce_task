from src.db import engine, Base


Base.metadata.create_all(bind=engine)
print("DB initialized")
