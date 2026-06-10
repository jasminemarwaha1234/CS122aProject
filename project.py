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
    pass

def insert_admin(uid, email, username, joined, firstname, lastname):
    #jasmine
    pass

def add_venue(eid, vid, is_primary):
    #jasmine
    pass

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
            print("fail")
            return
        cursor.execute(
            "UPDATE Slot SET is_reserved = 1 WHERE eid = %s AND snum = %s",
            (eid, snum)
        )

        cursor.execute(
            "INSERT INTO Reservation (eid, snum, uid) VALUES (%s, %s, %s)",
            (eid, snum, uid)
        )
        conn.commit()
        print("success")
    except:
        print("fail 2")
    finally:
        cursor.close()
        conn.close()


def cancel_reservation(eid, snum, uid):
    #spencer
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT is_reversed FROM Slot WHERE eid = %s AND snum = %s",
            (eid, snum)
        )

        row = cursor.fetchone()
        if row is None or row[0] == 0:
            print("fail")
            return
        
        cursor.execute(
            "SELECT * FROM Reservation WHERE eid = %s AND snum = %s AND uid = %s",
            (eid, snum, uid)
        )

        if cursor.fetchone() is None:
            print("fail 2")
            return

        cursor.execute(
            delete FROM Reservation WHERE eid = %s AND snum = %s AND uid = %s",
            (eid, snum, uid)
        )

        cursor.execute(
            "UPDATE Slot SET is_reserved = 0 WHERE eid = %s AND snum = %s",
            (eid, snum)
        )
        conn.commit()
        print("yippee")
    except:
        print("fail 3")
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
            print("fail")
        else:
            conn.commit()
            print("success")
    except:
        print("fail 2")
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
    pass

def organizer_stats(n):
    pass

def venue_events(vid):
    pass

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
