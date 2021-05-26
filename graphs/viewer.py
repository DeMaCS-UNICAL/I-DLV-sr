#!/usr/bin/env python3

from graphviz import Source
import sys

Source.from_file(sys.argv[1]).view()
