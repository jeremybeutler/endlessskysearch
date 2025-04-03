import os
from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
from dotenv import load_dotenv
import uuid

# Define ship attributes
SHIP_FIELDS = [
    {"name": "faction", "label": "Faction", "type": "text", "required": False},
    {"name": "uncapturable", "label": "Uncapturable", "type": "checkbox", "required": False},
    {"name": "never_disabled", "label": "Never Disabled", "type": "checkbox", "required": True},
    {"name": "name_singular", "label": "Name (Singular)", "type": "text", "required": True},
    {"name": "name_plural", "label": "Name (Plural)", "type": "text", "required": False},
    {"name": "sprite", "label": "Sprite Path", "type": "text", "required": False},
    {"name": "description", "label": "Description", "type": "textarea", "required": False},
]

# Define weapon attributes
WEAPON_FIELDS = [
    {"name": "name", "label": "Weapon Name", "type": "text", "required": False},
    {"name": "comment", "label": "Comment", "type": "textarea", "required": False},
    {"name": "shield_damage", "label": "Shield Damage", "type": "number", "required": False},
    {"name": "hull_damage", "label": "Hull Damage", "type": "number", "required": False},
    {"name": "blast_radius", "label": "Blast Radius", "type": "number", "required": False},
    {"name": "hit_force", "label": "Hit Force", "type": "number", "required": False},
]


# Load environment variables from .env file
load_dotenv()

# Initialize the flask app
app = Flask(__name__)
app.secret_key = os.getenv("SECRET")


# ------------------------ BEGIN FUNCTIONS ------------------------ #
# Function to retrieve DB connection
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_DATABASE")
    )
    return conn

def determine_type(input_value):
    if isinstance(input_value, int):
        return "int"
    elif isinstance(input_value, float):
        return "float"
    elif isinstance(input_value, str):
        return "str"
    else:
        return "ERROR"

def get_all_ships(): ## Eman0202byu ###A function that pulls the view of all ships in database
    # Create a new database connection for each request
    conn = get_db_connection()  # Create a new database connection
    cursor = conn.cursor() # Creates a cursor for the connection, you need this to do queries
    # Query the db
    query = "SELECT name, quantity FROM items"
    cursor.execute(query)
    # Get result and close
    result = cursor.fetchall() # Gets result from query
    conn.close() # Close the db connection (NOTE: You should do this after each query, otherwise your database may become locked)
    return result

def get_ship_param(): ## Eman0202byu ###passed in arg1 = collum_name arg2 = collumn_value
    # Create a new database connection for each request
    conn = get_db_connection()  # Create a new database connection
    cursor = conn.cursor() # Creates a cursor for the connection, you need this to do queries
    # Query the db
    query = "SELECT name, quantity FROM items"
    cursor.execute(query)
    # Get result and close
    result = cursor.fetchall() # Gets result from query
    conn.close() # Close the db connection (NOTE: You should do this after each query, otherwise your database may become locked)
    return result

def get_ship_id(): ## Eman0202byu ###passed in arg1 = SID (Ship ID)
    # Create a new database connection for each request
    conn = get_db_connection()  # Create a new database connection
    cursor = conn.cursor() # Creates a cursor for the connection, you need this to do queries
    # Query the db
    query = "SELECT name, quantity FROM items"
    cursor.execute(query)
    # Get result and close
    result = cursor.fetchall() # Gets result from query
    conn.close() # Close the db connection (NOTE: You should do this after each query, otherwise your database may become locked)
    return result
def create_ship(): ## Eman0202byu ###passed in arg1 = ship obj; return SID
    # Create a new database connection for each request
    conn = get_db_connection()  # Create a new database connection
    cursor = conn.cursor() # Creates a cursor for the connection, you need this to do queries
    # Query the db
    query = "SELECT name, quantity FROM items"
    cursor.execute(query)
    # Get result and close
    result = cursor.fetchall() # Gets result from query
    conn.close() # Close the db connection (NOTE: You should do this after each query, otherwise your database may become locked)
    return result

def update_ship(): ## Eman0202byu ###passed in arg1 = ship obj;
#### Passed in ship obj; grabs SID, updates all values for that SID with the values in arg1;
    #
    # Create a new database connection for each request
    conn = get_db_connection()  # Create a new database connection
    cursor = conn.cursor() # Creates a cursor for the connection, you need this to do queries
    # Query the db
    query = "SELECT name, quantity FROM items"
    cursor.execute(query)
    # Get result and close
    result = cursor.fetchall() # Gets result from query
    conn.close() # Close the db connection (NOTE: You should do this after each query, otherwise your database may become locked)
    return result

