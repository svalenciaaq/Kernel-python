#!/usr/bin/python
import kernel as Kernel
import threading


h2 = threading.Thread(target=Kernel.Kernel)
h2.start()
