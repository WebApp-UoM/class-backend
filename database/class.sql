DROP TABLE DirectionSubjects;
DROP TABLE Direction;
DROP TABLE Subjects;
DROP TABLE SubjectClasses;
DROP TABLE Students;
DROP TABLE YearsStudents;
DROP TABLE Years;
DROP TABLE YearsClasses;
DROP TABLE Classes;
DROP TABLE ClassStudents;
DROP TABLE TeachersClasses;
DROP TABLE Teachers;
DROP TABLE Authentication;
DROP TABLE TeachersSubject;
DROP TABLE StudentsDirection;


CREATE TABLE Subjects(
  name TEXT NOT NULL PRIMARY KEY
);

CREATE TABLE DirectionSubjects(
  direction INTEGER NOT NULL,
  subject TEXT NOT NULL,
  FOREIGN KEY(direction) REFERENCES Direction(id)
    ON UPDATE NO ACTION
    ON DELETE CASCADE,
  FOREIGN KEY(subject) REFERENCES Subjects(name)
    ON UPDATE NO ACTION
    ON DELETE CASCADE

);

CREATE TABLE Direction(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  year TEXT NOT NULL,
  UNIQUE (name, year)
  FOREIGN KEY(year) REFERENCES Years(year)
    ON UPDATE NO ACTION
    ON DELETE CASCADE

);

CREATE TABLE SubjectClasses(
  subject TEXT NOT NULL,
  class INTEGER NOT NULL,
  FOREIGN KEY(subject) REFERENCES Subjects(name)
    ON UPDATE NO ACTION
    ON DELETE CASCADE,
  FOREIGN KEY(class) REFERENCES Classes(id)
    ON UPDATE NO ACTION
    ON DELETE CASCADE
);

CREATE TABLE Classes(
  id INTEGER PRIMARY KEY AUTOINCREMENT
);

CREATE TABLE YearsClasses(
  year TEXT NOT NULL,
  class INTEGER NOT NULL,
  FOREIGN KEY(year) REFERENCES Years(year)
    ON UPDATE NO ACTION
    ON DELETE CASCADE,
  FOREIGN KEY(class) REFERENCES Classes(id)
    ON UPDATE NO ACTION
    ON DELETE CASCADE
);

CREATE TABLE Years(
  year TEXT NOT NULL PRIMARY KEY
);

CREATE TABLE YearsStudents(
  year TEXT NOT NULL,
  student TEXT NOT NULL,
  FOREIGN KEY(year) REFERENCES Years(year)
    ON UPDATE NO ACTION
    ON DELETE CASCADE,
  FOREIGN KEY(student) REFERENCES Students(username)
    ON UPDATE NO ACTION
    ON DELETE CASCADE
);

CREATE TABLE Students(
  firstname TEXT NOT NULL,
  lastname TEXT NOT NULL,
  username TEXT NOT NULL PRIMARY KEY,
  year TEXT NOT NULL,
  direction TEXT,
  phone TEXT,
  email TEXT,
  FOREIGN KEY(username) REFERENCES Authentication(username)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

CREATE TABLE ClassStudents(
  class INTEGER NOT NULL,
  student TEXT NOT NULL,
  FOREIGN KEY(class) REFERENCES Classes(id)
    ON UPDATE NO ACTION
    ON DELETE CASCADE,
  FOREIGN KEY(student) REFERENCES Students(username)
    ON UPDATE NO ACTION
    ON DELETE CASCADE
);


CREATE TABLE TeachersClasses(
  teacher TEXT NOT NULL,
  class INTEGER NOT NULL,
  FOREIGN KEY(class) REFERENCES Classes(id)
    ON UPDATE NO ACTION
    ON DELETE CASCADE,
  FOREIGN KEY(teacher) REFERENCES Teachers(username)
    ON UPDATE NO ACTION
    ON DELETE CASCADE
);

CREATE TABLE Teachers(
  firstname TEXT NOT NULL,
  lastname TEXT NOT NULL,
  username TEXT NOT NULL PRIMARY KEY,
  phone TEXT,
  email TEXT,
  FOREIGN KEY(username) REFERENCES Authentication(username)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

CREATE TABLE TeachersSubject(
  teacher TEXT NOT NULL,
  subject TEXT NOT NULL,
  FOREIGN KEY(subject) REFERENCES Subjects(name)
    ON UPDATE NO ACTION
    ON DELETE CASCADE,
  FOREIGN KEY(teacher) REFERENCES Teachers(username)
    ON UPDATE NO ACTION
    ON DELETE CASCADE
);

CREATE TABLE StudentsDirection(
  student TEXT NOT NULL,
  direction INTEGER NOT NULL,
  FOREIGN KEY(direction) REFERENCES Direction(id)
    ON UPDATE NO ACTION
    ON DELETE CASCADE,
  FOREIGN KEY(student) REFERENCES Students(username)
    ON UPDATE NO ACTION
    ON DELETE CASCADE
);

CREATE TABLE Authentication(
  username TEXT NOT NULL PRIMARY KEY,
  password TEXT NOT NULL,
  role TEXT NOT NULL,
  FOREIGN KEY(username) REFERENCES Teachers(username)
    ON UPDATE NO ACTION
    ON DELETE CASCADE,
  FOREIGN KEY(username) REFERENCES Students(username)
    ON UPDATE NO ACTION
    ON DELETE CASCADE
);

INSERT INTO Authentication VALUES ('root', 'root', 'admin');
INSERT INTO Teachers VALUES ('nikos', 'stef', 'root', NULL, NULL);
INSERT INTO Students VALUES ('enas', 'dio', 'tria', 'HS1', NULL, NULL, NULL);
INSERT INTO Subjects VALUES ('Maths');
INSERT INTO Subjects VALUES ('Physics');
INSERT INTO Subjects VALUES ('Literature');
INSERT INTO Direction VALUES (NULL, 'Thetiki', 'HS2');
INSERT INTO Direction VALUES (NULL, 'Texnologiki', 'HS3');
INSERT INTO Classes VALUES (0);
INSERT INTO DirectionSubjects 
SELECT Direction.id, Subjects.name FROM Direction, Subjects WHERE Direction.name = 'Thetiki' AND Subjects.name = 'Maths';
INSERT INTO DirectionSubjects
SELECT Direction.id, Subjects.name FROM Direction, Subjects WHERE Direction.name = 'Texnologiki' AND Subjects.name = 'Physics';

