# Setting up Postgres on Windows machine

I am using Windows 10 Home version 21H2 (OS build 19044.2486). I assume Mac/Linux follows very similar instructions but I could be wrong. Use at your own discretion.

1. Install Postgres from https://www.postgresql.org/download/. Select the version you want (I used version 15.2) and install. Set the installation directory, password, and port number. Default port is port 5432, and testing used the password "opendoor". Finish the installation (no need to install extra packages).

From here, you only need to run `create_tables()` in `db.sql` to create the tables.

FOR MAC: 

1. Save yourself a lot of time and go here https://postgresapp.com/downloads.html

## Accessing the command line

1. To access the command line tool for psql, search for "psql" in your windows search bar. The command-line took for psql should pop up. All of the defaults should be input, so just press enter until you get to the password prompt. When you get there, use the password you set. It should connect you to the database command prompt.

The database structure is as follows here (also seen in `db.py`)

```
CREATE TABLE IF NOT EXISTS profiles (
   net_id               VARCHAR(10) PRIMARY KEY,
   first_name           VARCHAR(50) NOT NULL,
   preferred_name       VARCHAR(50),
   middle_name          VARCHAR(50),
   last_name            VARCHAR(50) NOT NULL,
   dorm                 VARCHAR(50),
   major                VARCHAR(50),
   description          VARCHAR(2000)
);

CREATE TABLE IF NOT EXISTS users (
   net_id               VARCHAR(10) PRIMARY KEY,
   password             VARCHAR(100) NOT NULL,
   profile              VARCHAR(10) NOT NULL REFERENCES profiles(user_id)
);

CREATE TABLE IF NOT EXISTS activities (
   activity_id          UUID PRIMARY KEY,                 
   title                VARCHAR(50) NOT NULL,
   place                VARCHAR(50) NOT NULL,
   description          VARCHAR(2000),
   datetime             TIMESTAMP NOT NULL,
   fee                  INT NOT NULL,
   url                  VARCHAR(255),
   img                  BYTEA,
   reservation_needed   boolean NOT NULL,
   rsvp_list            VARCHAR(10)[]
);

CREATE TABLE IF NOT EXISTS student_events (
   id                   UUID REFERENCES activities(activity_id),
   notes                VARCHAR(2000)
);

/*
Every table below here will be empty in production.
They are only used to feed data from APIs into our database.
*/
CREATE TABLE IF NOT EXISTS ticketmaster (
   id                   INT PRIMARY KEY,
   name                 VARCHAR(50) NOT NULL,
   date                 DATE NOT NULL,
   time                 TIME NOT NULL,
   img_url              VARCHAR(255),
   url                  VARCHAR(255) NOT NULL
);
```

This will create the necessary tables.

This should be all you need to get the database up and running.