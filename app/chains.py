import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()


class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.3-70b-versatile"
        )

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### ROLE: 
            You are an expert Data Extraction Specialist focused on recruitment and job market analysis. 
            Your task is to parse raw HTML/Text content and extract specific job opportunities.

            ### CONTEXT:
            The following text is scraped from a company's career page. It may contain noise (headers, ads, footers). 
            Identify if there is a specific job posting and extract the details.

            ### INPUT DATA:
            <scraped_content>
            {page_data}
            </scraped_content>

            ### EXTRACTION RULES:
            1. If multiple jobs are found, return them as a list of JSON objects.
            2. If no job posting is found, return an empty list: [].
            3. Ensure the 'description' field is a concise summary of the role (max 3 sentences) to save downstream tokens.
            4. Clean all special characters from the 'skills' list.

            ### OUTPUT FORMAT:
            Return ONLY valid JSON. No preamble, no explanations.
            Schema:
            {{
                "jobs": [
                    {{
                        "role": "Job title",
                        "experience": "Years of experience required or seniority level",
                        "skills": ["skill1", "skill2"],
                        "description": "Short overview"
                    }}
                ]
            }}

            ### JSON OUTPUT:
            """
        )
        chain_extract = prompt_extract | self.llm
        result = chain_extract.invoke({"page_data": cleaned_text})
        
        json_parser = JsonOutputParser()
        json_result = json_parser.parse(result.content)
        return json_result.get('jobs', [])

    def write_mail(self, job, links):
        prompt_email = PromptTemplate.from_template(
            """
            ### ROLE:
            You are Mustafa, a Senior Business Development Executive at **Synthetix AI**. 
            Synthetix AI is a boutique AI Engineering firm specializing in LLM Orchestration, 
            Agentic Workflows, and Enterprise-grade Automation.

            ### INPUT DATA:
            JOB DESCRIPTION: 
            {job_description}

            PORTFOLIO LINKS: 
            {link_list}

            ### TASK:
            Write a high-converting, personalized cold email to the hiring manager/client. 
            Your goal is to demonstrate how Synthetix AI can solve the specific challenges mentioned in the job description.

            ### STRATEGY (The "Problem-Solution-Proof" Framework):
            1. **The Hook:** Start with a brief observation about their specific needs (from the job description).
            2. **The Value:** Position Synthetix AI as a partner that has solved similar problems using AI & Automation.
            3. **The Proof:** Select ONLY the top 2 most relevant links from the provided Portfolio Links that match the job's tech stack or goals.
            4. **The CTA:** A low-friction call to action (e.g., a 10-minute brainstorming call).

            ### CONSTRAINTS:
            - Persona: Professional, tech-savvy, helpful, and concise.
            - Avoid buzzwords like "revolutionary" or "game-changing".
            - Maximum length: 150 words.
            - No preamble (Don't say "Sure, here is the email").
            - Signature: Mustafa | Business Development, Synthetix AI.

            ### EMAIL OUTPUT:
            """
        )
        chain_email = prompt_email | self.llm
        result = chain_email.invoke({"job_description": str(job), "link_list": links})
        return result.content
