import sqlite3
con = sqlite3.connect('rmp_server.db')

cur = con.cursor()

print("creating table User", end=": ")
try:
    cur.execute(
        '''CREATE TABLE User
           (id integer primary key autoincrement,
            login varchar unique not null,
            password varchar not null)''')

    con.commit()
    print("Done")
except sqlite3.OperationalError as ex:
    print(ex)

print("creating table FileState", end=": ")
try:
    cur.execute(
        '''CREATE TABLE FileState
           (id integer primary key autoincrement,
            name varchar unique not null)''')

    con.commit()
    print("Done")
except sqlite3.OperationalError as ex:
    print(ex)

print("filling table FileState", end=": ")
try:
    cur.execute(
        '''insert into FileState(name)
           values ("error"), ("pending"), ("ready")''')

    con.commit()
    print("Done")
except sqlite3.OperationalError as ex:
    print(ex)
except sqlite3.IntegrityError:
    print("Records already exist")

print("creating table File", end=": ")
try:
    cur.execute(
        '''CREATE TABLE File
           (id integer primary key autoincrement,
            stateId integer not null,
            url varchar unique not null,
            path varchar unique not null,
            stateDescription varchar,
            foreign key(stateId) references FileState(id))''')

    con.commit()
    print("Done")
except sqlite3.OperationalError as ex:
    print(ex)

print("creating table TagSource", end=": ")
try:
    cur.execute(
        '''CREATE TABLE TagSource
           (id integer primary key autoincrement,
            name varchar unique not null)''')

    con.commit()
    print("Done")
except sqlite3.OperationalError as ex:
    print(ex)

print("filling table TagSource", end=": ")
try:
    cur.execute(
        '''insert into TagSource(name)
           values ("native"), ("spotify"), ("itunes"), ("celeris-google-search")''')

    con.commit()
    print("Done")
except sqlite3.OperationalError as ex:
    print(ex)
except sqlite3.IntegrityError:
    print("Records already exist")

print("creating table TagState", end=": ")
try:
    cur.execute(
        '''CREATE TABLE TagState
           (id integer primary key autoincrement,
            name varchar unique not null)''')

    con.commit()
    print("Done")
except sqlite3.OperationalError as ex:
    print(ex)

print("filling table TagState", end=": ")
try:
    cur.execute(
        '''insert into TagState(name)
           values ("pending"), ("parsing"), ("ready"), ("error")''')

    con.commit()
    print("Done")
except sqlite3.OperationalError as ex:
    print(ex)
except sqlite3.IntegrityError:
    print("Records already exist")

con.close()