def create_new_ship(ship, attributes, weapon, outfits):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Insert Ship
    sid = str(uuid.uuid4())
    query = """
        INSERT INTO Ship (sid, faction, uncapturable, never_disabled, license, name_singular, nameplural, sprite, customship, description)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    values = (sid, ship['faction'], int(ship['uncapturable']), int(ship['never_disabled']), "Pilot's", ship['name_singular'], ship['name_plural'], ship['sprite'], 1, ship['description'])
    print("Ship Query:", query, "Values:", values)  # ✅ Debugging
    cursor.execute(query, values)
    conn.commit()  # ✅ Commit ship before using sid
    
    # Insert Attributes
    for attribute in attributes:
        vid = str(uuid.uuid4())
        query = """
            INSERT INTO Value (vid, integervalue, floatvalue, stringvalue)
            VALUES (%s, %s, %s, %s)
        """
        values = (
            vid,
            attribute['value'] if attribute['type'] == 'int' else None,
            attribute['value'] if attribute['type'] == 'float' else None,
            attribute['value'] if attribute['type'] == 'str' else None
        )
        print("Attribute Query:", query, "Values:", values)
        cursor.execute(query, values)

        aid = str(uuid.uuid4())
        query = """
            INSERT INTO Attribute (aid, name, comment, sid, vid)
            VALUES (%s, %s, %s, %s, %s);
        """
        values = (aid, attribute['name'], '', sid, vid)
        print("Attribute Query:", query, "Values:", values)
        cursor.execute(query, values)
    
    # Insert Weapon
    wid = str(uuid.uuid4())
    query = """
        INSERT INTO Weapon (wid, comment, blastradius, shielddamage, hulldamage, hitforce, sid)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    values = (
        wid, '', 
        int(weapon.get('blast_radius', 0)), 
        int(weapon.get('shield_damage', 0)), 
        int(weapon.get('hull_damage', 0)), 
        int(weapon.get('hit_force', 0)), 
        sid
    )
    print("Weapon Query:", query, "Values:", values)
    cursor.execute(query, values)
    
    # Insert Outfits
    for outfit in outfits:
        oid = str(uuid.uuid4())
        vid = str(uuid.uuid4())
        query = """
            INSERT INTO Value (vid, integervalue, floatvalue, stringvalue)
            VALUES (%s, %s, %s, %s)
        """
        values = (vid, outfit['quantity'] if outfit['quantity'] > 1 else 1, None, None)
        print("Outfit Value Query:", query, "Values:", values)
        cursor.execute(query, values)

        query = """
            INSERT INTO Outfits (oid, name, comment, sid, vid)
            VALUES (%s, %s, %s, %s, %s);
        """
        values = (oid, outfit['name'], '', sid, vid)
        print("Outfit Query:", query, "Values:", values)
        cursor.execute(query, values)

    conn.commit()
    conn.close()
    
# ------------------------ END FUNCTIONS ------------------------ #


# ------------------------ BEGIN ROUTES ------------------------ #
# EXAMPLE OF GET REQUEST
@app.route("/", methods=["GET"])
def home():
    items = get_all_ships() # Call defined function to get all items
    return render_template("index.html", items=items) # Return the page to be rendered

# EXAMPLE OF POST REQUEST
@app.route("/create-ship", methods=["GET", "POST"])
def create_ship():
    if request.method == 'POST':
        ship_data = {field["name"]: (request.form.get(field["name"]) if field["type"] != "checkbox" else field["name"] in request.form) for field in SHIP_FIELDS}
        ship_data['custom_ship'] = True
        weapon_data = {field["name"]: request.form.get(field["name"]) for field in WEAPON_FIELDS}
        
        # Process outfits (multiple entries)
        outfit_data = []
        attribute_data = []
        outfit_count = int(request.form.get("outfit_count", 0))  # Dynamic count
        for i in range(outfit_count):
            outfit_data.append({
                "name": request.form.get(f"name_{i}"),
                "quantity": int(request.form.get(f"quantity_{i}")) if request.form.get(f"quantity_{i}") else 1
            })
        attribute_count = int(request.form.get("attribute_count", 0))
        for i in range(attribute_count):
            attribute_type = determine_type(request.form.get(f"value_{i}"))
            if attribute_type == 'str':
                attribute_value = str(request.form.get(f"value_{i}"))
            elif attribute_type == 'int':
                attribute_value = int(request.form.get(f"value_{i}"))
            elif attribute_type == 'float':
                attribute_type = float(request.form.get(f"value_{i}"))
            attribute_data.append({
                "name": request.form.get(f"name_{i}"),
                "value": attribute_value,
                "type": attribute_type
            })

        create_new_ship(ship_data, attribute_data, weapon_data, outfit_data)

    return render_template('create_ship.html', ship_fields=SHIP_FIELDS, weapon_fields=WEAPON_FIELDS)
# ------------------------ END ROUTES ------------------------ #


# listen on port 8080
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True) # TODO: Students PLEASE remove debug=True when you deploy this for production!!!!!
