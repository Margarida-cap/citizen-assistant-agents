# Citizen Assistant

This project leverages the Google ADK (Agent Development Kit) to build and deploy an AI-powered Citizen Assistant System for Public Service Navigation.

**Problem Description**:
Navigating public administration is often overwhelming for citizens due to disjointed websites, vague terminology, and redundant paperwork. This results in frustration, delayed access to critical services, and a higher load on public support centers. This use case introduces an agentic AI system that understands citizen queries, searches across government sites, recommends the right service or form, and assists with form completion using contextual data. It acts as a digital front door for citizen-government interaction—improving access, clarity, and administrative efficiency.

**Parameters**:

- Accept natural language queries (e.g., 'renew passport' or 'get birth certificate').
- Search across government portals using federated search or scraping.
- Recommend the most relevant service or form based on task intent and metadata.
- Auto-fill forms using historical data and contextual inference (with consent).
- Support digital identity login and secure data storage.
- Track task status, due dates, and send follow-up reminders.
- Explain complex administrative steps in plain language.
- Ensure data protection compliance.
- Provide multilingual and accessible UX.
- Measure success via task completion rate, user satisfaction, and form accuracy.

**Client/ Sponsor**:
GenCAT CTTI

**SME**:
Xavier Porcel-Blanes


## Setup Instructions

1. **Clone the Repository**
    ```bash
    git clone https://github.com/your-org/your-agent-project.git
    cd agent-hackathon
    ```

2. **Create a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

<!-- 3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ``` -->

3. **Install Google ADK**
    ```bash
    pip install google-adk
    ```
4. **Install GCP CLI**
    - Available in company portal (Google SDK)

5. **Authenticate with Gcloud**
    In the IDE console, do:
    ```bash
    gcloud init
    gcloud auth application-default login
    ```

6. **Run**
    ```bash
    adk web
    ```

## Resources
- [ADK Quickstart](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit/quickstart)
- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [Credentials](https://developers.google.com/workspace/guides/create-credentials)
- [Default Credentials](https://cloud.google.com/docs/authentication/application-default-credentials)


## License

This project is licensed under the MIT License.
