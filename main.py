from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from random import randint

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random")
def random_cafe():
    num_cafes = db.session.execute(db.select(Cafe)).scalars().all()
    random_id = randint(1, len(num_cafes))

    random_cafe = db.get_or_404(Cafe, random_id)

    cafe = {
        "cafe": {
            "id": random_cafe.id, 
            "name": random_cafe.name, 
            "image_url": random_cafe.img_url,
            "location": random_cafe.location, 
            "map_url": random_cafe.map_url,
            "seats": random_cafe.seats,
            "coffee_price": random_cafe.coffee_price,
            "can_take_calls": random_cafe.can_take_calls,
            "has_sockets": random_cafe.has_sockets,
            "has_toliets": random_cafe.has_toilet,
            "has_wifi": random_cafe.has_wifi
        }
    }

    return jsonify(cafe)

# HTTP GET - Read all Cafes
@app.route("/all")
def cafes():
    cafe_arr = []
    list_of_cafes = db.session.execute(db.select(Cafe)).scalars().all()

    for cafe in list_of_cafes:
        cafe_obj = {
            "id": cafe.id, 
            "name": cafe.name, 
            "image_url": cafe.img_url,
            "location": cafe.location, 
            "map_url": cafe.map_url,
            "seats": cafe.seats,
            "coffee_price": cafe.coffee_price,
            "can_take_calls": cafe.can_take_calls,
            "has_sockets": cafe.has_sockets,
            "has_toliets": cafe.has_toilet,
            "has_wifi": cafe.has_wifi
        }
        cafe_arr.append(cafe_obj)

    all_cafes = {
        "cafes": cafe_arr
    }

    return jsonify(all_cafes)

# HTTP GET - Find a location 
@app.route('/search')
def find_cafe():
    location = request.args['loc']
    cafe_arr = []
    cafe_locations = db.session.execute(db.select(Cafe).where(Cafe.location == location)).scalars().all()

    if len(cafe_locations) == 0:
        error ={
            "error": {
                "Not Found": "Sorry, we don't have a cafe at that location."
            }
        }

        return jsonify(error)

    for cafe in cafe_locations:
        cafe_obj = {
            "id": cafe.id, 
            "name": cafe.name, 
            "image_url": cafe.img_url,
            "location": cafe.location, 
            "map_url": cafe.map_url,
            "seats": cafe.seats,
            "coffee_price": cafe.coffee_price,
            "can_take_calls": cafe.can_take_calls,
            "has_sockets": cafe.has_sockets,
            "has_toliets": cafe.has_toilet,
            "has_wifi": cafe.has_wifi
        }
        cafe_arr.append(cafe_obj)

    all_cafes = {
        "cafes": cafe_arr
    }

    return jsonify(all_cafes)

# HTTP POST - Create Record

# HTTP PUT/PATCH - Update Record

# HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
