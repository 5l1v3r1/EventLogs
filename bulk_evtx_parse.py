#!/usr/bin/env python
'''
Name: bulk_evtx_parse.py
Author: Matthew Green - @mgreen27
Version: 1.01, Python 2.7
License: Creative Commons Attribution 4.0 | You may privatize, fork, edit,
 teach, publish, or deploy for commercial use - with attribution in the text.

Description: 
    Script to carve and parse certain EventIDs (currently supporting
    4624,4625,4672) in large repositories of windows event log files
    where standard review may be tedious. The script will turn requested
    EventIDs into csv files for review in excel or ingestion into
    Elastic|Splunk. Included multiprocess capabilities so try to run
    on a machine with lots of cores for faster processing.

Requirements:
    Python-evtx, pip install python-evtx

Instructions:
    $ python bulk_evtx_parse.py </input/folder> </output/folder>
    $ python bulk_evtx_parse.py /cases/evtx /cases/result
    $ python bulk_evtx_parse.py -h
'''

from lxml import etree
import Evtx.Evtx as evtx
import Evtx.Views as e_views
import os, multiprocessing
from datetime import datetime

##### Initialisation #####
input_files = []
##########################

def worker(file, queue):
    worker_time = datetime.now()
    print "Processing " + file
    with evtx.Evtx(file) as log:
        for record in log.records():
            root = etree.fromstring(record.xml())
            # Process Successful logon events
            if root[0][1].text == "4624":
                out_line = str(root[0][1].text)+","+str(root[0][2].text)+","+str(root[0][3].text)+","+str(root[0][4].text)+","+str(root[0][5].text)+","+str(root[0][6].text)+","+str(root[0][7].attrib)[16:-9]+","+str(root[0][8].text)+","+str(root[0][11].text)+","+str(root[0][12].text)+","+str(root[1][0].text)+","+str(root[1][1].text)+","+str(root[1][2].text)+","+str(root[1][3].text)+","+str(root[1][4].text) +","+ str(root[1][5].text)+","+str(root[1][6].text)+","+str(root[1][7].text)+","+str(root[1][8].text)+","+str(root[1][9].text)+","+str(root[1][10].text)+"," + str(root[1][11].text) +","+ str(root[1][12].text) +","+ str(root[1][13].text) +","+str(root[1][14].text) +","+ str(root[1][15].text) +","+ str(root[1][16].text) +","+ str(root[1][17].text) +","+ str(root[1][18].text) +","+ str(root[1][19].text) + "\n"
                queue.put(out_line)
            # Process Unsuccessful logon events
            elif root[0][1].text == "4625":
                out_line = str(root[0][1].text)+","+str(root[0][2].text)+","+str(root[0][3].text)+","+str(root[0][4].text)+","+str(root[0][5].text)+","+str(root[0][6].text)+","+str(root[0][7].attrib)[16:-9]+","+str(root[0][8].text)+","+str(root[0][11].text)+","+str(root[0][12].text)+","+str(root[1][0].text)+","+str(root[1][1].text)+","+str(root[1][2].text)+","+str(root[1][3].text)+","+str(root[1][4].text) +","+ str(root[1][5].text)+","+str(root[1][6].text)+","+str(root[1][7].text)+","+str(root[1][8].text)+","+str(root[1][9].text)+","+str(root[1][10].text)+"," + str(root[1][11].text) +","+ str(root[1][12].text) +","+ str(root[1][13].text) +","+str(root[1][14].text)+","+str(root[1][15].text)+","+str(root[1][16].text)+","+str(root[1][17].text)+","+str(root[1][18].text)+","+str(root[1][19].text)+","+str(root[1][20].text)+"\n"
                queue.put(out_line)
            # Process Elevated privilages logon events
            elif root[0][1].text == "4672":
                out_line = str(root[0][1].text)+","+str(root[0][2].text)+","+str(root[0][3].text)+","+str(root[0][4].text)+","+str(root[0][5].text)+","+str(root[0][6].text)+","+str(root[0][7].attrib)[16:-9]+","+str(root[0][8].text)+","+str(root[0][11].text)+","+str(root[0][12].text)+","+str(root[1][0].text)+","+str(root[1][1].text)+","+str(root[1][2].text)+","+str(root[1][3].text)+","+str(root[1][4].text).replace('\t', ' ').replace('\n', ' ')+"\n"
                queue.put(out_line)
    print(file + " complete in: {}".format(datetime.now() - worker_time))


