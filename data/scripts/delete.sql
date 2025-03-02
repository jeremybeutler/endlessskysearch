-- Delete from Weapon
DELETE FROM Weapon WHERE sid = '550e8400-e29b-41d4-a716-446655440000';
-- Delete from Attribute
DELETE FROM Attribute WHERE sid = '550e8400-e29b-41d4-a716-446655440000';
-- Delete from Outfits
DELETE FROM Outfits WHERE sid = '550e8400-e29b-41d4-a716-446655440000';
-- Delete from Value (Deleting only inserted values)
DELETE FROM Value WHERE vid IN ('b123f456-78d9-12d3-a456-426614174001',
                                'c234e567-89a0-23d4-b567-536614174002',
                                'd345f678-90b1-34e5-c678-646614174003');
-- Delete from Ship
DELETE FROM Ship WHERE sid = '550e8400-e29b-41d4-a716-446655440000';