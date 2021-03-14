import re

# Solution to: Q-66620236 on Stackoverflow
# filepath = "input.txt"

def make_dummy_data(filepath: str):
    
    s = """
    a0b1:ff33:acd5 ghwvauguvwi ybvakvi
    klasilvavh; 11b9:33df:55f6
    haliviv
    a4d1:e733:ff55
    66a1:b2f3:b9c5
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
    pattern = r"(\w{4}:\w{4}:\w{4})"
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
    #
    # ['a0-b1-ff-33-ac-d5',
    #  '11-b9-33-df-55-f6',
    #  'a4-d1-e7-33-ff-55',
    #  '66-a1-b2-f3-b9-c5']
