# Agent Project

This project leverages the Google ADK (Agent Development Kit) to build and deploy intelligent agents.



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