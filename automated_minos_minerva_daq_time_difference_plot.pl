#!/usr/bin/perl -w

#$SOURCE_DIR ="/home/minerva/cmtuser/Minerva_v10r9p1/Tools/ControlRoomTools/SmartShift";

$sleeptime = 596;
while (1) {
    print "Starting to create daq clock time difference plot at: ";
    $command="date";
    system($command);
    $command = "/home/minerva/cmtuser/Minerva_v10r9p1/Tools/ControlRoomTools/minos_minerva_daq_time_difference/live_minos_minerva_daq_time_difference_plot";
    system($command);
    sleep $sleeptime;
#    $command="_EOF_";
#    system($command);
_EOF_
}

##
# Need to Kerberize: source $HOME/mnvdaqrunscripts/Kerberize
# Run the script by doing perl web_screenshot_veto.pl
#