def listener(queue, output_folder):
    output_files = [os.path.join(output_folder, 'Evt4624.csv'), os.path.join(output_folder, 'Evt4625.csv'),os.path.join(output_folder, 'Evt4672.csv')]
    
    for output_file in output_files:
        try: os.remove(output_file)
        except: pass

    Evt4624Dump = open(os.path.join(output_folder, 'Evt4624.csv'), "a+")
    Evt4624Dump.write("EventID,Version,Level,Task,Opcode,Keywords,TimeCreatedUTC,EventRecordID,Channel,Computer,SubjectUserSid,SubjectUserName,SubjectDomainName,SubjectLogonId,TargetUserSid,TargetUserName,TargetDomainName,TargetLogonId,LogonType,LogonProcessName,AuthenticationPackageName,WorkstationName,LogonGuid,TransmittedServices,LmPackageName,KeyLength,ProcessId,ProcessName,IpAddress,IpPort\n")

    Evt4625Dump = open(os.path.join(output_folder, 'Evt4625.csv'), "a+")
    Evt4625Dump.write("EventID,Version,Level,Task,Opcode,Keywords,TimeCreatedUTC,EventRecordID,Channel,Computer,SubjectUserSid,SubjectUserName,SubjectDomainName,SubjectLogonId,TargetUserSid,TargetUserName,TargetDomainName,Status,FailureReason,SubStatus,LogonType,LogonProcessName,AuthenticationPackageName,WorkstationName,LmPackageName,KeyLength,ProcessId,ProcessName,IpAddress,IpPort\n")

    Evt4672Dump = open(os.path.join(output_folder, 'Evt4672.csv'), "a+")
    Evt4672Dump.write("EventID,Version,Level,Task,Opcode,Keywords,TimeCreatedUTC,EventRecordID,Channel,Computer,SubjectUserSid,SubjectUserName,SubjectDomainName,SubjectLogonId,PrivilegeList\n")

    while True:
        result = queue.get()
        if result == "kill":
            break
        elif "4624" in result:
            Evt4624Dump.write(result) 
            Evt4624Dump.flush()
        elif "4625" in result:
            Evt4625Dump.write(result) 
            Evt4625Dump.flush()
        elif "4672" in result:
            Evt4672Dump.write(result) 
            Evt4672Dump.flush()

    Evt4624Dump.close()
    Evt4625Dump.close()
    Evt4672Dump.close()

    for output_file in output_files:
        if os.stat(output_file).st_size<700:
            os.remove(output_file) 
        else:
            print "\nPlease review " + output_file   
    print "\n Complete"


def main():
    start_time = datetime.now()

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("input_folder", help="Input folder to parse event logs (evtx)")
    parser.add_argument("output_folder", help="Output folder to write output file 4624.csv")
    args = parser.parse_args()

    input_folder = os.path.join(args.input_folder, '')
    output_folder = os.path.join(args.output_folder, '')

    print "\nStarting processing event logs... \n"
    print "Folder to process: " + input_folder 
    print "Output folder: " + output_folder + "\n"

    print "\nPreparing files to parse..."
    for file in os.listdir(input_folder):
        if file.endswith(".evtx"):
            input_files.append(input_folder + file)
    print "Found " + str(len(input_files)) + " files \n"
    print "Using " + str(multiprocessing.cpu_count()) + " cores for work \n"
    
    #must use Manager queue here, or will not work
    manager = multiprocessing.Manager()
    queue = manager.Queue()    
    pool = multiprocessing.Pool(multiprocessing.cpu_count() + 2)

    #put listener to work first
    watcher = pool.apply_async(listener, (queue, output_folder))

    #fire off workers
    jobs = []
    for file in input_files:
        job = pool.apply_async(worker, (file, queue))
        jobs.append(job)
    # collect results from the workers through the pool result queue
    for job in jobs: 
        job.get()

    #now we are done, kill the listener
    queue.put('kill')
    pool.close() 

    print("Total duration: {}".format(datetime.now() - start_time))

if __name__ == "__main__":
    main()


