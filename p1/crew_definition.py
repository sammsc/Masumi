from crewai import Agent, Task, Crew, Process





######################################################
# CERTIFY ############################################
######################################################

class CertificateCrew:
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.crew = self.create_crew()

    def create_crew(self):
        certifier = Agent(
            role='Code/Metadata Certifier',
            goal='Classify agentic code/metadata as trusted, fraudulent, or uncertain',
            backstory='Experienced in code analysis and classification. You are working at a company who builds trustworthiness by doing evaluation and classification of different inputs',
            #system_template=template_certify,
            #prompt_template="{input_data}",
            verbose=self.verbose
        )

        crew = Crew(
            agents=[certifier],
            tasks=[Task(
                description='Classify code: {input_data}',
                expected_output='only output: TRUE/FALSE/ONHOLD based on your evaluation. TRUE = trusted,FALSE=fraudulent,ONHOLD=uncertain',
                agent=certifier
            )],
            #process=Process.parallel
        )
        return crew

    def certify(self, code: str, metadata: dict):
        result = self.crew.kickoff(input_data=code)
        return result


#####################################
# SURVEIL ###########################
#####################################

class SurveillanceCrew:
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.crew = self.create_crew()

    def create_crew(self):
        # Create the agent for surveillance
        researcher = Agent(
            role='Surveillance Agent',
            goal='Analyze transaction metadata for agentic service validation',
            backstory='Expert in validating marketplace transactions',
            verbose=self.verbose
        )

        # Initialize the crew with the surveillance task
        crew = Crew(
            agents=[researcher],
            tasks=[Task(
                description='Analyze transaction data for service validity.{input_data}',
                expected_output='only output: TRUE/FALSE/ONHOLD based on criteria validation.',
                agent=researcher
            )]
        )
        return crew

    def surveil(self, input_data: str):
        """
        This method processes the input data and applies the criteria validation.
        """
        try:
            task_output = self.crew.kickoff(input_data=input_data)
            return task_output.strip()
        except Exception as e:
            return f"Error: {str(e)}"



class InvestigateCrew:
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.crew = self.create_crew()

    def create_crew(self):
        investigator = Agent(
            role='Investigator',
            goal='based on different internal/external data, you investigate this case',
            backstory='Experienced in investigation. You are a private investigator getting information as input and then provide a suggestion as output',
      
            verbose=self.verbose
        )

        crew = Crew(
            agents=[investigator],
            tasks=[Task(
                description='investigation case and information: {input_data}',
                expected_output='output 3 key insights of the investigation case. Output your Suggestion and recommendation if the case can be solved wiht your case outputs(output TRUE,False,more_investigation)',
                agent=investigator
            )],
            
        )
        return crew

    def certify(self, code: str, metadata: dict):
        result = self.crew.kickoff(input_data=code)
        return result


















class ResearchCrew:
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.crew = self.create_crew()

    def create_crew(self):
        researcher = Agent(
            role='Research Analyst',
            goal='Find and analyze key information',
            backstory='Expert at extracting information',
            verbose=self.verbose
        )

        writer = Agent(
            role='Content Summarizer',
            goal='Create clear summaries from research',
            backstory='Skilled at transforming complex information',
            verbose=self.verbose
        )

        crew = Crew(
            agents=[researcher, writer],
            tasks=[
                Task(
                    description='Research: {input_data}',
                    expected_output='Detailed research findings about the topic',
                    agent=researcher
                ),
                Task(
                    description='Write summary',
                    expected_output='Clear and concise summary of the research findings',
                    agent=writer
                )
            ]
        )
        return crew