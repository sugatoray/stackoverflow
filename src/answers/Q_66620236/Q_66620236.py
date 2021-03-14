import re

# Solution to: Q-66620236 on Stackoverflow
# filepath = "input.txt"

def make_dummy_data(filepath: str):
    
    s = """
    0011:2233:4455 ghwvauguvwi ybvakvi
    klasilvavh; 1122:3344:5566
    haliviv
    4411:7733:6655
    6611:2233:9955
    """

    # Create dummy data file
    with open(filepath, "w") as f:
        f.write(s)

    print(f"Created file: {filepath}")

def read_file(filepath: str):
    """Reads and returns the content of a file."""

    with open(filepath, "r") as f:
        content = f.read() # read in one attemp
    return content

def format_mac_id(mac_id: str):
    """Returns a formatted mac_id.
    INPUT FORMAT: "xxxxxxxxxxxx"
    OUTPUT FORMAT: "xx-xx-xx-xx-xx-xx"
    """
    
    mac_id = list(mac_id)
    mac_id = ''.join([ f"-{v}" if (i % 2 == 0) else v for i, v in enumerate(mac_id)])[1:]
    return mac_id

def extract_mac_ids(content: str, format: bool=True):
    """Extracts and returns a list of formatted mac_ids after.
    INPUT FORMAT: "xxxx:xxxx:xxxx"
    OUTPUT FORMAT: "xx-xx-xx-xx-xx-xx"
    """
    
    # import re
    pattern = r"(\d{4}:\d{4}:\d{4})"
    pat = re.compile(pattern)
    mac_ids = pat.findall(content) # returns a list of all mac-ids
    # Replaces the ":" with "" and then formats 
    # each mac-id as: "xx-xx-xx-xx-xx-xx"
    if format:
        mac_ids = [format_mac_id(mac_id.replace(":", "")) for mac_id in mac_ids]
    return mac_ids


if __name__ == "__Main__":

    filepath = "input.txt"
    use_dummy_data = True

    if use_dummy_data:
        make_dummy_data(filepath)
    
    content = read_file(filepath)
    mac_ids = extract_mac_ids(content, format=True)

    print(mac_ids)

    ## Output: for Dummy Data
    # ['00-11-22-33-44-55',
    #  '11-22-33-44-55-66',
    #  '44-11-77-33-66-55',
    #  '66-11-22-33-99-55']
