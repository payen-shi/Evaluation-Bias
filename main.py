import os
import sys
import tomllib
import nest_asyncio

project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_dir)

from configs.agents_config import AGENTS_SETUP
from src.constants import *
from src.utils import *

nest_asyncio.apply()

if __name__ == '__main__':
    # Initialise args
    config_dir = f'{project_dir}/configs'
    
    #######################################
    ### Patient Configs Loading Session ###
    #######################################
    patient_config_dir = f'{config_dir}/patients/'
    patient_config_list = os.listdir(patient_config_dir)
    patient_config_paths = [os.path.join(patient_config_dir, entry) for entry in patient_config_list if not os.path.isdir(os.path.join(patient_config_dir, entry))]
    
    all_patient: list[Patient] = []
    for config_path in patient_config_paths:
        with open(config_path, "rb") as f:
            patient_params = tomllib.load(f)
            all_patient.append(Patient(patient_params))
           
           
    ######################################
    ### Agents Configs Loading Session ###
    ######################################
    agent_config_dir = f'{config_dir}/agents'
    agent_config_list = os.listdir(agent_config_dir)
    agent_config_paths = [os.path.join(agent_config_dir, entry) for entry in agent_config_list if not os.path.isdir(os.path.join(agent_config_dir, entry))]

    # Agent initialization
    all_agents: list[Human_Agent] = []
    
    for config_path in agent_config_paths:
        with open(config_path, "rb") as f:
            agent_params = tomllib.load(f)

        # Get the agent type from the loaded file
        agent_type = agent_params['agent_type']

        # Fetch the corresponding configuration from AGENTS_CONFIG
        if agent_type not in AGENTS_SETUP:
            raise ValueError(f"Unsupported agent type: {agent_type}")

        # Extract class and platforms for the agent type
        agent_class = AGENTS_SETUP[agent_type]['class']
        platforms = AGENTS_SETUP[agent_type]['platforms']

        agent_idx = 0
        # Iterate over platforms and initialize agents
        for _, platform_config in platforms.items():
            count = platform_config['count']
            model_info = platform_config['model_info']

            for _ in range(count):
                agent_idx += 1
                # Create and append agent instance
                agent: Human_Agent = agent_class(agent_params, model_info)
                agent.name = f'{agent_type}_{agent_idx}'
                all_agents.append(agent)   
    
    # Sort agents by priority order
    priority_order = ['Junior', 'Mid', 'Senior']
    all_agents = sorted(all_agents, key=lambda x: (priority_order.index(x.name.split('_')[0]), int(x.name.split('_')[-1])))
    
    # Create results directory if it doesn't exist
    results_dir = f'{project_dir}/results'
    os.makedirs(results_dir, exist_ok=True)

    criteria_table_save_path = f'{results_dir}/criteria_final_score_table.xlsx'
    criteria_prompt = "If you are evaluating diagnostic report from other LLM models, please propose another 2 important criteria you think beyond the 6 given criteria. Only reply me the criteria name, separate with ','. NO need for other information."
    criteria_list = []
    agent_names_list = []
    agent_types_list = []

    #################################
    ### Agents Evaluation Session ###
    #################################
    for patient_idx, patient in enumerate(all_patient):
        
        final_table_save_path = f'{results_dir}/{patient.name}_final_score_table.xlsx'
        
        invalid_agents_idx = []
        input_message = define_input_message(patient)
        for idx, agent in enumerate(all_agents):
            agent_result_save_path = f'{results_dir}/{patient.name}_{agent.name}_{agent.model_info.TYPE}_evaluation_report.txt'
            agent_table_save_path = f'{results_dir}/{patient.name}_{agent.name}_{agent.model_info.TYPE}_score_table.csv'
            
            agent.make_judge()
            
            # Generate evaluation report
            agent.generate_report(input_message)
            
            # Generate score table
            agent.generate_score_table()
            
            # Remove agent if table is invalid
            if not isinstance(agent.table_df, pd.DataFrame):
                print(f'Agent {agent.name} table invalid, discard...')
                invalid_agents_idx.append(idx)
                continue
                
            # Save the table and evaluation report
            agent.table_df.to_csv(agent_table_save_path, index=False, encoding="utf-8-sig")
            
            with open(agent_result_save_path, "w") as file:
                file.write(agent.report)

            print(f'Agent {agent.name} processed and saved.')
            
            if patient_idx == len(all_patient) - 1:
                agent.generate_report(criteria_prompt)
                criteria_list.append(agent.report)
                agent_names_list.append(agent.name)
                agent_types_list.append(agent.model_info.TYPE)
        
        # Remove invalid agents from the list
        all_agents = [agent for idx, agent in enumerate(all_agents) if idx not in invalid_agents_idx]
        
        # Generate a combined score table from all agents
        final_table_df = generate_combined_score_table(all_agents)
        
        # Save the large table to an Excel file with merged cells
        save_with_merged_cells(final_table_df, final_table_save_path)

    criteria_df = pd.DataFrame({
        'Agent Name': agent_names_list,
        'Agent Type': agent_types_list,
        'Top 2 important Criteria': criteria_list
    })
    criteria_df.to_excel(criteria_table_save_path, index=False)
