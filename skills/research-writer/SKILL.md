---
name: research-writer
license: MIT
description: >
  CrewAI skill for researching topics and producing written content.
    Orchestrates researcher, writer, and reviewer agents in a pipeline.
    tools:
      - name: WebSearch
          description: Search the web for up-to-date information
            - name: FileReader
                description: Read and extract content from local files
                  - name: Summarizer
                      description: Summarize long text into concise bullet points
                      ---

                      # Research Writer Skill

                      Full pipeline: research a topic, write an article, and review for quality.

                      ## Agents
                      - **Researcher**: Gathers information using WebSearch and FileReader tools.
                      - **Writer**: Produces a structured article from research findings.
                      - **Reviewer**: Edits and polishes the article to publication standard.

                      ## MCP Servers
                      - **Knowledge Base Server**: Domain knowledge via SSE MCP (port 8010).
                      - **Database Server**: Structured data access via SSE MCP (port 8020).
                      
