# Java Codebase RAG System

A production-ready Retrieval-Augmented Generation (RAG) system designed for large Java microservice architectures. Query your codebase in natural language and get context-aware answers using local LLMs.

## 🎯 Overview

This system provides intelligent code assistance by indexing your Java microservices and enabling natural language queries. Unlike fine-tuning approaches, RAG keeps your model up-to-date with live code changes while remaining cost-effective and easy to maintain.

## ✨ Key Features

- **🔍 AST-Based Parsing**: Intelligent Java code parsing using abstract syntax trees
- **📦 Method-Level Chunking**: Semantic chunking at method granularity for precise retrieval
- **🔗 Dependency-Aware**: Understands relationships across services and modules
- **💰 Cost-Effective**: Zero fine-tuning required, runs entirely locally
- **🤖 Local LLM Support**: Powered by Ollama (Qwen2.5-Coder 7B)
- **🌐 MCP Integration**: Model Context Protocol server for tool integration
- **⚡ Hybrid Search**: Combines keyword matching with vector similarity

## 🏗️ Architecture

```
Java Codebase
    ↓
Ingestion (AST Parsing)
    ↓
Chunking (Methods/XML Blocks)
    ↓
Embeddings (Nomic-Embed-Text)
    ↓
Vector Store (FAISS)
    ↓
Query Engine (Hybrid Search)
    ↓
LLM Generation (Qwen2.5-Coder)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Ollama installed and running
- Java codebase(s) to index

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd java-codebase-rag
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Install Ollama models**
```bash
ollama pull qwen2.5-coder:7b
ollama pull nomic-embed-text
```

4. **Configure your codebases**

Edit `config/paths.json`:
```json
{
  "codebases": {
    "core_lib": "/path/to/your/core-library",
    "service": "/path/to/your/microservice"
  }
}
```

### Usage

1. **Ingest your codebase**
```bash
python3 -m ingest.codebase_ingest
```

2. **Build the vector index**
```bash
python3 -m vectorstore.build_index
```

3. **Query your codebase**
```python
from query.generate import ask

answer = ask("How does the payment processing flow work?")
print(answer)
```

## 🔧 Configuration

### Settings (`config/settings.yaml`)

```yaml
project:
  language: java
  architecture: layered
  patterns:
    - spring
    - orchestration_xml

chunking:
  strategy: method
  max_lines: 80

indexing:
  include_tests: false
  include_configs: true
  supported_extensions:
    - .java
    - .xml
    - .yaml
    - .yml

retrieval:
  top_k: 3
```

### Supported File Types

- **Java files** (`.java`): Method-level extraction using javalang
- **XML files** (`.xml`): Pattern-based extraction for API/Processor/Control blocks
- **YAML files** (`.yaml`, `.yml`): Configuration file indexing

## 🛠️ MCP Server Integration

The system includes an MCP (Model Context Protocol) server for integration with AI assistants.

### Running the MCP Server

**STDIO Mode** (for Claude Desktop, etc.):
```bash
python3 -m mcp.stdio_server
```

**HTTP Mode** (REST API):
```bash
uvicorn mcp.server:app --host 0.0.0.0 --port 8000
```

### Available Tools

- `ask_codebase`: Query the indexed codebase with natural language

### Example MCP Configuration (Claude Desktop)

Add to your Claude Desktop config:
```json
{
  "mcpServers": {
    "java-rag": {
      "command": "python3",
      "args": ["-m", "mcp.stdio_server"],
      "cwd": "/path/to/java-codebase-rag"
    }
  }
}
```

## 📊 Use Cases

### 1. Code Navigation
**Query**: "Where is the user authentication logic implemented?"

**Response**: References specific files and methods handling authentication

### 2. Bug Root Cause Analysis
**Query**: "What could cause NullPointerException in the payment flow?"

**Response**: Identifies potential null reference points with file paths

### 3. Dependency Tracing
**Query**: "Which services depend on the UserService?"

**Response**: Lists all services importing or calling UserService

### 4. Configuration Understanding
**Query**: "What database connection pools are configured?"

**Response**: Extracts and explains database configuration from XML/YAML

### 5. Architecture Overview
**Query**: "Explain the orchestration flow for account creation"

**Response**: Walks through the XML orchestration steps with context

## 🎯 Why RAG Over Fine-Tuning?

| Aspect | RAG | Fine-Tuning |
|--------|-----|-------------|
| **Cost** | Low (local inference) | High (GPU training) |
| **Updates** | Instant (re-index) | Expensive (retrain) |
| **Accuracy** | High (exact retrieval) | Variable (generalization) |
| **Maintenance** | Simple | Complex |
| **Context** | Project-specific | General + biased |

## 📁 Project Structure

```
java-codebase-rag/
├── config/
│   ├── paths.json          # Codebase paths
│   └── settings.yaml       # System configuration
├── ingest/
│   ├── codebase_ingest.py  # Main ingestion pipeline
│   ├── java_parser.py      # Java AST parsing
│   └── xml_parser.py       # XML pattern extraction
├── vectorstore/
│   ├── faiss_store.py      # FAISS vector operations
│   ├── embedder.py         # Ollama embedding client
│   └── build_index.py      # Index building script
├── query/
│   ├── generate.py         # LLM generation
│   ├── search.py           # Hybrid search logic
│   └── prompt_loader.py    # Prompt template loader
├── mcp/
│   ├── server.py           # FastAPI MCP server
│   ├── stdio_server.py     # STDIO MCP server
│   ├── tools.py            # MCP tool implementations
│   └── schemas.py          # Tool schemas
├── prompts/
│   ├── system.txt          # System prompt
│   ├── java.txt            # Java conventions
│   ├── orchestration.txt   # Architecture notes
│   └── response.txt        # Response formatting
└── index/
    └── code_chunks.json    # Indexed chunks
