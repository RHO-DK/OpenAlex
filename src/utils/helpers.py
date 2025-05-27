import logging


#parsing

#præfix-håndtering

def strip_id(input_string):
    if not isinstance(input_string, str):
        logging.debug(f"strip_id: Modtog ikke-streng ({type(input_string)}): {input_string}")
        return input_string

    # DOI afviger fra det generelle mønster i input_strings:
    if input_string.startswith("https://doi.org/"):
        return input_string.replace("https://doi.org/", "")
    
    # Andre præfixer matcher dette strip af sidste element:
    if "/" in input_string:
        return input_string.rsplit("/", 1)[-1]

    return input_string


