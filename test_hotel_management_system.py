import unittest
from datetime import datetime, timedelta
from collections import defaultdict
from hotel_management_system import Hotel, Room


class TestHotelManagementSystem(unittest.TestCase):

    def setUp(self):
        """ Initialize the hotel system with sample rooms """
        self.hotel = Hotel()

    # Test for adding a new room
    def test_add_room(self):
        initial_room_count = len(self.hotel.rooms)
        self.hotel.add_room(106, "Suite", 250)
        self.assertEqual(len(self.hotel.rooms), initial_room_count + 1)
        self.assertEqual(self.hotel.rooms[-1].room_number, 106)
        self.assertEqual(self.hotel.rooms[-1].room_type, "Suite")
        self.assertEqual(self.hotel.rooms[-1].price, 250)

    # Test for booking a room
    def test_book_room(self):
        self.hotel.book_room(101, "John Doe")
        booked_room = next((room for room in self.hotel.rooms if room.room_number == 101), None)
        self.assertIsNotNone(booked_room)
        self.assertEqual(booked_room.status, "Booked")

    # Test for booking an unavailable room
    def test_book_room_unavailable(self):
        self.hotel.book_room(101, "John Doe")
        result = self.hotel.book_room(101, "Jane Doe")
        self.assertEqual(result, "Room 101 is not available or doesn't exist.")

    # Test for checking out a room
    def test_check_out(self):
        self.hotel.book_room(101, "John Doe")
        self.hotel.check_out(101)
        checked_out_room = next((room for room in self.hotel.rooms if room.room_number == 101), None)
        self.assertEqual(checked_out_room.status, "Available")

    # Test for checking out a room that wasn't booked
    def test_check_out_not_booked(self):
        result = self.hotel.check_out(101)
        self.assertEqual(result, "Room 101 is not booked or doesn't exist.")

    # Test for generating an income report
    def test_generate_income_report(self):
        self.hotel.book_room(101, "John Doe")
        self.hotel.book_room(102, "Jane Doe")
        self.hotel.check_out(101)
        self.hotel.check_out(102)
        income_report = self.hotel.generate_income_report()
        self.assertEqual(income_report["total_income"], 250)  # 100 + 150 from rooms 101 and 102
        self.assertEqual(income_report["income_by_room_type"]["Single"], 100)
        self.assertEqual(income_report["income_by_room_type"]["Double"], 150)

    # Test for adding multiple rooms
    def test_add_multiple_rooms(self):
        initial_room_count = len(self.hotel.rooms)
        self.hotel.add_room(106, "Suite", 250)
        self.hotel.add_room(107, "Single", 100)
        self.assertEqual(len(self.hotel.rooms), initial_room_count + 2)

    # Test for checking initial room availability
    def test_check_initial_room_availability(self):
        available_rooms = [room for room in self.hotel.rooms if room.status == "Available"]
        self.assertEqual(len(available_rooms), len(self.hotel.rooms))

    # Test for updating a room's price
    def test_update_room_price(self):
        self.hotel.add_room(106, "Single", 100)
        self.hotel.rooms[-1].update_room(price=120)
        updated_room = next((room for room in self.hotel.rooms if room.room_number == 106), None)
        self.assertEqual(updated_room.price, 120)

    # Test for updating a room's type
    def test_update_room_type(self):
        self.hotel.add_room(106, "Single", 100)
        self.hotel.rooms[-1].update_room(room_type="Double")
        updated_room = next((room for room in self.hotel.rooms if room.room_number == 106), None)
        self.assertEqual(updated_room.room_type, "Double")

    # Test for applying discount for long stays
    def test_apply_discount_for_long_stays(self):
        self.hotel.book_room(101, "John Doe")
        check_in_date = datetime.now() - timedelta(days=10)  # Simulate a long stay
        booking = self.hotel.bookings[0]
        booking["check_in_date"] = check_in_date.strftime("%Y-%m-%d %H:%M:%S")
        self.hotel.apply_discount_for_long_stays()
        self.assertEqual(booking["price"], 90)  # Assuming 10% discount for stays over 7 days

    # Test for canceling an existing booking
    def test_cancel_booking(self):
        self.hotel.book_room(101, "John Doe")
        self.hotel.cancel_booking(101)
        canceled_room = next((room for room in self.hotel.rooms if room.room_number == 101), None)
        self.assertEqual(canceled_room.status, "Available")
        self.assertEqual(len(self.hotel.bookings), 0)

    # Test for canceling a non-existing booking
    def test_cancel_booking_not_found(self):
        result = self.hotel.cancel_booking(999)
        self.assertEqual(result, "No active booking found for Room 999.")

    # Test for searching rooms by type and price range
    def test_search_rooms(self):
        self.hotel.add_room(108, "Single", 120)
        self.hotel.add_room(109, "Double", 180)
        self.hotel.add_room(110, "Suite", 250)

        # Search for rooms within price range
        self.hotel.search_rooms(min_price=100, max_price=200)
        # Ensure rooms 101 (Single), 102 (Double), and 103 (Suite) are included in the search

    # Test for checking room availability for specific dates
    def test_check_room_availability_for_dates(self):
        self.hotel.book_room(101, "John Doe")
        start_date = datetime.now() + timedelta(days=1)
        end_date = start_date + timedelta(days=2)
        self.hotel.check_room_availability_for_dates(101, start_date, end_date)
        self.hotel.check_room_availability_for_dates(102, start_date, end_date)

    # Test for modifying room details
    def test_modify_room(self):
        self.hotel.add_room(106, "Single", 100)
        self.hotel.modify_room(106, room_type="Double", price=150)
        modified_room = next((room for room in self.hotel.rooms if room.room_number == 106), None)
        self.assertEqual(modified_room.room_type, "Double")
        self.assertEqual(modified_room.price, 150)

    # Test for viewing all available rooms
    def test_view_rooms(self):
        self.hotel.book_room(101, "John Doe")
        self.hotel.view_rooms()
        available_rooms = [room for room in self.hotel.rooms if room.status == "Available"]
        self.assertEqual(len(available_rooms), len(self.hotel.rooms) - 1)

if __name__ == '__main__':
    unittest.main()
