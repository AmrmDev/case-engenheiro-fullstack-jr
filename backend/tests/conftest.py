import os
import pytest
from fastapi.testclient import TestClient

# Seta ANTES de qualquer import da app
os.environ["TEST_DATABASE_URL"] = "sqlite:///./test.db"

import app.database as db_module
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Substitui o engine diretamente no módulo
test_engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
db_module.engine = test_engine
db_module.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

from app.database import Base, get_db
from app.main import app

Base.metadata.create_all(bind=test_engine)

@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c