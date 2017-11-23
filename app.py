import air_traffic as Flights
import helpers as Help

def air_traffic(set_id, x, y):

    Flights.Collect.tile(set_id, x, y)

if __name__ == '__main__':

    Help.Config.set()

    # Flights.Collect.tile(4, 1)
