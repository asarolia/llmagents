from strands import Agent, tool
from strands_tools import calculator # Import the calculator tool
import argparse
import json
from strands.models import BedrockModel
import boto3
# 1. Import the Runtime app
from bedrock_agentcore.runtime import BedrockAgentCoreApp

# 2. Initialize the runtime App
app = BedrockAgentCoreApp()

class BedrockStrandsAgent:
    def __init__(self, profile_name):
        self.model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
            
        # check if profile is null
        if not profile_name:
            print("IAM Profile not passed, running script by assuming assigned EC2 role")
            self.model = BedrockModel(
                model_id=self.model_id,
                region_name="us-east-1"
            )
        else:
            print("Running script using passed IAM profile")
            self.session = boto3.Session(profile_name=profile_name, region_name="us-east-1")
            self.model = BedrockModel(
                model_id=self.model_id,
                boto_session=self.session
                #region_name="us-east-1"
            )


# Create a custom tool 
@tool
def weather():
    """ Get weather """ # Dummy implementation
    return "sunny"


# 3. Decorate the entrypoint function with entrypoint decorator 
@app.entrypoint
def strands_agent_bedrock(payload):

    user_input = payload.get("prompt")

    agent = BedrockStrandsAgent(profile_name="")

    ## Initialize 
    strands_agent = Agent(
    model= agent.model,
    tools=[calculator, weather],
    system_prompt="You're a helpful assistant. You can do simple math calculation, and tell the weather. If user request or ask anything other than math calculation or weather info, then politely refuse. "
    )
    response = strands_agent(user_input)
    return response.message['content'][0]['text']

    


if __name__ == "__main__":
    # ## To test this agent locally 
    # 1. --> python strands_agent_for_runtime.py
    # 2. --> curl -X POST http://localhost:8080/invocations -H "Content-Type: application/json" -d '{"prompt":"hello"}'

    # Use the Bedrock Agent Core runtime to control the app
    app.run()
        