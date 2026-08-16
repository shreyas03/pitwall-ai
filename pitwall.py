import os
import autogen
from autogen.coding import LocalCommandLineCodeExecutor
from dotenv import load_dotenv

load_dotenv()

# --- AutoGen LLM Config ---
llm_config = {
    "config_list": [{"model": "gpt-4o-mini", "api_key": os.environ.get("OPENAI_API_KEY")}],
    "temperature": 0.0, # 0.0 for maximum coding accuracy
}

# --- 1. Set up the Code Execution Environment ---
work_dir = "coding"
os.makedirs(work_dir, exist_ok=True)

executor = LocalCommandLineCodeExecutor(    
    timeout=10, 
    work_dir=work_dir,
)

# --- 2. Create the Agents ---

race_engineer = autogen.ConversableAgent(
    name="Race_Engineer",
    system_message=(
        "You are the Lead F1 Data Analyst on the pitwall. "
        "You have access to a local SQLite database named '../Formula1.sqlite'. "
        "To answer questions, you must write a Python script using the 'sqlite3' and 'pandas' libraries to query the database. "
        "The database contains standard Ergast F1 tables: 'races', 'results', 'drivers', 'constructors', 'lap_times', 'pit_stops', etc. "
        "First, write code to inspect the table schema if you are unsure. Then, write code to query the exact answer. "
        "Print the final result in your Python script so the Team Principal can see it. "
        "CRITICAL RULE: Do NOT output the word TERMINATE in the same message where you write Python code. "
        "Wait for the Team Principal to execute your code and return the terminal output. "
        "Once you have read the output, explain the final answer to the user in plain text, and ONLY THEN output the word TERMINATE."
    ),
    llm_config=llm_config,
    human_input_mode="NEVER", 
)

# YOU are now playing the role of the Team Principal
team_principal = autogen.ConversableAgent(
    name="You",
    system_message="Execute the Python code the Race Engineer gives you and report back the terminal output.",
    llm_config=False, 
    human_input_mode="TERMINATE", # <--- The magic change! Gives you the keyboard when the AI finishes.
    code_execution_config={"executor": executor}, 
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"]
)

# --- 3. Start the Live Simulation ---
if __name__ == "__main__":
    print("\n" + "="*50)
    print("LIVE PITWALL RADIO CHANNEL INITIATED.")
    print("="*50 + "\n")
    
    # Grab your first question directly from the terminal
    first_question = input("Radio Check! What is your question for the Race Engineer?\n> ")
    
    team_principal.initiate_chat(
        race_engineer,
        message=first_question
    )
