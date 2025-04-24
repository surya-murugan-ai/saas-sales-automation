import requests
from app.config import settings

class LLMService:
    def __init__(self):
        self.endpoint = settings.LLM_ENDPOINT  # e.g., http://localhost:11434
        self.model = settings.LLM_MODEL or "llama3.2"  # Default model name if not set

    def generate(self, prompt: str, max_tokens: int = 300):
        response = requests.post(
            f"{self.endpoint}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": max_tokens
                }
            }
        )
        response.raise_for_status()
        return response.json()["response"]

    def generate_profile(self, lead: dict, company_data: str):
        name = f"{lead.get('firstName', '')} {lead.get('lastName', '')}".strip()
        company = lead.get('companyName', 'Unknown Company')
        linkedin = lead.get('publicUrl', 'N/A')

        prompt = f"""
        Write a short, hyper-personalized professional summary of the following person in 4-5 sentences. 
        Avoid headings, bullet points, and formatting. Do not include phrases like "here is a profile."

        Start the summary by introducing the person using their full name and job title.

        Name: {name}
        Company: {company}
        LinkedIn: {linkedin}
        Company Info: {company_data}

        Make it sound natural, professional, and tailored to their role and company mission.
        """

        return self.generate(prompt, max_tokens=200)

    def generate_outreach(self, profile: str, sender_name: str = "Shiv Das"):
        prompt = f"""
        Based on the following profile, write a short, hyper-personalized cold outreach email ONLY. 
        Do not add summaries, explanations, or formatting instructions. Output just the email content.

        Profile:
        {profile}

        The email should include the following in the closing:

        Best regards, {sender_name}
        """
        return self.generate(prompt, max_tokens=300)


# Instantiate service
llm_service = LLMService()


# if __name__ == "__main__":
#     # Sample test data
#     lead = {
#         "firstName": "John",
#         "lastName": "Doe",
#         "company": "Tech Corp",
#         "linkedin_url": "https://www.linkedin.com/in/johndoe"
#     }

#     company_data = "Tech Corp specializes in AI-driven analytics and solutions for data-driven businesses."

#     profile = llm_service.generate_profile(lead, company_data)
#     print("Generated Profile:\n", profile)

#     sender_name = "Shiv Das"  # Replace with your name
#     company_name = "InfinityTech"  # Replace with your company name

#     outreach = llm_service.generate_outreach(profile, sender_name=sender_name, company_name=company_name)
#     print("\nGenerated Outreach Email:\n", outreach)
