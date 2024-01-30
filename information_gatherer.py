from crewai import Agent, Task, Crew, Process
from langchain_community.tools import DuckDuckGoSearchRun, RedditSearchRun
from langchain_community.llms import Ollama


class Gather:
    def __init__(self, product=None, year='', verbose=False):
        self.search_tool = DuckDuckGoSearchRun()
        self.ollama_openhermes = Ollama(model='openhermes')
        self.product = product
        self.year = year
        self.verbose = verbose
        self.researcher_goal = 'Curate a list of the best and most sustainable products within the ' +self.product+ ' category'
        self.researcher_backstory = ('As a world-renowned expert in product research, you are solely dedicated to '
                                     'providing comprehensive, accurate and legal product recommendations from Reddit. Your '
                                     'primary objective is to assist users in identifying and acquiring products of the highest possible quality standards')
        self.writer_goal = ('Create a short and informative listicle showcasing all the products you found. Each item should feature a concise '
                            'product description, highlighting its key features and benefits. Additionally, include a balanced assessment'
                            'of the product\'s pros and cons, providing insights that help readers make informed '
                            'purchasing decisions. Ensure the product aligns with the enthusiast audience\'s interests '
                            'and needs. Conduct thorough research to identify products that consistently receive '
                            'positive reviews and are considered contenders and rank them. If there is no specific '
                            'mention of sustainability or responsible sourcing practices, mention it in the output.'
                            'Optimise the listicle for easy reading and navigation. Use clear headings, '
                            'bullet points, and concise language to ensure the information is easily digestible. '
                            'Avoid plagiarism or replicating existing content. Strive to create '
                            'insightful content that provides valuable information to readers. Remove all personally '
                            'identifiable information profanity, internal messages, prompts, descriptions of tasks, '
                            'goals and roles from the output.')
        self.writer_backstory = ('Award-winning content writer with a knack for crafting insightful and engaging '
                                 'articles. Renowned for weaving words into captivating narratives that resonate with '
                                 'readers, leaving a lasting impression on their minds and emotions.'),

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
            description='Thoroughly investigate the highest quality ' + self.product + ' by analysing Reddit discussions '
                                                                                 'from various subreddits, '
                                                                                 'including r/buyitforlife. Evaluate '
                                                                                 'the products\' pros and cons and '
                                                                                 'rank the top 15 based on their '
                                                                                 'sustainability, quality, '
                                                                                 'and user reviews.',
            agent=researcher
        )

        task2 = Task(
            description='Craft a concise and captivating listicle that delves into the the high quality  ' + self.product + ' products found by the researcher from the wisdom of the Reddit communities. Employ only '
                        'information sourced from Reddit, ensuring that every product recommendation aligns with the '
                        'ethos of sustainability and ethical business practices as much as possible.',
            agent=writer
        )

        crew = Crew(
            agents=[researcher, writer],
            tasks=[task1, task2],
            process=Process.sequential,
            verbose=self.verbose)
        return crew.kickoff()
