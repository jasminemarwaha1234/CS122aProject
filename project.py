import sys
import os
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        user='test',
        password='password',
        database='cs122a'
    )

def import_data(folder):
    #jasmine
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DROP TABLE IF EXISTS Approval")
        cursor.execute("DROP TABLE IF EXISTS Hosting")
        cursor.execute("DROP TABLE IF EXISTS Slot")
        cursor.execute("DROP TABLE IF EXISTS Event")
        cursor.execute("DROP TABLE IF EXISTS OffCampus")
        cursor.execute("DROP TABLE IF EXISTS OnCampus")
        cursor.execute("DROP TABLE IF EXISTS Venue")
        cursor.execute("DROP TABLE IF EXISTS Administrator")
        cursor.execute("DROP TABLE IF EXISTS Participant")
        cursor.execute("DROP TABLE IF EXISTS Organizer")
        cursor.execute("DROP TABLE IF EXISTS User")

        cursor.execute("""
            CREATE TABLE User (
                uid INT,
                email TEXT NOT NULL,
                username TEXT NOT NULL,
                joined DATE NOT NULL,
                PRIMARY KEY (uid)
            )
        """)
        cursor.execute("""
            CREATE TABLE Organizer (
                uid INT,
                department TEXT NOT NULL,
                experience INT NOT NULL,
                PRIMARY KEY (uid),
                FOREIGN KEY (uid) REFERENCES User(uid) ON DELETE CASCADE
            )
        """)
        cursor.execute("""
            CREATE TABLE Participant (
                uid INT,
                type TEXT,
                PRIMARY KEY (uid),
                FOREIGN KEY (uid) REFERENCES User(uid) ON DELETE CASCADE
            )
        """)
        cursor.execute("""
            CREATE TABLE Administrator (
                uid INT,
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                PRIMARY KEY (uid),
                FOREIGN KEY (uid) REFERENCES User(uid) ON DELETE CASCADE
            )
        """)
        cursor.execute("""
            CREATE TABLE Event (
                eid INT,
                creator_uid INT NOT NULL,
                title TEXT NOT NULL,
                type TEXT NOT NULL,
                datetime DATETIME NOT NULL,
                PRIMARY KEY (eid),
                FOREIGN KEY (creator_uid) REFERENCES Organizer(uid) ON DELETE CASCADE
            )
        """)
        cursor.execute("""
            CREATE TABLE Slot (
                eid INT,
                snum INT NOT NULL,
                is_reserved BOOLEAN NOT NULL,
                uid INT,
                PRIMARY KEY (eid, snum),
                FOREIGN KEY (eid) REFERENCES Event(eid) ON DELETE CASCADE,
                FOREIGN KEY (uid) REFERENCES Participant(uid) ON DELETE CASCADE
            )
        """)
        cursor.execute("""
            CREATE TABLE Venue (
                vid INT,
                street TEXT NOT NULL,
                city TEXT NOT NULL,
                state TEXT NOT NULL,
                zip TEXT NOT NULL,
                PRIMARY KEY (vid)
            )
        """)
        cursor.execute("""
            CREATE TABLE OnCampus (
                vid INT,
                code TEXT NOT NULL,
                PRIMARY KEY (vid),
                FOREIGN KEY (vid) REFERENCES Venue(vid) ON DELETE CASCADE
            )
        """)
        cursor.execute("""
            CREATE TABLE OffCampus (
                vid INT,
                distance INT NOT NULL,
                PRIMARY KEY (vid),
                FOREIGN KEY (vid) REFERENCES Venue(vid) ON DELETE CASCADE
            )
        """)
        cursor.execute("""
            CREATE TABLE Hosting (
                eid INT NOT NULL,
                vid INT NOT NULL,
                is_primary BOOLEAN NOT NULL,
                PRIMARY KEY (eid, vid),
                FOREIGN KEY (eid) REFERENCES Event(eid) ON DELETE CASCADE,
                FOREIGN KEY (vid) REFERENCES Venue(vid) ON DELETE CASCADE
            )
        """)
        cursor.execute("""
            CREATE TABLE Approval (
                uid INT NOT NULL,
                vid INT NOT NULL,
                valid_from DATE NOT NULL,
                valid_until DATE NOT NULL,
                PRIMARY KEY (uid, vid),
                FOREIGN KEY (uid) REFERENCES Administrator(uid) ON DELETE CASCADE,
                FOREIGN KEY (vid) REFERENCES OffCampus(vid) ON DELETE CASCADE
            )
        """)

        tables = ['User', 'Organizer', 'Participant', 'Administrator',
                  'Event', 'Slot', 'Venue', 'OnCampus', 'OffCampus',
                  'Hosting', 'Approval']

        for table in tables:
            filepath = os.path.join(folder, f"{table}.csv")
            with open(filepath, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    values = line.split(',')
                    placeholders = ','.join(['%s'] * len(values))
                    values = [None if v == 'NULL' else v for v in values]
                    cursor.execute(f"INSERT INTO {table} VALUES ({placeholders})", values)

        conn.commit()
        print("Success")

    except Exception as e:
        print("Fail")
        print(e)

    finally:
        cursor.close()
        conn.close()

def insert_admin(uid, email, username, joined, firstname, lastname):
    #jasmine
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO User VALUES (%s, %s, %s, %s)", (uid, email, username, joined))
        cursor.execute("INSERT INTO Administrator VALUES (%s, %s, %s)", (uid, firstname, lastname))

        conn.commit()
        print("Success")

    except Exception as e:
        print("Fail")
        print(e)

    finally:
        cursor.close()
        conn.close()

def add_venue(eid, vid, is_primary):
    #jasmine
    try:
        conn = get_connection()
        cursor = conn.cursor()

        is_primary_bool = is_primary.lower() == 'true'

        if is_primary_bool:
            cursor.execute("SELECT * FROM Hosting WHERE eid = %s AND is_primary = true", (eid,))
            if cursor.fetchone():
                print("Fail")
                return

        cursor.execute("INSERT INTO Hosting VALUES (%s, %s, %s)", (eid, vid, is_primary_bool))
        conn.commit()
        print("Success")

    except Exception as e:
        print("Fail")
        print(e)

    finally:
        cursor.close()
        conn.close()

def reserve_slot(eid, snum, uid):
    #spencer
    try: 
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT is_reserved FROM Slot WHERE eid = %s AND snum = %s",
            (eid, snum)
        )
        row = cursor.fetchone()
        if row is None or row[0] == 1:
            print("Fail")
            return
        cursor.execute(
            "UPDATE Slot SET is_reserved = 1, uid = %s WHERE eid = %s AND snum = %s",
            (uid, eid, snum)
        )

        conn.commit()
        print("Success")
    except:
        print("Fail")
    finally:
        cursor.close()
        conn.close()


