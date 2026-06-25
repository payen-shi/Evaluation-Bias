"""
----------------
constants.py
----------------
This module defines constants and template strings used throughout this project.
It provides project descriptions, evaluation criteria, feedback templates, and standardized messages for agent interactions.
These constants facilitate consistent formatting and scoring in the evaluation of Large Language Models (LLMs) for medical diagnosis tasks.
----------------
"""

import textwrap

FULL_SCORE = 100

PROJECT_DESCRIPTION = textwrap.dedent(
    """
    Project name: GPT-Powered Adaptive Evaluating Assistant. Assessing the capabilities of several Large Language Models (LLMs) in interpreting a case report. Initially, all models are provided with the case report to make a diagnosis in a first response, then check their answer and generate a second response as double check to ensure the accuracy of the diagnosis. Two responses from each LLM model are given, and you will need to comprehensively evaluate both responses, and evaluate the capabilities of these LLMs in assisting medical diagnosis from several aspects, where each aspects should with scores and comments.
    """
)

TASK_CONTENT = textwrap.dedent(
    f"""
    Read the above project description and the given diagnostic report from each LLM and finish your evaluation task. Please make sure you evaluated results from ALL MODELS!!!
    """
)

EVALUATION_CRITERIA = textwrap.dedent(
            f"""
            ### **评估的不同维度 (1-{FULL_SCORE} points)**
            - **理解程度**: 你是否认为模型完全理解并良好归纳我们所提供的病例信息。
            - **逻辑性**: 你认为模型分析是否合乎医学逻辑。
            - **准确性**: 你是否认为模型诊断是准确的。
            - **帮助性**: 你是否认为模型提供的信息有助于临床诊断并进一步指导临床方案的制定。
            - **无害性**: 你是否认为模型提供的信息可以避免对患者的漏诊和误诊。
            - **结构化**: 你是否认为模型输出的形式是简洁明了，条理清晰的。
            """
        )

EXAMPLE_FEEDBACK_SUMMARY_TEMPLATE = textwrap.dedent(
    f"""
    ### 评估结果
    1. #### **Model XXXXXXXXXXXXX 评估**
    - **理解程度**: X/{FULL_SCORE}
    - 评价: XXXXXXXXXXXXX。
    
    - **逻辑性**: X/{FULL_SCORE}
    - 评价: XXXXXXXXXXXXX。

    （其他criteria依此类推）
    --------------------------------------
    2. #### **Model XXXXXXXXXXXXX 评估**
    - **理解程度**: X/{FULL_SCORE}
    - 评价: XXXXXXXXXXXXX。
    
    - **逻辑性**: X/{FULL_SCORE}
    - 评价: XXXXXXXXXXXXX。

    （其他criteria依此类推）
    --------------------------------------
    (其他模型依此类推)
    """
)

EXAMPLE_FEEDBACK_FINAL_SUMMARY_TEMPLATE = textwrap.dedent(
    f"""
    ### 总结：
    #### **评估员：xxxxxxxxx（扮演的角色character完整名称）**
    #### 评估员意见
    Model A XXXXXXXXXXXXXXXXXXXX, etc。Model B XXXXXXXXXXXXX, etc。
    """
)

EXAMPLE_FEEDBACK_TEMPLATE = textwrap.dedent(
    f"""
    谢谢您提供的详细病例信息和模型的诊断报告。我扮演的角色是XXXXXXXXXXXXXXXXXXX(扮演角色的character和background)。
    根据我的专业背景和经验，我将对所有模型的诊断报告进行评估。以下是我的评分和评价：
    {EXAMPLE_FEEDBACK_SUMMARY_TEMPLATE}
    --------------------------------------
    --------------------------------------
    {EXAMPLE_FEEDBACK_FINAL_SUMMARY_TEMPLATE}
    """
)