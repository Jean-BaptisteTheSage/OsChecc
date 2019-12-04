# OSChecc

This project was written to scan a  users local subnetwork and return estimates of all devices' operating systems.

## Dependencies

To run properly netifaces and nmap python packages must first be installed using the pip installer (Sidenote: python-nmap assumes the nmap command can be found in the PATH).

To install the python packages:

```
    pip install python-nmap netifaces
```

If nmap is not in the PATH:

```
    choco install nmap // for Windows OS
    sudo apt-get install nmap // for UNIX systems
```

## _Warnings_

This tool is for a network that is owned by the user **OR** a network the user has explicit permission to scan. Running this script will default to probing every device on the same subnetwork.

## Usage

To simply run a default scan on the clients' subnetwork use the command:
```
    ./scanner.py
```
_REMINDER_: Default behavior for this program is to search on the ENTIRE subnetwork so once again ensure permission to scan all devices has already been given.

For the more advanced user, this script also saves the nmap report detailing the actions taken under ```ip.txt``` . Such a file is useful for further debugging and to give easy access to useful nmap extensions this script has arguments for: debugging log, verbose log, and vulnerabilities log.
The user also has the option to use the --targ flag in order to scan only one IP address remote or local. This is better for testing and ensures that there is no accidental scanning of unowned devices.

An example of a single scan with verbose log enabled would be:

```
    ./scanner.py -v --targ localhost
```

Because OS estimation is just an estimation there are cases in which not enough ports are available to make a good guess. A failure message will be printed and the log file will have an OS fingerprint that can be submitted back to the official nmap page as a diagnostic for the future.