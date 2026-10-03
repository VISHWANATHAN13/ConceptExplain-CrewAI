# ConceptExplain-CrewAI

An AI teaching assistant built on **CrewAI**. Type in any technical topic and a
sequential crew of five agents researches it, breaks it into the subtopics that
actually matter, explains each one at medium depth, draws an ASCII flow diagram
when the topic warrants one, and compiles everything into a single Markdown
document — which the app then exports as a formatted `.docx` you can download.

Frontend is **Gradio**; the LLM is **OpenAI `gpt-4o-mini`** via CrewAI's `LLM`
wrapper.

---

## How it works

The crew runs as a `Process.sequential` pipeline — each task's output becomes
context for the next:

```
[User enters topic in Gradio]
         |
         v
[1. Topic Research Specialist]  --> definition, purpose, real-world use, key terms
         |
         v
[2. Concept Decomposition Specialist]  --> 5 to 7 essential subtopics, ordered
         |
         v
[3. Technical Concept Explainer]  --> explanation + example + takeaway per topic
         |
         v
[4. Technical Diagram Designer]  --> ASCII diagram, or "No diagram required"
         |
         v
[5. Documentation Compiler]  --> one polished Markdown document
         |
         v
[main.py: Markdown --> .docx]  --> outputs/<topic>_<timestamp>.docx
```

| # | Agent | Role | What it produces |
|---|---|---|---|
| 1 | `content_retriever_agent` | Topic Research Specialist | Definition, purpose, real-world relevance, key terms |
| 2 | `subtopic_retriever_agent` | Concept Decomposition Specialist | 5–7 essential subtopics in learning order, each with a one-line justification |
| 3 | `explanation_agent` | Technical Concept Explainer | 4–6 sentence explanation, a concrete example, and a takeaway per topic |
| 4 | `flow_diagram_generator_agent` | Technical Diagram Designer | A fenced ASCII flow diagram (4–8 steps) + legend, **only** for process/pipeline/lifecycle/architecture topics |
| 5 | `final_summarizer_agent` | Documentation Compiler | The complete Markdown body, diagram reproduced character-for-character |

### Design decisions worth knowing

- **Agents and tasks are defined in YAML, not in code.** `agents_configuration.yaml`
  holds role/goal/backstory; `task_configuration.yaml` holds description and
  expected_output. The Python files are thin factories that read the YAML and
  return an `(agent, task)` pair — so prompt tuning never requires touching code.
- **The topic is injected at kickoff, not at build time.** Task descriptions ship
  with a `{user_topic}` placeholder, and `crew.kickoff(inputs={"user_topic": ...})`
  interpolates it into every task. The crew object itself is topic-agnostic.
- **Diagrams are opt-out by design.** Agent 4 is explicitly instructed to skip the
  diagram for purely definitional topics rather than force one, and is told it has
  no image-generation ability so it can't hallucinate a saved file path.
- **ASCII-only diagram constraints exist for the DOCX export.** The task forbids box
  drawing characters, Unicode arrows, curly braces, and tabs — all of which break
  or misalign once the text lands in Word.
- **Whitespace preservation in Word is handled manually.** Word collapses leading and
  repeated spaces by default, so `add_diagram_line()` in [main.py](app/main.py)
  renders each diagram line in Consolas 9pt and sets `xml:space="preserve"` on the
  underlying `w:t` element. Without that, every diagram arrives left-flattened.
- **Corporate TLS is handled up front.** [load_llm.py](app/llm_config/load_llm.py)
  calls `truststore.inject_into_ssl()` so the Windows certificate store is used
  instead of certifi's bundle. Behind a re-signing proxy such as Zscaler, omitting
  this makes every OpenAI call fail as a bare "Connection error".

---

## Project layout

```
ConceptExplain-CrewAI/
├── app/
│   ├── main.py                        Gradio UI + Markdown-to-DOCX export
│   ├── agents/
│   │   ├── agents_configuration.yaml  role / goal / backstory for all 5 agents
│   │   ├── task_configuration.yaml    description / expected_output per task
│   │   ├── agents_config.py           YAML loader
│   │   ├── content_retriever_agent.py
│   │   ├── subtopic_retriever_agent.py
│   │   ├── explanation_agent.py
│   │   ├── flow_diagram_generator_agent.py
│   │   └── final_summarizer_agent.py
│   ├── crew/
│   │   └── create_crew.py             Assembles the sequential Crew
│   └── llm_config/
│       └── load_llm.py                gpt-4o-mini + truststore TLS fix
├── outputs/                           Generated .docx files (topic_timestamp.docx)
├── requirements.txt
└── .env                               OPENAI_API_KEY (not committed)
```

---

## Getting started

### Prerequisites

- Python 3.13 (authored and pinned against 3.13.7)
- An OpenAI API key

### Install

```bash
cd ConceptExplain-CrewAI

python -m venv .conceptexplain
.conceptexplain\Scripts\activate        # macOS/Linux: source .conceptexplain/bin/activate

pip install -r requirements.txt
```

> **Note on `requirements.txt`** — it is a full `pip freeze` written by Windows
> PowerShell, so it is UTF-16 encoded. If `pip install -r` fails to parse it,
> re-save it as UTF-8 first:
> ```powershell
> Get-Content requirements.txt | Set-Content -Encoding utf8 requirements-utf8.txt
> pip install -r requirements-utf8.txt
> ```

### Configure

Create `.env` in the project root:

```
OPENAI_API_KEY=sk-...
```

### Run

Launch from **inside `app/`** — the modules import as top-level packages
(`from crew.create_crew import ...`), so `app/` must be the working directory:

```bash
cd app
python main.py
```

Gradio prints a local URL (default `http://127.0.0.1:7860`). Enter a topic, click
**Generate Learning Content**, and you'll get the rendered Markdown in the browser
plus a downloadable `.docx` saved to `outputs/`.

---

## Example

Input: `Retrieval Augmented Generation`

Output: `outputs/Retrieval augmented generation_20261002_215619.docx` — a titled
document with research sections, 5–7 ordered subtopics, medium-depth explanations,
and a preserved ASCII pipeline diagram (RAG is a pipeline topic, so agent 4 draws one).

A purely definitional topic such as `Polymorphism` will correctly produce no
diagram at all, with no mention of its absence in the document.

---

## Tech stack

| Layer | Choice |
|---|---|
| Agent orchestration | CrewAI 1.15.23 (`Crew`, `Agent`, `Task`, `Process.sequential`) |
| LLM | OpenAI `gpt-4o-mini` via `crewai.LLM` |
| UI | Gradio 6.29 (`gr.Blocks`) |
| Document export | `python-docx` 1.2.0 |
| Config | PyYAML, `python-dotenv` |
| TLS | `truststore` (Windows cert store injection) |

---

## Customising

- **Change depth or tone** — edit `expected_output` and the rules in
  `app/agents/task_configuration.yaml`. No Python changes needed.
- **Change subtopic count** — the "maximum of 5 to 7 subtopics" rule lives in
  `subtopic_identification_task`.
- **Change the model** — single line in `app/llm_config/load_llm.py`.
- **Add an agent** — add its block to both YAML files, write a factory following the
  existing `create_*_agent()` pattern, then register the returned agent and task in
  `app/crew/create_crew.py`.

---


