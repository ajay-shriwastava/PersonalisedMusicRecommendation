DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);

CREATE TABLE USER(
    user_Id INTEGER PRIMARY KEY
)

CREATE TABLE USER_TRACK(
    user_Id INTEGER,
    track_Id INTEGER,
    rating INTEGER,
    PRIMARY KEY (user_Id, track_Id)
);

CREATE TABLE USER_ARTIST(
    user_Id INTEGER,
    artist_id INTEGER,
    rating INTEGER,
    PRIMARY KEY (user_Id, artist_id)
);

CREATE TABLE USER_PREFERENCE (
    user_Id INTEGER,
    tracks TEXT,
    location TEXT
);

CREATE TABLE TRACK(
    track_Id INTEGER PRIMARY KEY,
    track_title TEXT,
    artist_id INTEGER,
    tweet_count INTEGER
);

CREATE TABLE ARTIST(
    artist_id INTEGER PRIMARY KEY,
    artist_name TEXT
);

INSERT INTO TRACK (track_Id, track_title, artist_id, tweet_count)
VALUES
    (141574, 'Someone Like You', 9192, 432),
    (1479214, 'Paradise', 82745, 383),
    (141567, 'Set Fire to the Rain', 9192, 263),
    (1072515, 'It Will Rain', 52897, 197),
    (6213223, 'You da One', 356772, 178),
    (2106361, 'Practice', 122991, 174),
    (6213179, 'We Found Love', 356772, 173),
    (2106383, 'Shot for Me', 122991, 170),
    (4098232, 'The One That Got Away', 228395, 162),
    (8010733, 'Climax', 466569, 160);


INSERT INTO ARTIST (artist_id, artist_name)
VALUES
    (9192, 'Adele'),
    (82745, 'Coldplay'),
    (52897, 'BoB feat. Bruno Mars'),
    (356772, 'Rihanna'),
    (122991, 'Drake'),
    (228395, 'Katy Perry'),
    (466569, 'Usher');

INSERT INTO USER (user_Id)
VALUES
    (174626103),
    (161262801),
    (174228242),
    (160874621),
    (35653693),
    (259861614),
    (346364194),
    (181840782)


CREATE TABLE TWEET(
    tweet_Id INTEGER PRIMARY KEY,
    street TEXT,
    city TEXT,
    state TEXT,
    country TEXT,
    countryName TEXT,
    languages TEXT
);


INSERT INTO TWEET (tweet_Id, street, city, state, country, countryName, languages)
VALUES
    (174626103, "Great Portland Street", "City of Westminster" , "England", "GB", "United Kingdom", "en-GB,cy-GB,gd"),
    (161262801, "Emil-Jannings-Straße", "Potsdam", "Brandenburg", "DE", "Germany", "de"),
    (174228242, "Great Portland Street", "City of Westminster", "England", "GB", "United Kingdom", "en-GB,cy-GB,gd"),
    (160874621, "Wetzlarer Straße", "Potsdam", "Brandenburg", "DE", "Germany", "de"),
    (35653693, "403 King Springs Village Pky SE", "Smyrna", "GA", "US", "United States", "en-US,es-US,haw,fr"),
    (259861614, "528 N Felton St", "Philadelphia", "PA", "US", "United States", "en-US,es-US,haw,fr"),
    (346364194, "599 Wythe Ave", "Brooklyn", "NY", "US", "United States", "en-US,es-US,haw,fr"),
    (181840782, "2153 County Line Rd", "Mt Gilead", "NC", "US", "United States", "en-US,es-US,haw,fr")