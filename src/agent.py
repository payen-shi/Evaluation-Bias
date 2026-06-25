"""
----------------
agent.py
----------------
This module defines agent classes for simulating human evaluators with varying levels of medical expertise (Junior, Mid, Senior) in the context of evaluating large language models (LLMs) for clinical diagnosis support. Each agent is assigned a persona and background, and is capable of generating evaluation reports and structured score tables based on predefined criteria.

Classes:
    Human_Agent: Base class for human-like agents, providing methods for persona definition, evaluation, and score table generation.
    Junior: Represents a junior clinical medical student agent with randomized attributes.
    Mid: Represents a mid-level medical doctor agent with randomized attributes.
    Senior: Represents a senior international expert agent with extensive experience.
----------------
"""

import random
import textwrap
import pandas as pd

from io import StringIO
from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.models import ModelFactory

from src.constants import EXAMPLE_FEEDBACK_TEMPLATE, EVALUATION_CRITERIA, FULL_SCORE
from configs.API_INFO import *

"""
Class: Human_Agent

Description:
    Human_Agent is a base class that models a human evaluator for medical AI systems.
    It encapsulates persona attributes, example feedback templates, evaluation criteria,
    and the chat agent used to produce textual evaluation reports and a structured score table.

Attributes (created by constructor / methods):
    - model_info: model configuration object used to instantiate the chat model.
    - name: optional human-readable name for the agent.
    - institution, gender, identity, research_field, work_time: persona properties.
    - persona_basic, persona_background: human-readable persona strings.
    - example_feedback: example feedback template (populated by _define_example_feedback).
    - criteria: evaluation criteria (populated by _define_criteria).
    - chat_agent: initialized ChatAgent instance after make_judge() is called.
    - report: textual report produced by the agent.
    - table_df: pandas.DataFrame containing parsed score table after generate_score_table().

Returns:
    - The constructor returns an initialized object instance.
    - make_judge() sets up and stores a ChatAgent on self.chat_agent.
    - generate_report(input_message) populates self.report.
    - generate_score_table() populates self.table_df (or None on failure).

Public methods:
    - _define_example_feedback(): load or assign example feedback template to self.example_feedback.
    - _define_criteria(): load or assign evaluation criteria to self.criteria.
    - make_judge(): build system message, instantiate model via ModelFactory, create ChatAgent and set language.
    - generate_report(input_message): send a single step to chat_agent and save the response text.
    - generate_score_table(): ask the agent for a CSV-formatted score table, parse into pandas.DataFrame,
        validate required columns, compute a summary score column and assign to self.table_df.
"""
class Human_Agent:
    def __init__(self):
        self.model_info: Base_Model_Info = None
        self.name = None
        
        self.institution = None
        self.gender = None
        self.identity = None
        self.research_field = None
        
        self.persona_basic = None
        self.persona_background = None
        self.example_feedback = None
        self.criteria = None

        self.genders_list = ['男性', '女性']
        self.task_description = '现在你在参与研究一个项目,需要评估多个LLM对于某些疾病诊断的帮助。'
        
    def _define_example_feedback(self):
        self.example_feedback = EXAMPLE_FEEDBACK_TEMPLATE
        
    def _define_criteria(self):
        self.criteria = EVALUATION_CRITERIA
        
    def make_judge(self):
        self.msg_content = textwrap.dedent(
            f"""
            You are a judge in a medical AI.
            This is your persona: you MUST act as {self.persona_basic} character, and you have character background with {self.persona_background}.{self.task_description}
            Here is an example feedback that you might give with your persona, you MUST try your best to align with the following template:
            {self.example_feedback}
            When evaluating projects, you must use the following criteria:
            {self.criteria}
            You also need to give scores based on these criteria, in the range of 1-{FULL_SCORE}. The score given should be like 3/{FULL_SCORE}, 5/{FULL_SCORE}, 8/{FULL_SCORE}, etc.
            """
        )

        sys_msg = BaseMessage.make_assistant_message(
            role_name="Clinical Records Judge",
            content=self.msg_content,
        )

        model = ModelFactory.create(
            model_platform=self.model_info.PLATFORM,
            model_type=self.model_info.TYPE,
            api_key=self.model_info.API_KEY,
            url=self.model_info.API_BASE_URL,
        )

        agent = ChatAgent(
            system_message=sys_msg,
            model=model,
        )
        
        agent.set_output_language('English')

        self.chat_agent = agent
        
    def generate_report(self, input_message):
        response = self.chat_agent.step(input_message)
        self.report = response.msg.content
        
    def generate_score_table(self):
        score_table = self.chat_agent.step(
            'Excellent! Based on the marking table you generated in your report, could you please only output the score table contents? ONLY contains table please, no other things, and then format this table data as structured CSV-ready content.'
        ).msg.content

        start_index = score_table.find("\n") + 1
        end_index = score_table.rfind("\n")  # Find the last newline
        extracted_data = score_table[start_index:end_index]

        # Convert the string to a Pandas DataFrame
        try:
            table_data = StringIO(extracted_data)
            table_df = pd.read_csv(table_data)

            # Check if the DataFrame is empty
            if table_df.empty:
                raise ValueError("The score table is empty.")
            
            # Clean column names by stripping spaces
            table_df.columns = table_df.columns.str.strip()

            # List of required score columns
            score_columns = ["理解程度", "逻辑性", "准确性", "帮助性", "无害性", "结构化"]

            # Check if all required columns exist in the DataFrame
            if not all(col in table_df.columns for col in score_columns):
                raise KeyError("One or more required columns are missing from the score table.")

            # Calculate the total score and add it as a new column
            table_df["总分"] = table_df[score_columns].mean(axis=1).round(2)
            
            self.table_df = table_df

        except Exception as e:
            # Handle any parsing errors or validation issues
            print(f"Error while processing score table: {e}")
            self.table_df = None

