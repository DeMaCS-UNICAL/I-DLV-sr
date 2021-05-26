If you have an input stream log file and you want to run the system in socked-based mode, you can simulate a stream source socket service by using the Python script **sender.py** within the **stream_socker_service** folder in the repository.

To execute the script, use the following command.

```./sender.py <input_period(s)> <n_events_tosend> <path_to_the_input_log_file> <port_number>```

where:
* ```<input_period(s)>``` indicates how many seconds to wait before sending a new line of the input stream log;
* ```<n_events_tosend>``` indicated how many lines of the input stream log have to be sent;
* ```<path_to_the_input_log_file>``` indicates the input stream log file to send;
* ```<port_number>``` indicates the port where the socket based-service have to be started;

This script periodically sends a new line of the input stream log to I-DLV-sr until either it ends the content of the file or it reaches the maximum number of line to be sent.

Examples:
* ```./sender.py 0 2000 input.log 9000``` starts the socket based-service at localhost on port *9000* and sends *2000* lines of the file *input.log* at once;
* ```./sender.py 0.3 50 input.log 9500``` starts the socket based-service at localhost on port *9500* and sends *50* events of the file *input.log* with a period of one event every *0.3* seconds.