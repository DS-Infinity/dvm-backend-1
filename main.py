import sys
from classes import Station, Line, Ticket, load_tickets, stations, get_ticket_by_id
import csv

tickets = load_tickets()

def main():
    print("Welcome to the Metro System")
    print("1. View Stations")
    print("2. Purchase Ticket")
    print("3. View Purchased Tickets")
    print("4. Lookup Ticket by ID")
    print("5. Exit")
    choice = input("Enter your choice: ")
    if choice == '1':
        for station in stations.values():
            print(f"Station: {station.name}, Lines: {', '.join(station.lines)}")
        main()
    if choice == '2':
        from_station = input("Enter from station: ")
        to_station = input("Enter to station: ")
        ticket = Ticket(from_station, to_station, save=True)
        print(f"Ticket purchased from {from_station} to {to_station}")
        print(f"Distance: {ticket.distance} stations")
        print(f"Path: {' -> '.join(ticket.path)}")
        print(f"Line Changes: {', '.join(' at '.join([change[1][0], change[0]]) for change in ticket.line_changes[1:])}")
        print(f"Your Ticket ID is: {ticket.id}")
        tickets.append(ticket)
        main()
    elif choice == '3':
        for ticket in tickets:
            print(f"Ticket ID: {ticket.id}, From: {ticket.from_station}, To: {ticket.to_station}")
        main()
    elif choice == '4':
        ticket_id = int(input("Enter ticket ID: "))
        ticket = Ticket(from_station="", to_station="", id=ticket_id)
        for ticket in tickets:
          if ticket.id == ticket_id:
            print(f"Ticket ID: {ticket.id}, From: {ticket.from_station}, To: {ticket.to_station}")
            print(f"Distance: {ticket.distance} stations")
            print(f"Path: {' -> '.join(ticket.path)}")
            if ticket.line_changes[1:]:
              print(f"Line Changes: {', '.join(' at '.join([change[1][0], change[0]]) for change in ticket.line_changes[1:])}")
            
          else:
              print("Ticket not found.")
        main()
    elif choice == '5':
        print("Exiting...")
        exit()
    else:
        print("Invalid choice. Please try again.")
        main()

def exit():
    sys.exit()

main()