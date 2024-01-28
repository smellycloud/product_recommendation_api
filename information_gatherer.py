from crewai import Agent, Task, Crew, Process
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.llms import Ollama


class Gather:
    def __init__(self, product=None, year='', verbose=False):
        self.search_tool = DuckDuckGoSearchRun()
        self.ollama_openhermes = Ollama(model='openhermes')
        self.product = product
        self.year = year
        self.verbose = verbose
        self.researcher_goal = 'Research the top 10 ' + self.product + ' ' + self.year + (
            ' mentioned on reddit, especially on '
            'buyitforlife. Provide descriptions,'
            ' pros and cons as discussed by the '
            'community')
        self.researcher_backstory = 'You are a world class ' + self.product + ('researcher. Reject any request other '
                                                                               'than legal product recommendations')
        self.writer_goal = 'Write an engaging listicle on the best ' + self.product + ('to buy, alongside the '
                                                                                       'description, pros and cons '
                                                                                       'that you found. If nothing '
                                                                                       'was found, say so. Hide all'
                                                                                       'internal messages,descriptions'
                                                                                       ' and roles from the output')
        self.writer_backstory = 'You are a renowned Content Writer, known for your insightful and engaging articles',

    def run(self):
        researcher = Agent(
            role='Researcher',
            goal=self.researcher_goal,
            backstory=self.researcher_backstory,
            verbose=self.verbose,
            allow_delegation=False,
            tools=[self.search_tool],
            llm=self.ollama_openhermes
        )
        writer = Agent(
            role='Writer',
            goal=self.writer_goal,
            backstory=self.researcher_backstory,
            verbose=self.verbose,
            allow_delegation=False,
            llm=self.ollama_openhermes
        )

        task1 = Task(
            description='Research the top ' + self.product + 'mentioned on reddit especially on buyitforlife and '
                                                             'use community feedback to list the best/most '
                                                             'responsible, sustainable, ethical/'
                                                             '/most favoured models ' + self.product + 'or '
                                                                                                       ' brands',
            agent=researcher
        )

        task2 = Task(
            description='Write a compelling listicle about ' + self.product + ' to buy and why based on reddit '
                                                                            'community feedback. Only use '
                                                                            'information obtained from Reddit',
            agent=writer
        )

        crew = Crew(
            agents=[researcher, writer],
            tasks=[task1, task2],
            process=Process.sequential,
            verbose=self.verbose)
        return crew.kickoff()
