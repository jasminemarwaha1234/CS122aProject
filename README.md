# CS122A Project - ZotEvent

## Setup

### 1. Install MySQL (On MAC)
```bash
brew install mysql
brew services start mysql
```

### 2. Set up the database
```bash
mysql -u root
```
Then inside MySQL:
```sql
CREATE DATABASE cs122a;
CREATE USER 'test'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON cs122a.* TO 'test'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. Install Python connector
```bash
pip3 install mysql-connector-python
```

## Running the Program

```bash
cd Documents/CS122aProject
```

### Import data
```bash
python3 project.py import sample_data
```

### Insert admin
```bash
python3 project.py insertAdmin 1 admin@uci.edu awong 2024-04-19 Alice Wong
```

### Add venue
```bash
python3 project.py addVenue 10 3 true
```

### Reserve slot
```bash
python3 project.py reserveSlot 10 3 25
```

### Cancel reservation
```bash
python3 project.py cancelReservation 10 3 25
```

### Update event
```bash
python3 project.py updateEvent 10 "Database Seminar" "2026-05-15 15:00:00"
```

### Delete organizer
```bash
python3 project.py deleteOrganizer 12
```

### Available events
```bash
python3 project.py availableEvents 2026-05-01
```

### Popular event types
```bash
python3 project.py popularEventTypes 5
```

### Participant schedule
```bash
python3 project.py participantSchedule 25
```

### Organizer stats
```bash
python3 project.py organizerStats 3
```

### Venue events
```bash
python3 project.py venueEvents 7
```