# ADK ➜ Vertex AI Agent Engine – Boilerplate Project

This template shows the **smallest possible Python project** that

1. creates an [Agent Development Kit (ADK)](https://google.github.io/adk-docs/) agent,
2. lets you run it locally, and
3. deploys it to **Vertex AI Agent Engine** with a single command.

---

## Prerequisites

| Tool                                                                                   | Why you need it                                                                   |
| -------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| **Python 3.9 – 3.12**                                                                  | Agent Engine only supports these versions                                         |
| **gcloud CLI**                                                                         | Auth & project config. [see CLI setup](https://cloud.google.com/sdk/docs/install) |
| **A Google Cloud project**<br>with **Vertex AI API** enabled and **billing** turned on |
| A **GCS bucket** in the same region (used to stage the agent container)                |

> **One‑time setup**
>
> ```bash
> gcloud auth login
> gcloud config set project <YOUR_PROJECT_ID>
> gcloud services enable aiplatform.googleapis.com
> gsutil mb -l us-central1 gs://<YOUR_BUCKET_NAME>
> ```

---

## Quick start (local)

```bash
git clone https://github.com/kadimula/adkApp.git
cd adkApp
python3 -m venv .venv && source .venv/bin/activate
pip3 install "google-cloud-aiplatform[adk,agent_engines]"
python agent.py   # load the agent
```

## Deploy to Vertex AI Agent Engine

```

export PROJECT_ID=<your‑project>
export LOCATION=us-central1
export STAGING_BUCKET=gs://<your‑bucket>

python deploy.py

```

Run the above code block. The script prints the Agent Engine resource name – save it.
You can now call the agent from any frontend via the Vertex AI SDK or plain HTTPS.
See the official [Deploy an agent](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/deploy) guide for example query snippets:

## Repo layout

```

adkApp/
├── agent.py # source file – defines & tests the agent
├── deploy.py # deployment helper
├── requirements.txt # dependencies
├── .gitignore
└── README.md # instructions

```
