# Link Extractor

This is a simple tool to extract all the links in records from a Geonetwork and retrieve domain name.

## Usage
    
```bash
python main.py -t my_template -g gn_url -wr
```

## Options

- `-g` or `--gn-url'`: Geonetwork URL. Mandatory
- `-t` or `--template`: Template name to use.
- `-wr` or `--write-respense`: Saves the json body response from ES into `body_response.json` file. Use for debugging purposes.

