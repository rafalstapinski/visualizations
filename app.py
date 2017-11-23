import air_traffic as Flights
import helpers as Help
import optparse
import sys

def air_traffic(set_id, x, y):

    Flights.Collect.tile(set_id, x, y)

if __name__ == '__main__':

    Help.Config.set()

    # Flights.Collect.tile(4, 1)

    parser = optparse.OptionParser()
    parser.add_option('--collect', action='store_true', default=False)
    parser.add_option('--display', action='store_true', default=False)
    parser.add_option('-x', action='store', type='int')
    parser.add_option('-y', action='store', type='int')
    parser.add_option('-s', action='store', type='int')

    options, remainder = parser.parse_args()

    if options.display:

        if not options.s:
            print 'No set id provided'
            sys.exit(1)

        disp = Flights.Display(options.s)
        disp.show()

    elif options['collect']:

        pass
