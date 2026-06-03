from crewai import Agent, Task, Crew
from crewai.tools import BaseTool
from langchain_openai import ChatOpenAI

# ===== AGENT =====
researcher = Agent(
      role="Researcher",
      goal="Research topics thoroughly and accurately",
      backstory="Expert researcher with years of experience in data gathering.",
)
writer = Agent(
      role="Writer",
      goal="Write clear and engaging content",
      backstory="Skilled writer who turns research into compelling narratives.",
)
reviewer = Agent(
      role="Reviewer",
      goal="Review and improve content quality",
      backstory="Experienced editor with high standards.",
)

# ===== TOOL =====
class WebSearchTool(BaseTool):
      name: str = "WebSearch"
      description: str = "Search the web for up-to-date information on any topic."
      def _run(self, query: str) -> str:
                return f"Search results for: {query}"

  class FileReaderTool(BaseTool):
        name: str = "FileReader"
        description: str = "Read and extract content from local files."
        def _run(self, filepath: str) -> str:
                  return f"Contents of {filepath}"

    class APICallerTool(BaseTool):
          name: str = "APICaller"
          description: str = "Make HTTP requests to external APIs."
          def _run(self, url: str) -> str:
                    return f"Response from {url}"

      # ===== SKILL =====
      def research_and_write_skill(topic: str):
            """Skill: Full pipeline — research, write, and review content."""
            t1 = Task(description=f"Research {topic}", expected_output="Research report", agent=researcher)
            t2 = Task(description="Write article from research", expected_output="Draft article", agent=writer)
    t3 = Task(description="Review and improve the article", expected_output="Final article", agent=reviewer)
    crew = Crew(agents=[researcher, writer, reviewer], tasks=[t1, t2, t3])
    return crew.kickoff()

def quick_summary_skill(topic: str):
      """Skill: Quick research and summarization."""
      t1 = Task(description=f"Summarize key facts about {topic}", expected_output="Bullet points", agent=researcher)
      crew = Crew(agents=[researcher], tasks=[t1])
      return crew.kickoff()

# ===== MCP SERVER =====
MCP_SERVER_CONFIG = {
      "name": "CrewAI MCP Server",
      "version": "1.0.0",
      "transport": "stdio",
      "tools": ["WebSearch", "FileReader", "APICaller"],
}

# ===== AI MODEL =====
gpt4o_llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
gpt4o_mini_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

gpt4o_researcher = Agent(
      role="GPT-4o Researcher",
      goal="Use advanced AI to research complex topics",
      backstory="Powered by GPT-4o for deep analysis.",
      llm=gpt4o_llm,
)

# ===== OTHER =====
class ReportFormatter:
      """Utility for formatting crew outputs into structured reports."""

    def to_markdown(self, content: str) -> str:
              return f"# Report\n\n{content}"

    def to_json(self, content: str) -> dict:
              return {"report": content, "word_count": len(content.split())}
      
