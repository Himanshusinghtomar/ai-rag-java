import javalang

def parse_java_file(content):
    chunks = []

    try:
        tree = javalang.parse.parse(content)
        lines = content.splitlines()

        for _, node in tree.filter(javalang.tree.MethodDeclaration):
            if not node.position:
                continue

            start = node.position.line - 1
            chunk = "\n".join(lines[start:start + 80])

            chunks.append({
                "type": "java_method",
                "name": node.name,
                "content": chunk
            })

    except Exception:
        pass

    return chunks
