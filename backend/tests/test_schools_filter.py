import pytest
from app.db.database import SessionLocal
from app.models.school import School
from app.models.program import Program

@pytest.fixture(autouse=True)
def seed_test_schools():
    with SessionLocal() as db:
        # Create Public School
        s1 = School(
            name="Université de Yaoundé I",
            city="Yaoundé",
            location="Ngoa-Ekellé, Yaoundé",
            institution_type="public",
            description="Leading public university"
        )
        db.add(s1)
        db.flush()

        p1 = Program(
            school_id=s1.id,
            field_of_study="Informatique",
            degree_type="Licence",
            duration="3 years",
            language_of_instruction="French",
            delivery_mode="On-Campus",
            tuition_fee="50,000 FCFA / year"
        )
        db.add(p1)

        # Create IPES School
        s2 = School(
            name="The ICT University",
            city="Yaoundé",
            location="Messassi, Yaoundé",
            institution_type="ipes",
            description="American-style private university"
        )
        db.add(s2)
        db.flush()

        p2 = Program(
            school_id=s2.id,
            field_of_study="Software Engineering",
            degree_type="Bachelor",
            duration="3 years",
            language_of_instruction="English",
            delivery_mode="Hybrid",
            tuition_fee="730,000 FCFA / year"
        )
        db.add(p2)
        db.commit()

def test_list_schools_basic(client):
    response = client.get("/api/schools")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    first = data[0]
    assert "id" in first
    assert "name" in first
    assert "institution_type" in first
    assert "city" in first
    assert "programs" in first

def test_filter_institution_type_public(client):
    response = client.get("/api/schools?institution_type=public")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Université de Yaoundé I"
    assert data[0]["institution_type"] == "public"

def test_filter_institution_type_ipes(client):
    response = client.get("/api/schools?institution_type=ipes")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "The ICT University"
    assert data[0]["institution_type"] == "ipes"

def test_filter_city(client):
    response = client.get("/api/schools?city=Yaoundé")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_filter_field_of_study(client):
    response = client.get("/api/schools?field_of_study=Software")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "The ICT University"

def test_filter_degree_type(client):
    response = client.get("/api/schools?degree_type=Bachelor")
    assert response.status_code == 200
    data = response.json()
    # "Bachelor" matches both Bachelor and Licence per degree category mapping
    assert len(data) == 2

def test_filter_tuition_range(client):
    response = client.get("/api/schools?max_tuition=600000")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1

def test_filter_language(client):
    response = client.get("/api/schools?language_of_instruction=English")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "The ICT University"

def test_filter_delivery_mode(client):
    response = client.get("/api/schools?delivery_mode=Hybrid")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "The ICT University"

def test_general_search(client):
    response = client.get("/api/schools?search=Messassi")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "The ICT University"
