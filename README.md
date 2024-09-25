# Flow-Log-Parser
This program processes flow logs, maps each row to a tag based on a lookup table, and generates a summary of tag counts and port/protocol combinations.
**ASSUMPTIONS:**
 1.**Flow Log Format**
     a. The Flow logs follow AWS Version 2 Format
     b. Each line the flow log contains the following fields in the same order
         version, account-id, interface-id, srcaddr, dstaddr, srcport, dstport, protocol, packets,           bytes, start, end, action, log-status.
     c.Only dstport(Destination Port) and protocol are used for tag mapping
 2. Lookup Table:
     a. The lookup table is text file with three columns
 3. Supprted Protocols:
     a. The program recognizes 24 predefined protocols based on their protocol numbers.
     b. Any flow log with an unsupported protocol will be marked as "Unknown."
 4.Flow Data Parsing:
    a. Only rows with valid protocol numbers and destination ports are processed.
    b. If a row contains an unknown protocol or has missing fields, it will be skipped, and a 
       warning message will be shown.
 5.Output:
     results are written into a file named output.txt
**Usage**
**Input Files:**
   a.The input files must be named flow log.txt for the flow data and mappings.txt for the     lookup table.
   b.If other filenames are used, the program will throw an error. 
 RUNNING THE PROGRAM
 python assesment.py
**Limitations:**

The program only supports the predefined list of protocols.
It does not handle protocols outside this list.

   
