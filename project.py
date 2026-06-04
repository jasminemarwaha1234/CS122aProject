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
    pass

def cancel_reservation(eid, snum, uid):
    #spencer
    pass

def update_event(eid, title, datetime):
    #spencer
    pass

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
