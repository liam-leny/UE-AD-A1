import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc
import showtime_pb2
import showtime_pb2_grpc
import json


class BookingServicer(booking_pb2_grpc.BookingServicer):

    def __init__(self):
        with open("{}/booking/data/bookings.json".format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]

    def GetBookingByUserID(self, request, context):
        """
        This method handles the request to fetch booking details by user ID.
        If the user is found in the bookings list, it returns their booking data.
        """
        for booking in self.db:
            if booking["userid"] == request.userid:
                return self._to_booking_data(booking)
        context.set_details("User ID not found")
        context.set_code(grpc.StatusCode.NOT_FOUND)
        return booking_pb2.BookingData()

    def AddBooking(self, request, context):
        """
        This method handles the request to add a new booking.
        It checks the Showtime service for movie availability on the requested date,
        and if available, adds the booking to the database.
        """
        # Connection to the Showtime service to verify the availability
        with grpc.insecure_channel("localhost:3202") as channel:
            showtime_stub = showtime_pb2_grpc.ShowtimeStub(channel)
            try:
                # Call GetShowtimesByDate to get the movies available on the requested date
                showtime_response = showtime_stub.GetShowtimesByDate(
                    showtime_pb2.DateRequest(date=request.date)
                )
                if request.movieid not in showtime_response.movies:
                    return booking_pb2.BookingResponse(
                        message="",
                        error="The movie is not available on the requested date",
                    )
            except grpc.RpcError as e:
                return booking_pb2.BookingResponse(
                    message="",
                    error="Error contacting Showtime service: " + e.details(),
                )

        # Add the booking
        for booking in self.db:
            if booking["userid"] == request.userid:
                for date_entry in booking["dates"]:
                    if date_entry["date"] == request.date:
                        date_entry["movies"].append(request.movieid)
                        self._write_bookings()
                        return booking_pb2.BookingResponse(
                            message="Booking added successfully", error=""
                        )

                booking["dates"].append(
                    {"date": request.date, "movies": [request.movieid]}
                )
                self._write_bookings()
                return booking_pb2.BookingResponse(
                    message="Booking added successfully", error=""
                )

        # Create a new booking if the user doesn't exist
        new_booking = {
            "userid": request.userid,
            "dates": [{"date": request.date, "movies": [request.movieid]}],
        }
        self.db.append(new_booking)
        self._write_bookings()
        return booking_pb2.BookingResponse(
            message="Booking added successfully", error=""
        )

    def GetAllBookings(self, request, context):
        """
        This method handles the request to fetch all bookings.
        It returns a list of all bookings in the database.
        """
        for booking in self.db:
            yield self._to_booking_data(booking)

    def _to_booking_data(self, booking):
        """
        Helper method to convert a booking record to a BookingData protobuf message.
        """
        return booking_pb2.BookingData(
            userid=booking["userid"],
            dates=[
                booking_pb2.DateEntry(date=d["date"], movies=d["movies"])
                for d in booking["dates"]
            ],
        )

    def _write_bookings(self):
        """
        Helper method to save the updated bookings data back to the JSON file.
        """
        with open("./booking/data/bookings.json", "w") as f:
            json.dump({"bookings": self.db}, f, indent=2)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port("[::]:3201")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
