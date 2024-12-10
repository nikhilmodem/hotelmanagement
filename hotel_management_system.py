import os
import datetime
from collections import defaultdict


class Room:
    def __init__(self, room_number, room_type, price, status="Available"):
        self.room_number = room_number
        self.room_type = room_type
        self.price = price
        self.status = status  # Can be "Available" or "Booked"
        self.maintenance_status = "Good"  # New feature: Maintenance status of the room

    def __str__(self):
        return f"Room {self.room_number} ({self.room_type}) - ${self.price} - {self.status} - Maintenance: {self.maintenance_status}"

    def book(self):
        if self.status == "Available":
            self.status = "Booked"
            return True
        return False

    def check_out(self):
        if self.status == "Booked":
            self.status = "Available"
            return True
        return False

    def update_room(self, room_type=None, price=None):
        if room_type:
            self.room_type = room_type
        if price:
            self.price = price

    def schedule_maintenance(self):
        """ Mark the room for maintenance """
        self.maintenance_status = "Under Maintenance"

    def complete_maintenance(self):
        """ Mark the room as fully repaired and available """
        self.maintenance_status = "Good"


class Hotel:
    def __init__(self):
        self.rooms = []
        self.bookings = []
        self.load_rooms()

    def load_rooms(self):
        """ Load rooms from a predefined list of rooms (could be expanded to read from a file) """
        room_data = [
            {"room_number": 101, "room_type": "Single", "price": 100},
            {"room_number": 102, "room_type": "Double", "price": 150},
            {"room_number": 103, "room_type": "Suite", "price": 200},
            {"room_number": 104, "room_type": "Single", "price": 100},
            {"room_number": 105, "room_type": "Double", "price": 150},
            {"room_number": 105, "room_type": "Double", "price": 150},
            {"room_number": 105, "room_type": "Double", "price": 200},
            {"room_number": 105, "room_type": "Double", "price": 250},
            {"room_number": 105, "room_type": "Double", "price": 150},
            {"room_number": 105, "room_type": "Double", "price": 250},
            {"room_number": 105, "room_type": "Double", "price": 150},
            {"room_number": 105, "room_type": "Double", "price": 150},
            {"room_number": 105, "room_type": "Double", "price": 250},
            {"room_number": 105, "room_type": "Double", "price": 150},
            {"room_number": 105, "room_type": "Double", "price": 150},
            {"room_number": 105, "room_type": "Double", "price": 150},
            {"room_number": 105, "room_type": "Double", "price": 150},
            {"room_number": 105, "room_type": "Double", "price": 150},
            {"room_number": 105, "room_type": "Double", "price": 150},
            {"room_number": 105, "room_type": "Double", "price": 150},
            {"room_number": 105, "room_type": "Double", "price": 150},
            {"room_number": 105, "room_type": "Double", "price": 150},
            {"room_number": 105, "room_type": "Double", "price": 250},
            {"room_number": 105, "room_type": "Double", "price": 150},
            {"room_number": 105, "room_type": "Double", "price": 150},
            {"room_number": 105, "room_type": "Double", "price": 135},
            {"room_number": 105, "room_type": "Double", "price": 150},
            {"room_number": 105, "room_type": "Double", "price": 125},
            {"room_number": 105, "room_type": "Double", "price": 150},
            {"room_number": 105, "room_type": "Double", "price": 150},
            {"room_number": 105, "room_type": "Double", "price": 100},
            {"room_number": 105, "room_type": "Double", "price": 150},
            {"room_number": 105, "room_type": "Double", "price": 2000},
            {"room_number": 105, "room_type": "Double", "price": 150},
            {"room_number": 105, "room_type": "Double", "price": 150},
            {"room_number": 105, "room_type": "Double", "price": 250},
            {"room_number": 105, "room_type": "Double", "price": 250},



        ]

        for data in room_data:
            room = Room(data["room_number"], data["room_type"], data["price"])
            self.rooms.append(room)

    def add_room(self, room_number, room_type, price):
        """ Add a new room to the hotel """
        room = Room(room_number, room_type, price)
        self.rooms.append(room)
        print(f"Room {room_number} added successfully.")

    def view_rooms(self):
        """ View all available rooms """
        available_rooms = [str(room) for room in self.rooms if room.status == "Available"]
        return available_rooms if available_rooms else "No available rooms."

    def book_room(self, room_number, guest_name):
        for room in self.rooms:
            if room.room_number == room_number:
                if room.book():
                    check_in_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    booking = {
                        "guest_name": guest_name,
                        "room_number": room_number,
                        "check_in_date": check_in_date,
                        "room_type": room.room_type,
                        "price": room.price
                    }
                    self.bookings.append(booking)
                    return None  # Return None to indicate success
        return f"Room {room_number} is not available or doesn't exist."

    def check_out(self, room_number):
        for room in self.rooms:
            if room.room_number == room_number:
                if room.check_out():
                    for booking in self.bookings:
                        if booking["room_number"] == room_number:
                            check_out_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            booking["check_out_date"] = check_out_date
                            return f"Checked out of Room {room_number}. Thank you for your stay!"
        return f"Room {room_number} is not booked or doesn't exist."

    def cancel_booking(self, room_number):
        for booking in self.bookings:
            if booking["room_number"] == room_number and "check_out_date" not in booking:
                self.bookings.remove(booking)
                for room in self.rooms:
                    if room.room_number == room_number:
                        room.status = "Available"
                return f"Booking for Room {room_number} has been canceled."
        return f"No active booking found for Room {room_number}."

    def modify_room(self, room_number, room_type=None, price=None):
        for room in self.rooms:
            if room.room_number == room_number:
                room.update_room(room_type, price)
                return f"Room {room_number} updated successfully."
        return f"Room {room_number} not found."

    def search_rooms(self, room_type=None, min_price=None, max_price=None):
        results = []
        for room in self.rooms:
            if room_type and room.room_type != room_type:
                continue
            if min_price and room.price < min_price:
                continue
            if max_price and room.price > max_price:
                continue
            results.append(str(room))
        return results if results else "No rooms found matching the criteria."

    def generate_room_availability_report(self):
        report = [str(room) for room in self.rooms]
        return report if report else "No rooms available."

    def apply_discount_for_long_stays(self):
        discount_threshold = 7  # Days for discount eligibility
        applied_discounts = []
        for booking in self.bookings:
            if "check_out_date" not in booking:
                check_in_date = datetime.datetime.strptime(booking["check_in_date"], "%Y-%m-%d %H:%M:%S")
                current_date = datetime.datetime.now()
                days_stayed = (current_date - check_in_date).days
                if days_stayed >= discount_threshold:
                    original_price = booking["price"]
                    discounted_price = original_price * 0.9  # 10% discount
                    booking["price"] = discounted_price
                    applied_discounts.append(booking)
        return applied_discounts if applied_discounts else "No discounts applied."

    def check_room_availability_for_dates(self, room_number, start_date, end_date):
        """ Check room availability for specific dates """
        for room in self.rooms:
            if room.room_number == room_number:
                for booking in self.bookings:
                    if booking["room_number"] == room_number:
                        check_in_date = datetime.datetime.strptime(booking["check_in_date"], "%Y-%m-%d %H:%M:%S")
                        check_out_date = booking.get("check_out_date")
                        if check_out_date:
                            check_out_date = datetime.datetime.strptime(check_out_date, "%Y-%m-%d %H:%M:%S")
                            if start_date <= check_out_date and end_date >= check_in_date:
                                return f"Room {room_number} is not available between {start_date} and {end_date}."
                return f"Room {room_number} is available between {start_date} and {end_date}."
        return f"Room {room_number} not found."

    def generate_income_report(self):
        """ Generate an income report for the hotel """
        total_income = 0
        income_by_room_type = defaultdict(int)

        if not self.bookings:
            return {"total_income": 0, "income_by_room_type": {}}

        for booking in self.bookings:
            room_price = booking["price"]
            total_income += room_price
            income_by_room_type[booking["room_type"]] += room_price

        return {
            "total_income": total_income,
            "income_by_room_type": dict(income_by_room_type)
        }

    def perform_room_maintenance(self, room_number):
        """ Perform maintenance on a room """
        for room in self.rooms:
            if room.room_number == room_number:
                room.schedule_maintenance()
                return f"Room {room_number} is now under maintenance."
        return f"Room {room_number} not found."

    def complete_room_maintenance(self, room_number):
        """ Complete maintenance on a room """
        for room in self.rooms:
            if room.room_number == room_number:
                room.complete_maintenance()
                return f"Room {room_number} maintenance is complete and the room is available."
        return f"Room {room_number} not found."

    def add_special_offer(self, offer_description, discount_percent):
        """ Add a special offer for customers """
        return f"Special offer added: {offer_description} with a {discount_percent}% discount."

    def view_special_offers(self):
        """ View all available special offers """
        return "Currently, there are no special offers available."


# Example usage
if __name__ == "__main__":
    hotel = Hotel()
    hotel.add_room(106, "Suite", 250)
    print(hotel.view_rooms())
    hotel.book_room(106, "John Doe")
    print(hotel.check_out(106))
    print(hotel.perform_room_maintenance(106))
    print(hotel.complete_room_maintenance(106))
    print(hotel.add_special_offer("Winter Discount", 20))
    print(hotel.view_special_offers())
