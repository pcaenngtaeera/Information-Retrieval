# Assignment 1: Indexing

## About

Our project focuses on indexing a collection and searching the collection using the index.
We have implemented an inverted index to store term occurence information.
The program consists of two scripts: `index.py` and `search.py`

## Requirements

You will need:

  - access to one of RMIT's core teaching servers `@(titan|saturn|jupiter).csit.rmit.edu.au`
  - an installation of Python 2.7.4 on the core teaching server
  - to be able to SSH and SCP with the core teaching server using your PC
  
      * [Windows] PuTTY & WinSCP
      * [macOS] Terminal
      * [Linux] Bash

  - a copy of our scripts on your PC

      * index.py
      * search.py

## Instructions

1)  Move `index.py` and `search.py` to the server

1a) [Windows]

    Run `WinSCP` and enter the server, username and password when prompted:

    ```
    Host Name (or IP address): [server] (e.g. jupiter.csit.rmit.edu.au)
    Port: 22
    ```
    
    Finally, drag `index.py` and `search.py` to the server

1b) [macOS|Linux]

    Run `Terminal|Bash` with `scp [source] [user]@[server]:[destination]`

    ```
    e.g.  scp ./* s3538463@jupiter.csit.rmit.edu.au:/home/sh3/S3538463/IR/assignment1
    ```

2)  Connect to the core teaching server

2a) [Windows]

    Run `PuTTY` and SSH to the server (see `WinSCP` instructions)
    
2b) [macOS/Linux]

    Run `Terminal/Bash` and enter `ssh [user]@(titan|saturn|jupiter).csit.rmit.edu.au`
    
    ```
    e.g.  ssh s3538463@jupiter.csit.rmit.edu.au 
    ```

3)  Relocate to the script's directory using `cd [script_directory]`

    ```
    e.g. cd /home/sh3/S3538463/IR/assignment1
    ```         
    
4)  Execute `index.py` by using `python index.py -s /home/inforet/a1/stoplist -p /home/inforet/a1/latimes > print`

    * `-s [stoplist]` and '-p' are optional arguments
    * assume `stoplist` and `latimes` are in the given locations
    * '> print' is optional, it will redirect `stdout` to a file named `print` when '-p' is active
    * files `map`, `lexicon`, and `invlists` will be created in the same directory

5)  Execute `search.py` by using `python search.py lexicon invlists map <queryterm> [<queryterm> ...] > result`

    * `index.py` must be executed at least once to generate `map`, `lexicon`, and `invlists` 
    * `<queryterm> [<queryterm> ...]` indicates `n` space-separated queryterms where n >= 1
    * a query that doesn't exist within the lexicon will result in no output
    * '> result' is optional, it will redirect `stdout` to a file named `result`
      
## Contributions

The script is developed by Christopher Nguyen (3595629). 
WeiWei Wen (3538463) conducted rigorous testing on the core teaching servers.
The `Report.pdf` and `README.txt` is written by both Chris and WeiWei.
