# I-DLV-sr

I-DLV-s is a logic-based system for reasoning over data streams, which relies on a tight, fine-tuned interaction between the [Apache Flink](https://flink.apache.org/) Stream Processor and the [I<sup>2</sup>-DLV](https://github.com/DeMaCS-UNICAL/I-DLV/wiki/Incremental-IDLV) system.

The architecture allows to take advantage from both the powerful distributed stream processing capabilities of Apache Flink and the incremental reasoning capabilities of I<sup>2</sup>-DLV, based on overgrounding techniques.

## Download

A beta release of I-DLV-sr for Linux x86-64 is available [here](https://github.com/DeMaCS-UNICAL/I-DLV-sr/releases/tag/v1.0).

Requirements include:
* Java 11
* Graphviz (optional)

## Usage

I-DLV-sr can run in two different modes: **socket-based** and **file-based**.

### **Socket-based**

I-DLV-sr reads the input stream from a source socket. Once running, it waits for input events until the socket is open.

In the socket-based mode, one should:

1. Start up the service providing the input stream.
   For instance, one can run netcat from a command line to start a socket based-service: ```nc -l <ip_address> <port_number>```.
2. Start up I-DLV-sr as follows:
```
java -jar I-DLV-sr.jar --program=<path_to_the_program> --hostname=<ip_address> --port=<port_number>
```
The port number and the IP address can change at will.

Note that the port number and the IP address of the socket-based service and I-DLV-sr must coincide.
By default, in I-DLV-sr *hostname=localhost* and *port=9000*.

### **File-based**

I-DLV-sr reads the input stream from a log file. Once running, it reads all input events up to the end of the file.

In the file-based mode, one should just execute:
```
java -jar I-DLV-sr.jar --program=<path_to_the_program> --log=<path_to_the_input_stream_file>
```

## Input Language

### Program
I-DLV-sr accepts as input programs whose syntax extends [ASP-Core-2](https://arxiv.org/abs/1911.04326) with so-called streaming literals.

An I-DLV-sr program contains rules of one out of the two forms:
1. α : - l<sub>1</sub>, ... , l<sub>b</sub>.
2. **\#temp** α : - l<sub>1</sub>, . . . , l<sub>b</sub>.

where:
* *α* is a predicate atom of the form *p(t<sub>1</sub>,...,t<sub>n</sub>)* as in [ASP-Core-2](https://arxiv.org/abs/1911.04326)
* *l<sub>1</sub>, ... , l<sub>b</sub>* is a conjunction of streaming literals

Let *α* be a predicate atom, *c ∈ N+* a constant, *t* be a term and *D={d<sub>1</sub>, ... , d<sub>m</sub>}* be a set of natural numbers.
The I-DLV-sr language includes three types of streaming atoms:
* α **at least** c **in** {d<sub>1</sub>, ... , d<sub>m</sub>}: 
  intuitively, it holds if *α* is true *at least c* times within time points identified by *{d<sub>1</sub>, ... , d<sub>m</sub>}*;
* α **always in** {d<sub>1</sub>, ... , d<sub>m</sub>}:
  intuitively, it holds if *α* is *always* true within within time points identified by *{d<sub>1</sub>, ... , d<sub>m</sub>}*;
* α **count** t **in** {d<sub>1</sub>, ... , d<sub>m</sub>}: 
  intuitively, it counts how many time *α* is true within time points identified by *{d<sub>1</sub>, ... , d<sub>m</sub>}*.
  When *t* is a constant greater than *0*, it holds if *α* is true exactly *t* times.
  When *t* is a variable, it assigns to *t* the number of times *α* is true.
  
Let *s* be a streaming atom of any type and *t<sup>e</sup>* be the time evaluation time point, the set of natural numbers *D={d<sub>1</sub>, ... , d<sub>m</sub>}* defines how we have to look back starting from *t<sup>e</sup>* when evaluating *s*: *s* will be evaluated within the time points defined by {t<sup>e</sup>-d<sub>1</sub>, ... ,t<sup>e</sup>-d<sub>m</sub>}. 

For instance, if *s = α **always in** {0, 1, 2, 3}* and *t<sup>e</sup>=10*, then *s* will be evaluated over the time points *{10, 9, 8, 7}*.

If *D = {n ∈ N s.t. 0 ≤ n ≤ w ∧ w > 0}* we indicate it simply as **[w]**; e.g., we write *α **always in** [3]* instead of *α **always in** {0, 1, 2, 3}*.

When *s* is a streaming atom, a streaming literal can be either the positive literal (*s*) or the negative literal (***not*** *s*); ***not*** denotes negation as failure.

Moreover, the following shortcuts are admitted:
- *α **in** {d<sub>1</sub>, ... , d<sub>m</sub>}* in place of *α **at least** 1 **in** {d<sub>1</sub>, ... , d<sub>m</sub>}*;
- *α* in place of *α **at least** 1 **in** {0}* (this is called “degenerate” form of a streaming literal);
- *α **at most** c **in** {d<sub>1</sub>, ... , d<sub>m</sub>}* in place of not *α **at least** c' **in** {d<sub>1</sub>, ... , d<sub>m</sub>}* where *c'=c+1*.

By default, the time unit is *second*. In order to change this setting, one can:
1. use the option ```--window-unit=unit```: I-DLV-sr will globally set up the time unit to ```unit``` for all streaming atoms that do not have an explicit time unit.
2. specify the time unit within windows: I-DLV-sr will locally set up the time unit for the streaming atom that contains it; this means that each window can have their own time unit if locally specified.
Currently, the accepted time units are: ```sec```, ```min``` and ```hrs``` (resp., seconds, minutes and hours).

Besides streaming literals, I-DLV-sr also supports built-atoms and aggregate literals as defined in [ASP-Core-2](https://arxiv.org/abs/1911.04326); currently, the only restriction is that aggregate elements cannot feature (non-degenerate) streaming literals.

### Input Stream Log

When referring to time in a program (for example in windows), one can refer to different notions of time:
* **processing time:** is to the system time of the machine that is evaluating the program
* **event time:** is the time at which each event occurred in the source.

I-DLV-sr relies on the event time notion.
It requires that the input stream consists of a log chronologically ordered elements of the form:
``` 
timestamp p_1; ... p_n;
```
where ```timestamp``` is a date-time timestamp and ```p_1; ... p_n;``` is a list of ground predicate atoms (i.e., [ASP-Core-2](https://arxiv.org/abs/1911.04326) facts) true at that timestamp.
Each timestamp of the input stream log represents a *time point*.

### Example

Let us imagine we want to build a monitoring system for the underground trains in the city of Milan. Given a station, passengers expect to see a train stopping every 3–6 minutes, during the rush hours.

The following I-DLV-sr program models a simple control system that warns passengers when this regularity is broken to several extents (i.e., mild/grave irregularity).
``` 
irregular :- not train_pass in [6].
irregular :- train_pass, train_pass count X in {1,2}, X>0.
#temp numanomalies(X) :- irregular count X in [30].
mildalert :- numanomalies(X), X>2, X<=5.
severealert :-numanomalies(X), X>5.
``` 
A possible input stream log could be the following:
```
2020-05-26T12:16:18 train_pass; 
2020-05-26T12:16:23 train_pass; 
2020-05-26T12:16:24 
2020-05-26T12:16:25 train_pass; 
```
Let us assume to be at the time point ```2020-05-26T12:16:25```.
An irregularity is detected thanks to the second rule of the program: ```irregular``` is inferred because all the streaming atoms within its body hold. 
In particular:
* ```train_pass``` (shortcut for ```train_pass at least 1 in {0}```) holds because the predicate atom ```train_pass``` is given as input at the time point ```2020-05-26T12:16:25```;
* ```train_pass count X in {1,2}``` counts how many times ```train_pass``` is true within the time points *{2020-05-26T12:16:24, 2020-05-26T12:16:23}* (i.e., *{2020-05-26T12:16:25 - 1sec, 2020-05-26T12:16:25 - 2sec}*),
  then it assigns then it assigns 1 to *X* because because ```train_pass``` is true only at time point ```2020-05-26T12:16:23```;
* ```X>0``` holds because *1>0*.

Note that ```numanomalies(1)``` is also inferred since when evaluating ```irregular count X in [30]``` the count amounts to 1 within a window of the last 30 seconds constructed starting from ```2020-05-26T12:16:25```.

Note that since the program does not define an explicit time unit for the streaming atoms, the system uses *seconds* by default.

## Command-line Options

* ```--hostname=<ip>``` set the source ip address (default: "localhost")
* ```--port-number=<int>```set the source port number (default: 9000)
* ```--program``` (required) path to the program file
* ```--log``` path to the input log file
* ```--semi-incremental-reasoning``` enable the semi-incremental reasoning i.e., an incremental I-DLV instance per worker is used (default: disabled)
* ```--parallelism=<int>``` set the default parallelism of the execution environment, i.e., a default parallelism for all operators within the Apache Flink dataflow (default: the number of processors of the machine that runs the system)
* ```--windows-unit=<sec|min|hrs>``` assign the specified timeunit to streaming atoms whose timeunit is not explicitly declared within the program
* ```--complete-windows``` disable the evaluation of "always" atoms over partial windows, i.e., windows whose lower bound is less than the first event's timestamp
* ```--export-graphs``` export the stream dependency, component and macro-node graphs (see "graphs" folder)
* ```--print-extended-log``` print an extended version of the output log with additional information
* ```--print-stats``` print processing and time statistics
* ```--help``` print the help

## Additional resources

### Simulate a Source Socket

If you have an input stream log file and you want to run the system in socked-based mode, you can simulate a stream source socket service by using the Python script **sender.py** within the **stream_socker_service** folder in the repository.

To execute the script on a Linux bash type:

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

### Visualize the Stream Dependency, Component and Macro-node graphs

After exporting the graphs with ```--export-graphs```, on a Linux bash you can visualize them as follows. Graphviz is needed in this case.

1. execute the script **viewer.py**, reported in the **graphs** folder of this repository, as follows:
   ```./viewer.py <input.gv>```
   where ```<input.gv>``` is the graph to display

2. run the command: ```dot -Tps <input.gv> -o <output.ps>```

## ICLP 2021 Submission

The benchmarks used for the experimental analysis described in the paper are available in the folder: **ICLP2021-Experiments** of this repository.
The folder contains the related *Programs* and *Logs*, for each compared system ([Distributed-SR](http://distributed-stream-reasoner.ainf.at/prototype/) and I-DLV-sr) and for each performed test.

## Contacts

For further information, contact [i-dlv@googlegroups.com](mailto:i-dlv@googlegroups.com).
