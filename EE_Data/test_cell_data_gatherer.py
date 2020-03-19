''' module which holds the perpetual, but interruptable loop'''
import configparser
import logging.config
import os
import sys, getopt
import signal

from time import sleep

import EE_Data.test_cell_interface_functions as tc
from EE_Data.tc_trigger_class import Gather_Class as Gatherer

keep_running = True

log_config_check = os.path.isfile('log_config.conf')
if log_config_check:
    # setup the config file based logger
    logging.config.fileConfig(fname='log_config.conf',
                              disable_existing_loggers=False)
    # Get the logger specified in the file
    logger = logging.getLogger("test_cell_logger")
else:
    input("Logging setup file not found. Hit enter to exit")


#def signal_handler(signal, frame):
#    '''signal handler, this detects the ctrl+c input which cancels
#    the perpetual loop '''
##    global keep_running
#    logger.info("exiting")
#    # print("exiting")
#    keep_running = False


def config_file_checker():
    '''simple function to check for config file prescence'''

    logger.debug("checking for config files")

    log_config_check = os.path.isfile('log_config.conf')

    if not log_config_check:
        logger.debug("missing log_config.conf")

    data_gatherer_check = os.path.isfile('data_gatherer_config.ini')

    if not data_gatherer_check:
        logger.debug("missing data_gatherer_config.conf")

    master_check = log_config_check and data_gatherer_check

    if master_check is False:
        print("Missing a config file go check:")
        print("\t Log config (log_config.conf): \t", log_config_check)
        print("\t Data gatherer config (data_gatherer_config.ini): \t",
              data_gatherer_check)
        input("hit enter to end")

    return master_check


if __name__ == '__main__':
    ''' main function of the program, all starts here'''



    argv = sys.argv[1:]
    testing_mode = False
    try:
        opts, args = getopt.getopt(argv,"ht:",["testing_mode="])
    except getopt.GetoptError:
        print('Options: /n -t Test mode flag, any value will make it true')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Options: -t Test mode flag, any value will make it true')
            sys.exit()
        elif opt in ("-t", "--testing_mode_Bool"):
            testing_mode = True

    # never ending loop variable
    keep_running = True

    # testing logging, say hi
    logger.info("start")

    # check we have the required config files
    config_check = config_file_checker()

    # as long as we have the config files lets get going
    if config_check:
        # fetch the config data
        config = configparser.ConfigParser()
        config.read('data_gatherer_config.ini')
        config_data = config['config']
        # create a gathering instance
        trigger = Gatherer(config_data, testing_mode)

        while keep_running:
            trigger.trigger_read()

            sleep(int(config_data['trigger_interval']))
    else:
        logger.error("Data gatherer failed to start, lack of config files")
