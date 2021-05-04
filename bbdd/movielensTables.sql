BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "movie" (
	"movieId"	INTEGER,
	"title"	TEXT NOT NULL,
	"genres"	TEXT NOT NULL,
	PRIMARY KEY("movieId" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "rating" (
	"ratingId"	INTEGER,
	"userId"	INTEGER NOT NULL,
	"movieId"	INTEGER NOT NULL,
	"rating"	REAL NOT NULL,
	"timestamp"	INTEGER NOT NULL,
	PRIMARY KEY("ratingId" AUTOINCREMENT),
	FOREIGN KEY("movieId") REFERENCES "movie"("movieId")
);
COMMIT;