DROP TABLE IF EXISTS cards;
DROP TABLE IF EXISTS uncertain_sightings;
DROP TABLE IF EXISTS deck_meta;

CREATE TABLE deck_meta (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL
);

CREATE TABLE cards (
  id TEXT PRIMARY KEY,
  title_zh TEXT NOT NULL,
  status TEXT NOT NULL,
  visibility TEXT NOT NULL,
  confidence REAL NOT NULL,
  border_colors TEXT,
  source_images TEXT,
  visible_text TEXT,
  notes TEXT
);

CREATE TABLE uncertain_sightings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title_guess TEXT NOT NULL,
  source_images TEXT,
  reason TEXT
);