```

## 🔍 How It Works

### 1. Ingestion Phase
- Scans configured codebase directories
- Parses Java files using AST (Abstract Syntax Tree)
- Extracts methods with context (up to 80 lines)
- Parses XML orchestration files using regex patterns
- Stores structured chunks with metadata

### 2. Indexing Phase
- Generates embeddings using `nomic-embed-text` via Ollama
- Builds FAISS vector index for similarity search
- Stores metadata alongside vectors

### 3. Query Phase
- Performs hybrid search:
  - **Keyword matching**: Fast filtering based on terms
  - **Vector similarity**: Semantic understanding
- Retrieves top-k relevant code chunks
- Constructs context-aware prompt
- Generates answer using `qwen2.5-coder:7b`

## 🎨 Customization

### Adding New Parsers

Create a new parser in `ingest/`:

```python
# ingest/kotlin_parser.py
def parse_kotlin_file(content):
    chunks = []
    # Your parsing logic
    return chunks
```

Update `codebase_ingest.py` to use it.

### Custom Prompts

Edit files in `prompts/` to customize:
- System behavior (`system.txt`)
- Language-specific rules (`java.txt`)
- Response formatting (`response.txt`)

### Search Tuning

Modify `query/search.py`:
- Adjust `top_k` for more/fewer results
- Tune keyword matching thresholds
- Customize context formatting

## 🐛 Troubleshooting

### Ollama Connection Issues
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama
ollama serve
```

### Empty Search Results
- Verify index was built: `ls vectorstore/codebase.index`
- Check chunks were created: `cat index/code_chunks.json`
- Increase `top_k` in search parameters

### MCP Server Not Responding
- Check logs: `tail -f /tmp/mcp_stdio_server.log`
- Verify Ollama models are pulled
- Ensure Python environment is activated

## 📝 Example Queries

```python
from query.generate import ask

# Architecture questions
ask("What design patterns are used in this codebase?")

# Implementation details
ask("How is caching implemented in the UserService?")

# Debugging
ask("Where might memory leaks occur in the data processing pipeline?")

# Configuration
ask("What are the retry policies for external API calls?")
```

## 🔐 Security Notes

- All processing happens locally
- No data sent to external APIs
- Configure `.gitignore` to exclude indexes from version control
- Sensitive codebases remain on your infrastructure

## 📈 Performance

- **Indexing**: ~100 files/second (depends on codebase size)
- **Search**: <100ms for typical queries
- **Generation**: 2-5 seconds (7B model on CPU)
- **Memory**: ~2GB for moderate codebases

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional language parsers (Kotlin, Scala, etc.)
- Enhanced search algorithms
- Multi-repo dependency graphs
- Web UI for queries

## 📄 License

[Add your license here]

## 🙏 Acknowledgments

- Powered by [Ollama](https://ollama.ai/)
- Vector search via [FAISS](https://github.com/facebookresearch/faiss)
- Java parsing using [javalang](https://github.com/c2nes/javalang)
- MCP protocol support
