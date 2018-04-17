## System Monitoring tools

Tools to monitor consumption of system resources (CPU and RAM memory).

---

Monitor the resources of consumption of a running executable `BINARY.exe`.
It monitors virtual memory (allocated memory), shared memory (useful for parallel runs), and resident memory (actual used memory).

In case `BINARY.exe` is running in parallel, it logs into an ASCII file `FNAME_OUT` the consumption given by each instance too.

The monitoring process dies either when the process finishes or when its killed by hand.

    $ ./monit_process.py -h
    usage: monit_process.py [-h] [-fo FNAME_OUT] [-pn PROC_NAME]

    Script to monitor memory info about processes that match a given pattern.

    optional arguments:
      -h, --help            show this help message and exit
      -fo FNAME_OUT, --fname_out FNAME_OUT
                            output filename. (default: test.txt)
      -pn PROC_NAME, --proc_name PROC_NAME
                            pattern for the process command we seek for (default:
                            BINARY.exe)

---
## Physical quantities

Some handy functions in [phys.py](./phys.py).
See:

    ./calc_beta.py -Ek 1e9

<!--- EOF -->
