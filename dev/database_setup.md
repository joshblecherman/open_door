# Setting up Postgres on Windows machine

I am using Windows 10 Home version 21H2 (OS build 19044.2486). I assume Mac/Linux follows very similar instructions but I could be wrong. Use at your own discretion.

1. Install Postgres from https://www.postgresql.org/download/. Select the version you want (I used version 15.2) and install. Set the installation directory, password, and port number. Default port is port 5432, and testing used the password "opendoor".

2. Finish and search for psql. The command-line took for psql should pop up. All of the defaults should be input, so just press enter until you get to the password prompt. When you get there, use the password you set.

3. Once the command prompt is open, paste the following code into the window:

FOR MAC: 

1. Save yourself a lot of time and go here https://postgresapp.com/downloads.html

```
CREATE TABLE IF NOT EXISTS profiles (
   user_id              VARCHAR(10) PRIMARY KEY,
   dorm                 VARCHAR(50),
   major                VARCHAR(50),
   description          VARCHAR(2000)
);

CREATE TABLE IF NOT EXISTS users (
   user_id              VARCHAR(10) PRIMARY KEY,
   password             VARCHAR(100) NOT NULL,
   profile              VARCHAR(10) NOT NULL REFERENCES profiles(user_id)
);

CREATE TABLE IF NOT EXISTS activities (
   activity_id          UUID PRIMARY KEY,                 
   title                VARCHAR(50) NOT NULL,
   place                VARCHAR(50) NOT NULL,
   description          VARCHAR(2000),
   time                 TIME NOT NULL,
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

CREATE TABLE IF NOT EXISTS ticketmaster_staging (
   id                   INT PRIMARY KEY,
   name                 VARCHAR(50) NOT NULL,
   time                 TIME NOT NULL
);
```

This will create the necessary tables.

This should be all you need to get the database up and running.