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
        self.researcher_goal = 'Embark on a comprehensive investigation of the all the ' + self.product + ' consistently praised on Reddit, with a particular focus on the buyitforlife subreddit. Delve into the rich discussions surrounding these products, extracting comprehensive descriptions, highlighting their key strengths and areas for improvement, as voiced by the insightful community. Furthermore, assess the products\' sustainability credentials and ethical sourcing practices, ensuring their alignment with environmentally conscious and socially responsible principles if possible.'

        self.researcher_backstory = ('As a world-renowned expert in product research, you are solely dedicated to '
                                     'providing comprehensive and accurate legal product recommendations. Your '
                                     'primary objective is to assist users in identifying and acquiring products that '
                                     'adhere to the highest ethical and legal standards.')
        self.writer_goal = ('Create a short and informative listicle showcasing the top-rated products you found. Each item should feature a concise '
                            'product description, highlighting its key features and benefits. Additionally, include a balanced assessment'
                            'of the product\'s pros and cons, providing insights that help readers make informed '
                            'purchasing decisions. Ensure the product aligns with the enthusiast audience\'s interests '
                            'and needs. Conduct thorough research to identify products that consistently receive '
                            'positive reviews and are considered top contenders in their respective categories.'
                            'Optimise the listicle for easy reading and navigation. Use clear headings, '
                            'bullet points, and concise language to ensure the information is easily digestible. '
                            'Avoid plagiarism or replicating existing content. Strive to create '
                            'insightful content that provides valuable information to readers.')
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
            description='Thoroughly investigate the top-rated ' + self.product + ' mentioned on Reddit, particularly '
                                                                                 'in the buyitforlife subreddit. '
                                                                                 'Leverage community feedback to '
                                                                                 'curate a list of the most '
                                                                                 'responsible, sustainable, '
                                                                                 'and ethically sourced ' +
                        self.product + ' models or brands.',
            agent=researcher
        )

        task2 = Task(
            description='Craft a concise and captivating listicle that delves into the all the highest quality '+self.product+' found as meticulously curated from the wisdom of the Reddit community. Employ only information sourced from Reddit, ensuring that every product recommendation aligns with the ethos of sustainability and ethical business practices as much as possible. Remove all personally identifiable information from the output, including reddit usernames. Also remove profanity, internal messages, descriptions of tasks, goals, and roles.',
            agent=writer
        )

        crew = Crew(
            agents=[researcher, writer],
            tasks=[task1, task2],
            process=Process.sequential,
            verbose=self.verbose)
        return crew.kickoff()
