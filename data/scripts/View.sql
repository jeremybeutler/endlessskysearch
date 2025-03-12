CREATE VIEW ShipDetails AS
SELECT
--Ship Table
  s.SID,
  s.Faction,
  s.Uncapturable,
  s.Never_Disabled AS NeverDisabled,
  s.License,
  s.Name_Singular AS NameSingular,
  s.Name_Plural AS NamePlural,
  s.Sprite,
  s.CustomShip,
  s.Description,

-- Attribute Table
  a.AID,
  a.Name AS AttributeName,
  a.Comment AS AttributeComment,
  a.VID AS AttributeVID,

-- Attribute's Value Table
  av.IntegerValue AS AttributeInt,
  av.FloatValue AS AttributeFloat,
  av.StringValue AS AttributeString,

-- Weapon Table
  w.WID,
  w.BlastRadius,
  w.ShieldDamage,
  w.HullDamage,
  w.HitForce,

-- Outfit Table
  o.OID,
  o.Name AS OutfitName,
  o.Comment AS OutfitComment,
  o.VID AS OutfitVID,

-- Outfit's Value Table
  ov.IntegerValue AS OutfitInt,
  ov.FloatValue AS OutfitFloat,
  ov.StringValue AS OutfitString

FROM Ship s
LEFT JOIN Attribute a ON s.SID = a.SID
LEFT JOIN Value av ON a.VID = av.VID
LEFT JOIN Weapon w ON s.SID = w.SID
LEFT JOIN Outfits o ON s.SID = o.SID
LEFT JOIN Value ov ON o.VID = ov.VID;