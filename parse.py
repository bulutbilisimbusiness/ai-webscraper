import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

template=(
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **If No Match Found:** If you cannot find the requested information, respond with 'No matching data found on this page section.' "
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested."
    "5. **Be Thorough:** Look carefully through all the text content provided before concluding no data exists."
)

# Groq model - Free and fast AI API
model = ChatGroq(
    model="llama3-8b-8192",  # Free Llama3 model
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.1
)

def parse_with_ai(dom_chunks, parse_description):
    if not os.getenv("GROQ_API_KEY"):
        return "ERROR: GROQ_API_KEY not found in .env file!"
    
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    
    parsed_results = []
    for i, chunk in enumerate(dom_chunks, start=1):
        try:
            response = chain.invoke({
                "dom_content": chunk,
                "parse_description": parse_description
            })
            result = response.content.strip()
            if result and result != "No matching data found on this page section.":
                parsed_results.append(f"=== Batch {i} Results ===\n{result}")
            else:
                parsed_results.append(f"=== Batch {i} ===\nNo data found in this section")
        except Exception as e:
            error_msg = f"=== Batch {i} ERROR ===\nError: {str(e)}"
            parsed_results.append(error_msg)
    
    if not parsed_results:
        return "No data was found in any page section. Check if the page loaded correctly."
    
    return "\n\n".join(parsed_results)    
        
        
    