def cancel_reservation(eid, snum, uid):
    #spencer
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT is_reserved, uid FROM Slot WHERE eid = %s AND snum = %s",
            (eid, snum)
        )
        row = cursor.fetchone()
        if row is None or row[0] == 0 or str(row[1]) != str(uid):
            print("Fail")
            return

        cursor.execute(
            "UPDATE Slot SET is_reserved = 0, uid = NULL WHERE eid = %s AND snum = %s",
            (eid, snum)
        )
        conn.commit()
        print("Success")
    except:
        print("Fail")
    finally:
        cursor.close()
        conn.close()


def update_event(eid, title, datetime_val):
    #spencer
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE Event SET title = %s, datetime = %s WHERE eid = %s",
            (title, datetime_val, eid)
        )

        if cursor.rowcount == 0:
            print("Fail")
        else:
            conn.commit()
            print("Success")
    except:
        print("Fail")
    finally:
        cursor.close()
        conn.close()

def delete_organizer(uid):
    pass

def available_events(date):
    pass

def popular_event_types(n):
    pass

def participant_schedule(uid):
    # ryan
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT 
                e.eid,
                e.title,
                e.type,
                e.datetime,
                s.snum,
                v.vid,
                v.street,
                v.city,
                v.state,
                v.zip
            FROM Slot s
            JOIN Event e ON s.eid = e.eid
            LEFT JOIN Hosting h ON e.eid = h.eid AND h.is_primary = TRUE
            LEFT JOIN Venue v ON h.vid = v.vid
            WHERE s.uid = %s
            ORDER BY e.datetime ASC
        """

        cursor.execute(query, (uid,))
        rows = cursor.fetchall()

        for row in rows:
            print(','.join('' if val is None else str(val) for val in row))

    except Exception as e:
        print("Fail")
        print(e)

    finally:
        cursor.close()
        conn.close()

def organizer_stats(n):
    # ryan
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT
                o.uid,
                u.username,
                o.department,
                COUNT(e.eid) AS eventCount
            FROM Organizer o
            JOIN User u ON o.uid = u.uid
            LEFT JOIN Event e ON o.uid = e.creator_uid
            GROUP BY o.uid, u.username, o.department
            HAVING COUNT(e.eid) >= %s
            ORDER BY eventCount DESC, o.uid ASC
        """

        cursor.execute(query, (n,))
        rows = cursor.fetchall()

        for row in rows:
            print(','.join('' if val is None else str(val) for val in row))

    except Exception as e:
        print("Fail")
        print(e)

    finally:
        cursor.close()
        conn.close()

def venue_events(vid):
    # ryan
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT
                e.eid,
                e.title,
                e.type,
                e.datetime,
                h.is_primary
            FROM Hosting h
            JOIN Event e ON h.eid = e.eid
            WHERE h.vid = %s
            ORDER BY e.datetime ASC, e.eid ASC
        """

        cursor.execute(query, (vid,))
        rows = cursor.fetchall()

        for row in rows:
            print(','.join('' if val is None else str(val) for val in row))

    except Exception as e:
        print("Fail")
        print(e)

    finally:
        cursor.close()
        conn.close()

def main():
    func = sys.argv[1]

    if func == "import":
        import_data(sys.argv[2])
    elif func == "insertAdmin":
        insert_admin(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
    elif func == "addVenue":
        add_venue(sys.argv[2], sys.argv[3], sys.argv[4])
    elif func == "reserveSlot":
        reserve_slot(sys.argv[2], sys.argv[3], sys.argv[4])
    elif func == "cancelReservation":
        cancel_reservation(sys.argv[2], sys.argv[3], sys.argv[4])
    elif func == "updateEvent":
        update_event(sys.argv[2], sys.argv[3], sys.argv[4])
    elif func == "deleteOrganizer":
        delete_organizer(sys.argv[2])
    elif func == "availableEvents":
        available_events(sys.argv[2])
    elif func == "popularEventTypes":
        popular_event_types(sys.argv[2])
    elif func == "participantSchedule":
        participant_schedule(sys.argv[2])
    elif func == "organizerStats":
        organizer_stats(sys.argv[2])
    elif func == "venueEvents":
        venue_events(sys.argv[2])

if __name__ == "__main__":
    main()
