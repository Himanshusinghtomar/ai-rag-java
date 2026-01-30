import re

def parse_xml_file(content):
    chunks = []

    patterns = [
        r"<API.*?</API>",
        r"<Processor.*?</Processor>",
        r"<Control.*?</Control>"
    ]

    for pattern in patterns:
        for match in re.finditer(pattern, content, re.DOTALL):
            chunks.append({
                "type": "xml_block",
                "content": match.group(0)
            })

    return chunks
