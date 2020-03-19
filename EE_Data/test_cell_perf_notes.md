# MOVED TO TEAMWORK AS A NOTEBOOK

## Welcome to the EE LT Test Cell Control logic interface program

## Python requirements

The following modules will need to be installed in the python instance via pip

1. Requests
2. Datetime
3. pandas
4. possibly numpy
5. csv

The following files will need to be included:

1. eip.py
2. lgxDevice.py
3. RepeatedTimer.py

The following folders need to be in the root folder:

1. archive
2. store

## History

This is an adaptation of the original CLX interface program written for PCM.

## TODO

[ ] convert to a class object based device
[ ] have a fast running routine which monitors for the performance test bit - 'EE_performance_point_trigger'
[ ] have a secondary class based device which then fetches data, confirms it is good and averages

## things to add

[x] If post fails then archive file in seperate folder
[ ] then when post is successful go to folder and post the rest
[ ] If archive gets bigger than x start wiping old files
[x] Check PLC is connected by ping first during data fetch, if not cancel out
    - currently goes straight to data fetch then once ot has data sends it
    - need to change to a ping check then if successful go to a data check
[ ] Re write to use CSV as input

## Method

PLC class, owns connection
has a method <trigger_check> to check the trigger, called every second by the rapid fire loop
has a method pull the data <data_pull> which returns either an dict, dataframe or a list
has a method <data_master> which calls <data_pull> X number of times (a config setting), once it has pulled the data it averages and stores
has a method <data_present> which then converts the averaged data to a properly formatted txt file for model center
has a method <mc_call> which then calls the model center code for the appropriate engine, for the performance report
has a method <integrity_present> which preps the data for the mechanical integrity report


## Stretch goals:
has a method to push the calculated T3 back to the PLC for HMI presentation
