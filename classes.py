import csv
from collections import defaultdict

class Station:
    def __init__(self, name, lines):
        self.name = name
        self.lines = lines
 
class Line:
    def __init__(self, name, stations):
        self.name = name
        self.stations = stations

    def get_stations(self):
        return [station.name for station in self.stations]

def load_lines(file_path):
    lines = {}
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            line_name = row['line']
            station_names = row['stations'].split(';')
            stations = [Station(name, [line_name]) for name in station_names]
            line = Line(line_name, stations)
            lines[line_name] = line
    return lines

def load_stations(file_path):
    stations = {}
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            station_name = row['name']
            line_names = row['lines'].split(';')
            station = Station(station_name, line_names)
            stations[station_name] = station
    return stations

stations = load_stations('stations.csv')

# print(stations['Shaheed Sthal (New Bus Adda)'])

def get_station_by_name(name):
    return stations[name]

lines = load_lines('lines.csv')

def build_graph(lines):
    graph = defaultdict(list)
    for line in lines.values():
        for i in range(len(line.stations) - 1):
            graph[line.stations[i].name].append(line.stations[i + 1].name)
            graph[line.stations[i + 1].name].append(line.stations[i].name)

    return graph

graph = build_graph(lines)
# print(graph)

def find_shortest_path(graph, start, end):
    from collections import deque

    queue = deque([(start, [start])])
    visited = set()

    while queue:
        current_station, path = queue.popleft()
        if current_station == end:
            return [len(path), path]

        visited.add(current_station)

        for neighbor in graph[current_station]:
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))

    return None

def line_changes(path):
    changes = []
    current_line = None

    for i in range(len(path) - 1):
        station_a = get_station_by_name(path[i])
        station_b = get_station_by_name(path[i + 1])

        possible_lines = set(station_a.lines).intersection(set(station_b.lines))

        if current_line not in possible_lines:
            changes.append((path[i], list(possible_lines)))
            current_line = possible_lines.pop() if possible_lines else None

    return changes

# print(line_changes(find_shortest_path(graph, 'Shaheed Sthal (New Bus Adda)', 'Kirti Nagar')[1]))
# Find id of last ticket in tickets.csv
def get_last_ticket_id():
    try:
        with open('tickets.csv', mode='r') as file:
            csv_reader = csv.reader(file)
            last_row = None
            for last_row in csv_reader:
                pass
            if last_row:
                return int(last_row[0])
            else:
                return 0
    except:
        return 0

class Ticket:
    def __init__(self, from_station, to_station, id=None, save=False):
        path = find_shortest_path(graph, from_station, to_station)
        self.from_station = from_station
        self.to_station = to_station
        self.distance = path[0] - 1  # number of stations - 1
        self.path = path[1]
        self.line_changes = line_changes(self.path)
        if id is None:
            self.id = get_last_ticket_id() + 1
        else:
            self.id = id
        if save:
            self.save()
        # Sync with tickets.csv

    def get_route(self):
        return [self.path]
    
    def save(self):
        with open('tickets.csv', mode='a', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([self.id, self.from_station, self.to_station])
            file.flush()
    
    
def get_ticket_by_id(ticket_id):
    for ticket in load_tickets():
        if ticket.id == ticket_id:
            return ticket
    return None
                
def load_tickets():
  with open('tickets.csv', mode='r') as file:
    csv_reader = csv.reader(file)
    a=[]
    for row in csv_reader:
        ticket_id = int(row[0])
        from_station = row[1]
        to_station = row[2]
        ticket = Ticket(from_station, to_station, id=ticket_id)
        a.append(ticket)
    # file.sav()

    return a



        