# EventLogs
## Some EventLog parsing tools to use as templates

1. sysmon_parser.py - Sysmon event log parser (last used for version 6.02)
	
	$ python sysmon_parser.py /location/to/sysmon.evtx > /location/to.output.csv
	
		Supported EventIDs
		EventID 1 - Process Create events
		EventID 3 - Network events
		EventID 4 - Sysmon Service State Change
		EventID 5 - Process end event
		EventID 6 - Driver load events
		EventID 11 - File create events\n
		EventID 12 - RegistryEvent - Registry object added or deleted
		EventID 13 - RegistryEvent - Registry value set
		EventID 16 - Sysmon Config
		It is fairly straight forward to add event types.



2. bulk_evtx_parse.py - Parse certain EventIDs in large repositories of windows event log files (evtx) where standard review may be tedious. Output in csv, multiprocessing capable to optimise speed.
	
	$ python bulk_evtx_parse.py <input/folder> <output/folder>
		
		Supported EventIDs
		EventID 4624 - Logon Success
		EventID 4625 - Logon Failures
		EventID 4672 - Administrator privilages
		It is fairly straight forward to add event types.
		


3. bulk_evtx_search.py - A tool to search for keywords in large repositories of windows event log files (evtx) where standard review may be tedious. On search hit, output event record in Evtx xml format to outfile, multiprocessing capable to optimise speed
	
	$ python bulk_evtx_search.py -s "<search,strings,comma,delimited>" <input/folder> <output/file.path>
