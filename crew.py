from crewai import Agent, Task, Crew

researcher = Agent(
      role="Researcher",
      goal="Research topics thoroughly and accurately",
      backstory="An expert researcher with years of experience in data gathering.",
)

writer = Agent(
      role="Writer",
      goal="Write clear and engaging content",
      backstory="A skilled writer who turns research into compelling narratives.",
)

research_task = Task(
      description="Research the latest trends in AI agents",
      expected_output="A detailed report on AI agent trends",
      agent=researcher,
)

write_task = Task(
      description="Write a blog post based on the research",
      expected_output="A 500-word blog post",
      agent=writer,
)

crew = Crew(
      agents=[researcher, writer],
      tasks=[research_task, write_task],
)

if __name__ == "__main__":
      result = crew.kickoff()
      print(result)
  
