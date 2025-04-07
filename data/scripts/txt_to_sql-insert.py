import uuid
import re
from datetime import datetime
import psycopg2
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()

# Function to retrieve DB connection
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_DATABASE")
    )
    return conn

## Below is the file that is read from to generate the insert script
INPUT_FILE = "bunrodea-ships.txt"
## Below is a global that ensures "Start of ships JSON:" is only printed once
one_print = False ## DO NOT CHANGE

def parse_ships(file_path):
########################################################################################################
####### Below are the known values that were origionally called 'internals'
####### Each one will need to be hardcoded out to ensure they do not end up being put into the outfits
    hardcoded_escapes = ['gun ', 'engine ', 'leak ', 'explode ', 'turret ', 'bay ', '"final explode"']
########################################################################################################
####### I could try to implement a better solution, but I am too tired to do that right now
########################################################################################################
    ships = []
    current_ship = None
    in_attributes = False
    in_weapon = False
    in_outfits = False

    with open(file_path, 'r') as f:
        for line in f:
            original_line = line
            line = line.strip()

            if line.startswith('ship "'):
                if current_ship:
                    ships.append(current_ship)
                current_ship = {
                    'name': re.search(r'ship "(.*?)"', line).group(1),
                    'attributes': {},
                    'weapon': {},
                    'outfits': [],
                    'description': [],
                    'license': [],
                    'sprite': None,
                    'thumbnail': None
                }
                in_attributes = False
                in_weapon = False
                in_outfits = False
            elif current_ship:
                if line.startswith('sprite "'):
                    current_ship['sprite'] = re.search(r'sprite "(.*?)"', line).group(1)
                elif line.startswith('thumbnail "'):
                    current_ship['thumbnail'] = re.search(r'thumbnail "(.*?)"', line).group(1)
                elif line.startswith('license "'):
                    current_ship['license'] = re.search(r'license "(.*?)"', line).group(1)
                elif line.startswith('description "'):
                    desc = re.search(r'description "(.*?)"', line).group(1)
                    current_ship['description'].append(desc)
                elif line == 'attributes':
                    in_attributes = True
                    in_weapon = False
                elif line == 'weapon' and in_attributes:
                    in_weapon = True
                elif line == 'outfits':
                    in_outfits = True
                    in_attributes = False
                elif any(line.startswith(escaped) for escaped in hardcoded_escapes): 
                    1 + 1
                elif in_attributes:
                    if line.startswith('"'):
                        key_match = re.match(r'"(.+?)" (.+)', line)
                        if key_match:
                            key, value = key_match.groups()
                            if in_weapon:
                                current_ship['weapon'][key] = int(float(value))
                            else:
                                current_ship['attributes'][key] = value
                    else:
                        match = re.match(r'(\w+)\s+"?(.+?)"?$', line)
                        if match:
                            key, value = match.groups()
                            current_ship['attributes'][key] = value.strip('"')
                elif in_outfits and line:
                    outfit_match = re.match(r'"?(.*?)"?\s+(\d+)$', line)
                    if outfit_match: ##ERROR: Grabs engine, gun, leak, explode and description
                        name, count = outfit_match.groups()
                        current_ship['outfits'].append((name, int(count)))
                    else:
                        current_ship['outfits'].append((line.strip('"'), 1))
                elif re.search(r'description\s+"', original_line, re.IGNORECASE):
                    desc = re.search(r'description\s+"(.*?)"', original_line, re.DOTALL)
                    if desc:
                        current_ship['description'].append(desc.group(1).strip())

        if current_ship:
            ships.append(current_ship)
    return ships

def generate_sql(ships):
    output = []
    output.append(f"-- Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    global one_print
    if one_print == False:
        one_print = True
        print("\n---------------------------------------------------")
        print("---------------------------------------------------")
        print("Start of ships JSON:")
        print("\n\n\n")
        for ship in ships:
            print(ship, end="\n\n")
        print("\n\n\n")
        print("---------------------------------------------------")
        print("---------------------------------------------------")
        print("Start of SQL insert script:")
        print("\n\n\n")
    for ship in ships:
        sid = str(uuid.uuid4())
        weapon_id = str(uuid.uuid4()) if ship['weapon'] else None
        # Validate required fields
        if not ship['sprite']:
            raise ValueError(f"Ship {ship['name']} missing sprite")
        if not ship['description']:
            raise ValueError(f"Ship {ship['name']} missing description")

        # Ship table insert
        ship_sql = f"""
INSERT INTO Ship (SID, Faction, Uncapturable, Never_Disabled, License, 
    Name_Singular, NamePlural, Sprite, CustomShip, Description)
VALUES (
    '{sid}',
    'Bunrodea',
    0,
    0,
    {f"'{ship['licenses'][0]}'" if ship.get('licenses') and ship['licenses'] else 'NULL'},
    '{ship['name']}',
    '{ship['name']}s',
    '{ship['sprite']}',
    0,
    $${' '.join(ship['description'])}$$
);"""
        output.append(ship_sql.strip())

        # Attributes handling
        for key, value in ship['attributes'].items():
            vid = str(uuid.uuid4())
            aid = str(uuid.uuid4())
            
            value_type, sql_value = determine_value_type(value)
            output.append(f"INSERT INTO Value (VID, {value_type}) VALUES ('{vid}', {sql_value});")
            
            output.append(
                f"INSERT INTO Attribute (AID, Name, SID, VID) "
                f"VALUES ('{aid}', '{key}', '{sid}', '{vid}');"
            )

        # Weapon handling
        if ship['weapon']:
            output.append(f"""
INSERT INTO Weapon (WID, BlastRadius, ShieldDamage, HullDamage, HitForce, SID)
VALUES (
    '{weapon_id}',
    {ship['weapon'].get('blast radius', 0)},
    {ship['weapon'].get('shield damage', 0)},
    {ship['weapon'].get('hull damage', 0)},
    {ship['weapon'].get('hit force', 0)},
    '{sid}'
);""".strip())

        # Outfits handling
        for outfit, count in ship['outfits']:
            oid = str(uuid.uuid4())
            if count > 1:
                vid = str(uuid.uuid4())
                output.append(f"INSERT INTO Value (VID, IntegerValue) VALUES ('{vid}', {count});")
                output.append(
                    f"INSERT INTO Outfits (Name, OID, SID, VID) "
                    f"VALUES ('{outfit}', '{oid}', '{sid}', '{vid}');"
                )
            else:
                output.append(
                    f"INSERT INTO Outfits (Name, OID, SID, VID) "
                    f"VALUES ('{outfit}', '{oid}', '{sid}', NULL);"
                )
        
        output.append("")  # Add empty line between ships
    
    return '\n'.join(output)

def determine_value_type(value):
    try:
        # Try converting to float first
        float_val = float(value)
        if '.' in value:
            return 'FloatValue', float_val
        else:
            return 'IntegerValue', int(float_val)
    except ValueError:
        return 'StringValue', f"$${value}$$"

if __name__ == "__main__":
    ships = parse_ships(INPUT_FILE)
    query = generate_sql(ships)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit() 
    conn.close()
