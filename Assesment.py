def load_lookup_table(lookup_file):
    lookup = {}
    try:
        with open(lookup_file,mode='r',encoding='ascii') as file:
            next(file) # to skip the header
            for row in file :
                row = row.strip()
                if row:
                    try:
                        dstport,protocol,tag = row.split(",")
                        lookup[int(dstport),protocol.lower()] = tag
                    except ValueError as e:
                        print(f"Error: Could not parse the row '{row}'.Please Make sure it has the correct format(dstport,protocol,tag).{e}")
    except FileNotFoundError:
        print(f"Error: The lookup file '{lookup_file}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred while loading the lookup table: {e}")
    return lookup
#to get some protocol names 
def get_protocol_name(protocol_num):
    protocol_map = {
        1: "icmp",
        2: "igmp",
        4: "ipv4",
        6: "tcp",
        9: "igp",
        12: "pup",
        17: "udp",
        18: "mux",
        28: "irtp",
        33: "dccp",
        35: "idpr",
        36: "xtp",
        41: "ipv6",
        45: "idrp",
        46: "rsvp",
        84: "iptm",
        92: "mtp",
        100: "gmtp",
        109: "snp",
        118: "stp",
        121: "smp",
        123: "ptp",
        131: "pipe",
        139: "hip"
    }
    return protocol_map.get(protocol_num, "unknown")
def parse_flow_log(flowlog_file):
    flow_data = []
    try:
        with open (flowlog_file,mode='r',encoding ='ascii') as file:
            for row in file:
                row = row.strip()
                if row:
                    parts = row.split()
                    if(len(parts) < 8):
                        print(f"Warning:Skipping row due to insufficient data:'{row}'")
                        continue
                    try:
                        dstport = parts[6]
                        protocol_num = int(parts[7])
                        protocol = get_protocol_name(protocol_num)
                        flow_data.append((dstport,protocol))
                    except IndexError as e:
                        print(f"Error: Row has missing elements: '{row}'. {e}")
    except FileNotFoundError:
        print(f"Error: The flow log file '{flowlog_file}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred while parsing the flow log: {e}")
    return flow_data

def map_flows_to_tags(flow_data,lookup_):
    try:
        tag_counts = {}
        port_protocol_counts = {}
        for dstport,protocol in flow_data:
            protocol = protocol.lower()
            tag = lookup_.get((int(dstport),protocol),"Untagged")
            tag_counts[tag] = tag_counts.get(tag,0)+1
            port_protocol_counts[(int(dstport),protocol)] = port_protocol_counts.get((int(dstport),protocol),0) +1
    except Exception as e:
        print(f"Error: unexpected error occured while parsing{e}")
    return tag_counts,port_protocol_counts

def write_output(tag_counts,port_protocol_counts,output_file):
    try:
        with open(output_file,mode='w') as file:
            file.write("Tag Counts:\n")
            file.write("Tag,Count\n")
            for tag,count in tag_counts.items():
                file.write(f"{tag},{count}\n")
            file.write("\nPortandProtocol Combination Counts:\n")
            file.write("Port,Protocol,Count\n")
            for (port,protocol),count in port_protocol_counts.items():
                file.write(f"{port},{protocol},{count}\n")
    except IOError as e:
        print(f"Error: Failed to Write to '{output_file}'.{e}")
    except Exception as e:
        print(f"Unexcepted error occured while writing to '{output_file}':" )
def main():
    flowlog_file = 'flow log.txt'
    lookup_file = 'mappings.txt'
    output_file = 'output.txt'
    lookup_ = load_lookup_table(lookup_file)
    flow_data = parse_flow_log(flowlog_file)
    tag_counts,port_protocol_counts = map_flows_to_tags(flow_data,lookup_)
    write_output(tag_counts,port_protocol_counts,output_file)
       
if __name__ == "__main__":
    main()