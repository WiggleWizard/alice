Installing and running Alice
============================

Alice relies on WonderlandX (a CoD4X plugin) to communicate with the CoD4 server, as such you must be running a CoD4X server with WonderlandX installed. To install CoD4X and WonderlandX follow this guide: TBC.

## Prerequisites

Firstly, Alice (along with the whole Project Alice suite) only runs on Linux operating systems. I recommend Debian as it's mostly cutting edge and simple to keep up to date without running into major issues. The follow guide will assume you run a Debian based OS (this includes Ubuntu/Mint).

You will need `git` installed, this will not only come in handy for downloading Alice but also keeping it up to date. If you are on a Debian machine you can execute:

```bash
sudo apt-get install git
```

Alice communicates with WonderlandX through Interprocess Communication protocols (or TCP ,depends on your needs). To reduce the overhead and work load, WonderlandX and Alice use the [ØMQ](http://zeromq.org/) library as its IPC communications backbone. To download and install ØMQ for Alice execute:

```bash
sudo apt-get install python-zmq
```

## Folder structure

Below is the suggested folder structure, of course, you may deviate from this but throughout this guide it assumes this structure.

```
/var/cod4server/
    └─ server
        └─ main
            └─ configs
            └─ logs
        └─ zone
    └─ cod4x
    └─ wonderlandx
    └─ alice
```

## Install

If you have git installed, you can simply clone the Alice repository 