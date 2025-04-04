CREATE VIEW ShipDetail AS
SELECT
  -- Ship Table fields (top-level ship fields)
  s.SID,
  s.Faction,
  s.Uncapturable,
  s.Never_Disabled AS NeverDisabled,
  s.License,
  s.Name_Singular AS NameSingular,
  s.NamePlural AS NamePlural,
  s.Sprite,
  s.CustomShip,
  s.Description,

  -- Attributes as an array under "attributes"
  (
    SELECT json_agg(json_build_object(
      'AID', a.AID,
      'AttributeName', a.Name,
      'AttributeComment', a.Comment,
      'AttributeVID', a.VID,
      'AttributeInt', av.IntegerValue,
      'AttributeFloat', av.FloatValue,
      'AttributeString', av.StringValue
    ))
    FROM Attribute a
    LEFT JOIN Value av ON a.VID = av.VID
    WHERE a.SID = s.SID
  ) AS attributes,

  -- Weapon as an object under "weapon"
  (
    SELECT json_build_object(
      'WID', w.WID,
      'WeaponComment', w.Comment,
      'WeaponBlastRadius', w.BlastRadius,
      'WeaponShieldDamage', w.ShieldDamage,
      'WeaponHullDamage', w.HullDamage,
      'WeaponHitForce', w.HitForce
    )
    FROM Weapon w
    WHERE w.SID = s.SID
  ) AS weapon,

  -- Outfits as an array under "outfits"
  (
    SELECT json_agg(json_build_object(
      'OID', o.OID,
      'OutfitName', o.Name,
      'OutfitComment', o.Comment,
      'OutfitVID', o.VID,
      'OutfitInt', ov.IntegerValue,
      'OutfitFloat', ov.FloatValue,
      'OutfitString', ov.StringValue
    ))
    FROM Outfits o
    LEFT JOIN Value ov ON o.VID = ov.VID
    WHERE o.SID = s.SID
  ) AS outfits

FROM Ship s;
