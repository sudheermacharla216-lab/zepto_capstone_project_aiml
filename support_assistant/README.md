# Support assistant

Install the consolidated requirements from the repository root. Default mock mode needs no LLM-provider key. Run `MOCK_LLM=1 uvicorn main:app --app-dir support_assistant --host 0.0.0.0 --port 7860` from the root. Send `POST http://127.0.0.1:7860/ask` with `{"query":"What is the refund policy?"}`.

## Architecture
Ingestion: eight docs/doc_*.txt files contain the assignment corpus; main.py resources() uses each document as one chunk. Embedding: resources() runs local all-MiniLM-L6-v2 and upserts vectors into the persistent Chroma zepto_policies collection using cosine distance. Retrieval: the LangGraph classify_intent node routes keyword matches to retrieve_and_answer, which embeds the query and requests the top three chunks. Generation: retrieve_and_answer returns a deterministic excerpt from the top chunk in mock mode, or uses the structured PROMPT in optional real mode. direct_answer handles the other route. FastAPI /ask invokes the graph and validates the answer/sources/confidence response with Pydantic.

MOCK_LLM defaults to 1. Classification uses the specified keyword heuristic and both answer nodes use canned outputs. Embedding and retrieval always run for real. With MOCK_LLM=0, classification and generation use llm_call; generation validates JSON and retries twice before returning a marked error. Classification also retries and falls back to the keyword heuristic if unsuccessful. Optional endpoint variables are LLM_CHAT_URL, LLM_API_KEY and LLM_MODEL; use a genuinely free provider if you choose this extension. No paid service is needed for the baseline. Never commit keys.

The first installation/model download requires internet; afterward a cached or locally saved embedding model supports offline mock queries. Mock confidence=1.0 is a deterministic rubric value, not a calibrated probability. Mock sources list all retrieved IDs although the answer excerpts only the top document. These are assignment policies, not verified current Zepto policies.

## Local Docker verification — run outside standard Colab
From the repository root:
```sh
docker build -t zepto-support support_assistant
docker run --rm -p 7860:7860 -e MOCK_LLM=1 zepto-support
```
In a second terminal:
```sh
curl -X POST http://localhost:7860/ask -H "Content-Type: application/json" -d '{"query":"What is the refund policy?"}'
curl -X POST http://localhost:7860/ask -H "Content-Type: application/json" -d '{"query":"What is two plus two?"}'
```
The image downloads the embedding model at build time, then loads it locally. Building requires internet and enough disk for PyTorch and the model. Record your actual Docker verification below; the notebook does not claim to have built the image.

Dockerfile and Docker execution commands are included for reproducible deployment. The FastAPI application itself was verified with MOCK_LLM=1 using local HTTP POST requests. Docker image build/run should additionally be verified on a Docker-capable machine before final submission.

## Actual HTTP transcripts (MOCK_LLM=1)

```json
[
  {
    "request": {
      "query": "What is the refund policy for damaged grocery items?"
    },
    "status": 200,
    "response": {
      "answer": "Based on the retrieved context: Returns & Refunds\nGrocery and perishable items may be reported for a return within 24 hours of delivery if damaged, spoiled, or incorrect; non-perishable packaged items may be returned within 7 days o",
      "sources": [
        "doc_02",
        "doc_06",
        "doc_05"
      ],
      "confidence": 1.0
    }
  },
  {
    "request": {
      "query": "What is two plus two?"
    },
    "status": 200,
    "response": {
      "answer": "I can only answer questions about Zepto policies right now.",
      "sources": [],
      "confidence": 1.0
    }
  }
]
```