# Junior doctor agent class
class Junior(Human_Agent):
    def __init__(self, params, model_info):
        super().__init__()
        self.model_info = model_info
        
        self.identity_list = params['identity_list']
        self.institution_list = params['institution_list']
        self.research_fields_list = params['research_fields_list']
        self.work_time_list = params['work_time_list']
        
        self.identity = random.choice(self.identity_list)
        self.gender = random.choice(self.genders_list)
        self.institution = random.choice(self.institution_list)
        self.research_field = random.choice(self.research_fields_list)
        self.work_time = random.choice(self.work_time_list)
        
        self._define_persona()
        self._define_example_feedback()
        self._define_criteria()
        
    def _define_persona(self):
        self.persona_basic = f'你是一名{self.institution}的{self.research_field}的{self.gender}{self.identity}。'
        self.persona_background = f'作为规培或学业任务中的一部分，你已经以实习临床医学生的身份参与了{self.work_time}的临床工作。'

# Mid-career doctor agent class
class Mid(Human_Agent):
    def __init__(self, params, model_info):
        super().__init__()
        self.model_info = model_info
        
        self.identity_list = params['identity_list']
        self.institution_list = params['institution_list']
        self.research_fields_list = params['research_fields_list']
        self.work_time_list = params['work_time_list']
        
        self.identity = random.choice(self.identity_list)
        self.gender = random.choice(self.genders_list)
        self.institution = random.choice(self.institution_list)
        self.research_field = random.choice(self.research_fields_list)
        self.work_time = random.choice(self.work_time_list)
        
        self._define_persona()
        self._define_example_feedback()
        self._define_criteria()
        
    def _define_persona(self):
        self.persona_basic = f'你是{self.institution}的{self.research_field}的{self.gender}{self.identity}。'
        self.persona_background = f'你最高学历是医学硕士研究生或是医学博士研究生(Master of Medicine, Doctor of Medicine）,你有{self.work_time}的临床工作经验。'
        
# Senior doctor agent class
class Senior(Human_Agent):
    def __init__(self, params, model_info):
        super().__init__()
        self.model_info = model_info
        
        self.research_fields_list = params['research_fields_list']
        self.work_time_list = params['work_time_list']
        
        self.gender = random.choice(self.genders_list)
        self.research_field = random.choice(self.research_fields_list)
        self.work_time = random.choice(self.work_time_list)
        
        self._define_persona()
        self._define_example_feedback()
        self._define_criteria()
        
    def _define_persona(self):
        self.persona_basic = f'你是一个国际知名的{self.gender}专家。'
        self.persona_background = f'你不仅是一个国际知名医学院的{self.research_field}教授，还是这个医学院附属的一个大型医院的主任医师，你有{self.work_time}的{self.research_field}相关的科研,临床,教学经验,有非常坚实的理论基础和非常丰富的临床实践经验。你承担十几项关于{self.research_field}的国际研究项目,你的研究结果经常在Science, Nature, NEJM等顶级杂志上发表。'