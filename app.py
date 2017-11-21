import air_traffic as Flights
import helpers as Help

def air_traffic():

    Flights.Collect.tile(4, 1)

if __name__ == '__main__':

    Help.Config.set()

    Flights.Collect.tile(4, 1)
