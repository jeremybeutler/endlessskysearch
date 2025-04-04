import os
from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
from dotenv import load_dotenv
import uuid

# Define ship attributes
SHIP_FIELDS = [
    {"name": "faction", "label": "Faction", "type": "text", "required": False},
    {"name": "uncapturable", "label": "Uncapturable", "type": "checkbox", "required": False},
    {"name": "neverdisabled", "label": "Never Disabled", "type": "checkbox", "required": True},
    {"name": "namesingular", "label": "Name (Singular)", "type": "text", "required": True},
    {"name": "nameplural", "label": "Name (Plural)", "type": "text", "required": False},
    {"name": "sprite", "label": "Sprite Path", "type": "text", "required": False},
    {"name": "description", "label": "Description", "type": "textarea", "required": False},
]

# Define weapon attributes
WEAPON_FIELDS = [
    {"name": "WID", "label": "", "type": "hidden", "required": False},
    {"name": "WeaponComment", "label": "Comment", "type": "textarea", "required": False},
    {"name": "WeaponShieldDamage", "label": "Shield Damage", "type": "number", "required": False},
    {"name": "WeaponHullDamage", "label": "Hull Damage", "type": "number", "required": False},
    {"name": "WeaponBlastRadius", "label": "Blast Radius", "type": "number", "required": False},
    {"name": "WeaponHitForce", "label": "Hit Force", "type": "number", "required": False},
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

def get_ship_by_id(ship_id): 
    # Create a new database connection for each request
    conn = get_db_connection()  # Create a new database connection
    cursor = conn.cursor()  # Creates a cursor for the connection, you need this to do queries

    # Query the db for ship data using the existing view
    query = "SELECT * FROM ShipDetail WHERE sid = %s"
    values = (ship_id,)
    cursor.execute(query, values)

    # Get column names (field names)
    column_names = [desc[0] for desc in cursor.description]

    # Get result
    result = cursor.fetchall()  # Gets result from query

    # Close the db connection
    conn.close()  # Close the db connection (NOTE: You should do this after each query, otherwise your database may become locked)
    
    # Organize the result
    ship = {}
    attributes = []
    outfits = []
    weapon = {}

    # Process the rows into the organized result
    for row in result:
        row_dict = {column_names[i]: row[i] for i in range(len(column_names))}
        
        # Organizing the ship info (if it's the first row or contains the ship's main details)
        if "sid" in row_dict:
            ship = {
                "faction": row_dict["faction"],
                "uncapturable": row_dict["uncapturable"],
                "neverdisabled": row_dict["neverdisabled"],
                "namesingular": row_dict["namesingular"],
                "nameplural": row_dict["nameplural"],
                "sprite": row_dict["sprite"],
                "custom_ship": row_dict["customship"],
                "description": row_dict["description"]
            }
        # Organizing attributes
        if "attributes" in row_dict and row_dict["attributes"] is not None:
            for attribute_dict in row_dict["attributes"]:
                attribute = {
                    "AID": attribute_dict.get("AID"),
                    "Name": attribute_dict.get("AttributeName"),
                    "Value": None,
                    "Type": None
                }
            
                # Include non-null values and add ValueType
                if attribute_dict["AttributeInt"] is not None:
                    attribute["Value"] = attribute_dict["AttributeInt"]
                    attribute["Type"] = 'int'
                elif attribute_dict["AttributeFloat"] is not None:
                    attribute["Value"] = attribute_dict["AttributeFloat"]
                    attribute["Type"] = 'float'
                elif attribute_dict["AttributeString"] is not None:
                    attribute["Value"] = attribute_dict["AttributeString"]
                    attribute["Type"] = 'str'
            
                # Add attribute if a valid value exists
                if attribute["Value"] is not None:
                    attributes.append(attribute)
        
        # Organizing outfits
        if "outfits" in row_dict and row_dict["outfits"] is not None:
            for outfit_dict in row_dict["outfits"]:
                outfit = {
                    "OID": outfit_dict.get("OID"),
                    "Name": outfit_dict.get("OutfitName"),
                    "Quantity": outfit_dict.get("OutfitInt")
                }


                # Add outfit if a valid value exists
                if outfit["Quantity"] is not None:
                    outfits.append(outfit)
        
        # Organizing weapons
        weapon = row_dict['weapon']

    # Return the organized result
    return {
        "ship": ship,
        "attributes": attributes,
        "outfits": outfits,
        "weapon": weapon
    }


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

def create_new_ship(ship, attributes, weapon, outfits):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Insert Ship
    sid = str(uuid.uuid4())
    query = """
        INSERT INTO Ship (sid, faction, uncapturable, never_disabled, license, name_singular, nameplural, sprite, customship, description)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    values = (sid, ship['faction'], ship['uncapturable'], ship['neverdisabled'], "Pilot's", ship['namesingular'], ship['nameplural'], ship['sprite'], 1, ship['description'])
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
        cursor.execute(query, values)

        aid = str(uuid.uuid4())
        query = """
            INSERT INTO Attribute (aid, name, comment, sid, vid)
            VALUES (%s, %s, %s, %s, %s);
        """
        values = (aid, attribute['name'], '', sid, vid)
        cursor.execute(query, values)
    
    # Insert Weapon
    wid = str(uuid.uuid4())
    query = """
        INSERT INTO Weapon (wid, comment, blastradius, shielddamage, hulldamage, hitforce, sid)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    values = (
        wid, 
        weapon.get('Comment', 0),
        weapon.get('BlastRadius', 0), 
        weapon.get('ShieldDamage', 0), 
        weapon.get('HullDamage', 0), 
        weapon.get('HitForce', 0), 
        sid
    )
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
        cursor.execute(query, values)

        query = """
            INSERT INTO Outfits (oid, name, comment, sid, vid)
            VALUES (%s, %s, %s, %s, %s);
        """
        values = (oid, outfit['name'], '', sid, vid)
        cursor.execute(query, values)

    conn.commit()
    conn.close()

def update_existing_ship(sid, old_ship, updated_ship):
    conn = get_db_connection()
    cursor = conn.cursor()
    print('old_ship', old_ship, 'updated_ship', updated_ship)
    query = """
        UPDATE Ship
        SET faction = %s, uncapturable = %s, never_disabled = %s, name_singular = %s, nameplural = %s, sprite = %s, description = %s
        WHERE sid = %s
    """
    values = (updated_ship['ship']['faction'], updated_ship['ship']['uncapturable'], updated_ship['ship']['neverdisabled'], updated_ship['ship']['namesingular'], updated_ship['ship']['nameplural'], updated_ship['ship']['sprite'], updated_ship['ship']['description'], sid)
    cursor.execute(query, values)

    for index, attribute in enumerate(updated_ship['attributes']):
        if index >= len(old_ship['attributes']):
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
            cursor.execute(query, values)

            aid = str(uuid.uuid4())
            query = """
                INSERT INTO Attribute (aid, name, comment, sid, vid)
                VALUES (%s, %s, %s, %s, %s);
            """
            values = (aid, attribute['name'], '', sid, vid)
            cursor.execute(query, values)
        elif attribute != old_ship['attributes'][index]:
            if attribute['Name'] != old_ship['attributes'][index]['Name']:
                query = """
                    UPDATE Attribute
                    SET name = %s
                    WHERE aid = %s
                """
                values = (attribute['Name'], old_ship['attributes'][index]['AID'])
                cursor.execute(query, values)
            if attribute['Value'] != old_ship['attributes'][index]['Value']:
                query = """
                    UPDATe Value
                    SET integervalue = %s, floatvalue = %s, stringvalue = %s
                    WHERE vid = (
                        SELECT vid FROM Attribute WHERE aid = %s
                    )
                """
                values = (
                    attribute['Value'] if attribute['Type'] == 'int' else None,
                    attribute['Value'] if attribute['Type'] == 'float' else None,
                    attribute['Value'] if attribute['Type'] == 'str' else None,
                    old_ship['attributes'][index]['AID']
                )
                cursor.execute(query, values)
    for index, outfit in enumerate(updated_ship['outfits']):
        if index >= len(old_ship['outfits']):
            vid = str(uuid.uuid4())
            query = """
                INSERT INTO Value (vid, integervalue, floatvalue, stringvalue)
                VALUES (%s, %s, %s, %s)
            """
            values = (vid, outfit['quantity'], None, None)
            cursor.execute(query, values)

            oid = str(uuid.uuid4())
            query = """
                INSERT INTO Outfits (oid, name, comment, sid, vid)
                VALUES (%s, %s, %s, %s, %s);
            """
            values = (oid, outfit['Name'], '', sid, vid)
            cursor.execute(query, values)
        elif outfit != old_ship['outfits'][index]:
            if outfit['Name'] != old_ship['outfits'][index]['Name']:
                query = """
                    UPDATE Outfits
                    SET name = %s
                    WHERE oid = %s
                """
                values = (outfit['Name'], old_ship['outfits'][index]['OID'])
                cursor.execute(query, values)
            if outfit['Quantity'] != old_ship['outfits'][index]['Quantity']:
                query = """
                    UPDATE Value
                    SET integervalue = %s, floatvalue = %s, stringvalue = %s
                    WHERE vid = (
                        SELECT oid FROM Outfits WHERE oid = %s
                    )
                """
                values = (outfit['Quantity'], None, None, old_ship['outfits'][index]['OID'])
                cursor.execute(query, values)

    if updated_ship['weapon'] != old_ship['weapon']:
        query = """
            UPDATE Weapon 
            SET comment = %s, blastradius = %s, shielddamage = %s, hulldamage = %s, hitforce = %s
            WHERE wid = %s;
        """
        values = (
            updated_ship['weapon']['WeaponComment'],
            updated_ship['weapon']['WeaponBlastRadius'], 
            updated_ship['weapon']['WeaponShieldDamage'], 
            updated_ship['weapon']['WeaponHullDamage'], 
            updated_ship['weapon']['WeaponHitForce'], 
            old_ship['weapon']['WID'],
        )
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
        ship_data = {field["name"]: request.form.get(field["name"]) if field["type"] != "checkbox" else int(field["name"] in request.form) for field in SHIP_FIELDS}
        ship_data['custom_ship'] = True
        weapon_data = {field["name"]: int(request.form.get(field["name"])) if field['type'] == 'number' else request.form.get(field["name"]) for field in WEAPON_FIELDS}
        
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

@app.route("/update-ship/<uuid:ship_uuid>", methods=["GET", "POST"])
def update_ship(ship_uuid):
    ship_uuid = str(ship_uuid)
    ship = get_ship_by_id(ship_uuid)
    if request.method == 'POST':
        for field in SHIP_FIELDS:
            if field["type"] == "checkbox":
                print(int(field["name"] in request.form) )
        ship_data = {field["name"]: request.form.get(field["name"]) if field["type"] != "checkbox" else int(field["name"] in request.form) for field in SHIP_FIELDS}
        ship_data['custom_ship'] = 1
        weapon_data = {field["name"]: int(request.form.get(field["name"])) if field['type'] == 'number' else request.form.get(field["name"]) for field in WEAPON_FIELDS}
        
        # Process outfits (multiple entries)
        outfit_data = []
        attribute_data = []
        outfit_count = int(request.form.get("outfit_count", 0))  # Dynamic count
        for i in range(outfit_count):
            outfit_data.append({
                "OID": request.form.get(f"oid_{i}"),
                "Name": request.form.get(f"name_{i}"),
                "Quantity": int(request.form.get(f"quantity_{i}")) if request.form.get(f"quantity_{i}") else 1
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
                "AID": request.form.get(f"aid_{i}"),
                "Name": request.form.get(f"name_{i}"),
                "Value": attribute_value,
                "Type": attribute_type
            })
        update_existing_ship(ship_uuid, ship, { 'ship': ship_data, 'attributes': attribute_data, 'outfits': outfit_data, 'weapon': weapon_data })
        ship = get_ship_by_id(ship_uuid)

    return render_template('update_ship.html', 
        ship_fields=SHIP_FIELDS, 
        weapon_fields=WEAPON_FIELDS, 
        ship=ship['ship'], 
        weapon=ship['weapon'], 
        attributes=ship['attributes'], 
        outfits=ship['outfits']
    )

# listen on port 8080
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True) # TODO: Students PLEASE remove debug=True when you deploy this for production!!!!!
