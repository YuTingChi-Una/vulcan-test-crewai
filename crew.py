"""CrewAI agent, tool, skill, MCP, and model definitions."""
from crewai import Agent, Task, Crew
from crewai.tools import BaseTool
from crewai_tools import MCPServerAdapter

# ===== MCP SERVERS =====
knowledge_base_mcp = MCPServerAdapter(
          server_params={"url": "http://localhost:8010/sse", "transport": "sse"},
)

database_mcp = MCPServerAdapter(
          server_params={"url": "http://localhost:8020/sse", "transport": "sse"},
)

# ===== TOOLS =====
class WebSearchTool(BaseTool):
          name: str = "WebSearch"
          description: str = "Search the web for up-to-date information on any topic."
          def _run(self, query: str) -> str:
                        return f"Search results for: {query}"

      class FileReaderTool(BaseTool):
                name: str = "FileReader"
                description: str = "Read and extract content from local files."
                def _run(self, filepath: str) -> str:
                              return f"Contents of: {filepath}"

            class SummarizerTool(BaseTool):
                      name: str = "Summarizer"
                      description: str = "Summarize long text into concise bullet points."
                      def _run(self, text: str) -> str:
                                    return f"Summary: {text[:200]}"

                  # ===== AGENTS =====
                  researcher = Agent(
                            role="Researcher",
                            goal="Research topics thoroughly and accurately using available tools",
                            backstory="Expert researcher with 10 years of experience in data gathering and analysis.",
                            tools=[WebSearchTool(), FileReaderTool()],
                            llm="gpt-4o",
                            verbose=True,
                  )

writer = Agent(
          role="Writer",
          goal="Write clear and engaging content based on research findings",
          backstory="Skilled content writer who transforms research into compelling narratives.",
          tools=[SummarizerTool(), FileReaderTool()],
          llm="gpt-4o",
          verbose=True,
)

reviewer = Agent(
          role="Reviewer",
          goal="Review and improve content quality to meet publication standards",
          backstory="Experienced editor with high standards for clarity and accuracy.",
          tools=[SummarizerTool()],
          llm="gpt-4o-mini",
          verbose=True,
)

# ===== SKILLS (Crew workflows) =====
def research_and_write_skill(topic: str) -> str:
          """Skill: Full pipeline — research, write, and review content on a given topic."""
          t1 = Task(
              description=f"Research the topic: {topic}. Gather comprehensive information.",
              expected_output="A detailed research report with key findings and sources.",
              agent=researcher,
          )
          t2 = Task(
              description="Write a well-structured article based on the research.",
              expected_output="A 500-word article ready for publication.",
              agent=writer,
          )
          t3 = Task(
              description="Review the article for quality, accuracy, and clarity.",
              expected_output="A polished, publication-ready final article.",
              agent=reviewer,
          )
          crew = Crew(agents=[researcher, writer, reviewer], tasks=[t1, t2, t3])
          return crew.kickoff()
      
