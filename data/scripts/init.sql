CREATE TABLE Value
(
  VID CHAR(36) NOT NULL,
  IntegerValue INT NOT NULL,
  FloatValue FLOAT NOT NULL,
  StringValue VARCHAR NOT NULL,
  PRIMARY KEY (VID)
);

CREATE TABLE Ship
(
  SID CHAR(36) NOT NULL,
  Faction VARCHAR NOT NULL,
  Uncapturable INT NOT NULL,
  Never-Disabled INT NOT NULL,
  License VARCHAR,
  Name-Singular VARCHAR NOT NULL,
  NamePlural VARCHAR NOT NULL,
  Sprite VARCHAR NOT NULL,
  CustomShip INT NOT NULL,
  Description VARCHAR NOT NULL,
  PRIMARY KEY (SID)
);

CREATE TABLE Attribute
(
  AID CHAR(36) NOT NULL,
  Name VARCHAR NOT NULL,
  Comment VARCHAR,
  SID CHAR(36) NOT NULL,
  VID CHAR(36) NOT NULL,
  PRIMARY KEY (AID),
  FOREIGN KEY (SID) REFERENCES Ship(SID),
  FOREIGN KEY (VID) REFERENCES Value(VID)
);

CREATE TABLE Weapon
(
  WID CHAR(36) NOT NULL,
  Comment VARCHAR,
  BlastRadius INT NOT NULL,
  ShieldDamage INT NOT NULL,
  HullDamage INT NOT NULL,
  HitForce INT NOT NULL,
  SID CHAR(36) NOT NULL,
  PRIMARY KEY (WID),
  FOREIGN KEY (SID) REFERENCES Ship(SID)
);

CREATE TABLE Outfits
(
  Name VARCHAR NOT NULL,
  OID CHAR(36) NOT NULL,
  Comment VARCHAR,
  SID CHAR(36) NOT NULL,
  VID CHAR(36),
  PRIMARY KEY (OID),
  FOREIGN KEY (SID) REFERENCES Ship(SID),
  FOREIGN KEY (VID) REFERENCES Value(VID)
);