from strands import Agent, tool
from strands_tools import calculator # Import the calculator tool
import argparse
import json
from strands.models import BedrockModel
import boto3

# Create a custom tool 
@tool
def weather():
    """ Get weather """ # Dummy implementation
    return "sunny"



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
            self.session = boto3.Session(profile_name=profile_name, region_name="us-east-1")
            self.model = BedrockModel(
                model_id=self.model_id,
                boto_session=self.session
                #region_name="us-east-1"
            )

    def strands_agent_bedrock(self, payload):
        ## Initialize 
        agent = Agent(
        model=self.model,
        tools=[calculator, weather],
        system_prompt="You're a helpful assistant. You can do simple math calculation, and tell the weather. If user request or ask anything other than math calculation or weather info, then politely refuse. "
        )

        """
        Invoke the agent with a payload
        """
        user_input = payload.get("prompt")
        response = agent(user_input)
        return response.message['content'][0]['text']



if __name__ == "__main__":
    ## To test this agent locally, invoke from shell --> python strands_agent.py '{"prompt":"hello"}'
    parser = argparse.ArgumentParser()
    parser.add_argument("payload", type=str)
    args = parser.parse_args()
    try:

        agent = BedrockStrandsAgent(profile_name="")
        response = agent.strands_agent_bedrock(json.loads(args.payload))
    except Exception as e:
        print('Exception - {0}'.format(e))
        