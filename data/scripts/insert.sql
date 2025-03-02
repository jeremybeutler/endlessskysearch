-- Insert into Ship (CustomShip not included, so it can be deleted)
INSERT INTO Ship (sid, faction, uncapturable, "Never-Disabled", license, "Name-Singular", nameplural, sprite, description)
VALUES
  ('550e8400-e29b-41d4-a716-446655440000', 'Federation', 0, 1, 'Pilot License', 'Falcon', 'Falcons', 'falcon.png', 'A fast and agile spaceship.');
-- Insert into Value (Each row has a unique UUID and only one value type populated)
INSERT INTO Value (vid, integervalue, floatvalue, stringvalue)
VALUES
  ('b123f456-78d9-12d3-a456-426614174001', 10, NULL, NULL), -- Integer-based Value
  ('c234e567-89a0-23d4-b567-536614174002', NULL, 99.9, NULL), -- Float-based Value
  ('d345f678-90b1-34e5-c678-646614174003', NULL, NULL, 'Ultra Fast'); -- String-based Value
-- Insert into Outfits (Each row gets a unique UUID)
INSERT INTO Outfits (oid, name, comment, sid, vid)
VALUES
  ('e456g789-01c2-45f6-d789-756614174004', 'Laser Cannon', 'A high-powered laser weapon',
   '550e8400-e29b-41d4-a716-446655440000', 'b123f456-78d9-12d3-a456-426614174001');
-- Insert into Attribute
INSERT INTO Attribute (aid, name, comment, sid, vid)
VALUES
  ('f567h890-12d3-56g7-e890-866614174005', 'Speed', 'Defines how fast the ship moves',
   '550e8400-e29b-41d4-a716-446655440000', 'd345f678-90b1-34e5-c678-646614174003');
-- Insert into Weapon
INSERT INTO Weapon (wid, comment, blastradius, shielddamage, hulldamage, hitforce, sid)
VALUES
  ('g678i901-23e4-67h8-f901-976614174006', 'High-impact plasma cannon', 50, 200, 100, 500,
   '550e8400-e29b-41d4-a716-446655440000');