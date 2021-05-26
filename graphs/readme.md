After exporting the graphs with ```--export-graphs```, you can visualize them as follows.

* run the script **viewer.py** within the **graphs** folder by using the command

```./viewer.py <input.gv>```

where ```<input.gv>``` is the graph to display. Graphviz is needed in this case;
* run the command: ```dot -Tps <input.gv> -o <output.ps>```.