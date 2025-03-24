from app import app, db
from models import Character, Planet, Vehicle

# Crear los datos en el contexto de la aplicación
with app.app_context():
    print("Inicializando base de datos...")

    # ====== CREACIÓN DE PLANETAS ======
    planets = [
        Planet(name="Tatooine", population=200000, climate="arid",
               terrain="desert", diameter=10465),
        Planet(name="Alderaan", population=1000000000, climate="temperate",
               terrain="grasslands", diameter=12500),
        Planet(name="Hoth", population=0, climate="frozen",
               terrain="tundra", diameter=7200),
        Planet(name="Endor", population=100000, climate="temperate",
               terrain="forests", diameter=10200),
        Planet(name="Dagobah", population=2000000000, climate="murky",
               terrain="swamps", diameter=8900),
    ]

    # Insertar planetas solo si no existen
    if not Planet.query.first():
        db.session.add_all(planets)
        db.session.commit()
        print("¡5 planetas de Star Wars agregados exitosamente!")

    # ====== CREACIÓN DE VEHÍCULOS ======
    vehicles = [
        Vehicle(name="X-wing", model="T-65 X-wing", manufacturer="Incom Corporation", vehicle_class="Starfighter",
                cost_in_credits=149999, length=12, crew=1, passengers=0, cargo_capacity=110, max_atmosphering_speed=1050, consumables="1 week"),
        Vehicle(name="TIE Fighter", model="TIE Fighter", manufacturer="Sienar Fleet Systems", vehicle_class="Starfighter",
                cost_in_credits=75000, length=8, crew=1, passengers=0, cargo_capacity=65, max_atmosphering_speed=1200, consumables="2 days"),
        Vehicle(name="Imperial Shuttle", model="Lambda-class T-4a Shuttle", manufacturer="Sienar Fleet Systems", vehicle_class="Transport",
                cost_in_credits=240000, length=20, crew=6, passengers=20, cargo_capacity=80000, max_atmosphering_speed=850, consumables="2 months"),
        Vehicle(name="AT-AT", model="All Terrain Armored Transport", manufacturer="Kuat Drive Yards", vehicle_class="Walker",
                cost_in_credits=5000, length=22, crew=5, passengers=40, cargo_capacity=1000, max_atmosphering_speed=60, consumables="None"),
        Vehicle(name="Slave I", model="Firespray-31", manufacturer="Kuat Systems Engineering", vehicle_class="Firespray-31-class patrol and attack craft",
                cost_in_credits=5000, length=21.5, crew=1, passengers=6, cargo_capacity=70000, max_atmosphering_speed=1000, consumables="1 month"),
    ]

    # Insertar vehículos solo si no existen
    if not Vehicle.query.first():
        db.session.add_all(vehicles)
        db.session.commit()
        print("¡5 vehículos de Star Wars agregados exitosamente!")

    # ====== CREACIÓN DE PERSONAJES ======
    characters = [
        Character(name="Luke Skywalker", gender="male", height=172, mass=77, eye_color="blue", hair_color="blond",
                  skin_color="fair", birth_year="19BBY", homeworld_id=1),
        Character(name="Chewbacca", gender="male", height=202, mass=136, eye_color="blue", hair_color="none",
                  skin_color="dark", birth_year="200BBY", homeworld_id=2),
        Character(name="Leia Organa", gender="female", height=150, mass=49, eye_color="brown", hair_color="brown",
                  skin_color="light", birth_year="47BBY", homeworld_id=3),
        Character(name="Darth Vader", gender="male", height=175, mass=80, eye_color="yellow", hair_color="black",
                  skin_color="pale", birth_year="41.9BBY", homeworld_id=4),
        Character(name="Padmé Amidala", gender="female", height=165, mass=54, eye_color="brown", hair_color="brown",
                  skin_color="light", birth_year="21BBY", homeworld_id=5),
    ]

    # Insertar personajes solo si no existen
    if not Character.query.first():
        db.session.add_all(characters)
        db.session.commit()
        print("¡5 personajes de Star Wars agregados exitosamente!")

print("Base de datos inicializada correctamente.")
