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

def create_cafe_object(obj):
    cafe =  {
        "id": obj.id, 
        "name": obj.name, 
        "image_url": obj.img_url,
        "location": obj.location, 
        "map_url": obj.map_url,
        "seats": obj.seats,
        "coffee_price": obj.coffee_price,
        "can_take_calls": obj.can_take_calls,
        "has_sockets": obj.has_sockets,
        "has_toliets": obj.has_toilet,
        "has_wifi": obj.has_wifi
    }

    return cafe


@app.route("/")
def home():
    return render_template("index.html")

# HTTP GET - Read Record
@app.route("/random")
def random_cafe():
    num_cafes = db.session.execute(db.select(Cafe)).scalars().all()
    random_id = randint(1, len(num_cafes))

    random_cafe = db.get_or_404(Cafe, random_id)

    return jsonify(cafe=create_cafe_object(random_cafe))

# HTTP GET - Read all Cafes
@app.route("/all")
def cafes():
    cafe_arr = []
    list_of_cafes = db.session.execute(db.select(Cafe)).scalars().all()

    for cafe in list_of_cafes:
        cafe_arr.append(create_cafe_object(cafe))

    return jsonify(cafes=cafe_arr)

# HTTP GET - Find a location 
@app.route('/search')
def find_cafe():
    location = request.args['loc']
    cafe_arr = []
    cafe_locations = db.session.execute(db.select(Cafe).where(Cafe.location == location)).scalars().all()

    if len(cafe_locations) == 0:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."})

    for cafe in cafe_locations:
        cafe_arr.append(create_cafe_object(cafe))

    return jsonify(cafes=cafe_arr)

# HTTP POST - Create Record
@app.route("/add", methods=['POST'])
def add_cafe():
    new_cafe = Cafe(
        name = request.form['name'],
        map_url = request.form['map_url'],
        img_url = request.form['img_url'],
        location = request.form['location'],
        seats = request.form['seats'],
        has_toilet = bool(request.form['has_toilet']),
        has_wifi = bool(request.form['has_wifi']),
        has_sockets = bool(request.form['has_sockets']),
        can_take_calls = bool(request.form['can_take_calls']),
        coffee_price = request.form['coffee_price']
    )

    db.session.add(new_cafe)
    db.session.commit()

    return jsonify(response={"success": "Successfully added the new cafe."})

# HTTP PUT/PATCH - Update Record
@app.route('/update-price/<int:cafe_id>', methods=['PATCH'])
def update_price(cafe_id):
    try:
        cafe = db.get_or_404(Cafe, cafe_id) 
        cafe.coffee_price = request.form['new_price']
        db.session.commit()
    except:
        return jsonify(error={"Not Found": "Sorry, a cafe with that id was not found in the database."}), 404

    return jsonify(success="Successfully updated the price.")

# HTTP DELETE - Delete Record
@app.route("/report-closed/<int:cafe_id>", methods=['DELETE'])
def cafe_closed(cafe_id):

    if request.args['api_key'] != 'TopSecretAPIKey':
        return jsonify(error="Sorry, you are not authorized to delete data from the database."), 403

    try:
        cafe = db.get_or_404(Cafe, cafe_id) 
        db.session.delete(cafe)
        db.session.commit()
    except:
        return jsonify(error={"Not Found": "Sorry, a cafe with that id was not found in the database."}), 404

    return jsonify(success="Successfully deleted the cafe from the database.")

if __name__ == '__main__':
    app.run(debug=True)
