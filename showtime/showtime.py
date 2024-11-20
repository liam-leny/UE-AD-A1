import grpc
from concurrent import futures
import showtime_pb2
import showtime_pb2_grpc
import json


class ShowtimeServicer(showtime_pb2_grpc.ShowtimeServicer):

    def __init__(self):
        with open("{}/showtime/data/times.json".format("."), "r") as jsf:
            self.db = json.load(jsf)["schedule"]

    def GetShowtimes(self, request, context):
        """
        This method is called when the client requests showtimes.
        It will yield the showtimes for each entry in the schedule.
        """
        for showtime in self.db:
            yield showtime_pb2.ShowtimeData(
                date=showtime["date"], movies=showtime["movies"]
            )

    def GetShowtimesByDate(self, request, context):
        """
        This method is called when the client requests showtimes for a specific date.
        If the date is found in the schedule, the corresponding showtimes are returned.
        If the date is not found, a NOT_FOUND error is set.
        """
        for showtime in self.db:
            if showtime["date"] == request.date:
                return showtime_pb2.ShowtimeData(
                    date=showtime["date"], movies=showtime["movies"]
                )
        context.set_details("Date not found")
        context.set_code(grpc.StatusCode.NOT_FOUND)
        return showtime_pb2.ShowtimeData()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    showtime_pb2_grpc.add_ShowtimeServicer_to_server(ShowtimeServicer(), server)
    server.add_insecure_port("[::]:3202")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
