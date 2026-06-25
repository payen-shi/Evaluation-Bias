"""
----------------
patient.py
----------------
Short utilities and data model for representing a patient used by evaluation workflows.
Provides the Patient class, a lightweight container holding:
- name: patient identifier (str)
- clinical_records: clinical data associated with the patient
- target_illness: the illness being evaluated
- diagnostic_reports_: optional mapping of model names to their diagnostic reports
Constructor expects a params dict with:
- 'patient_info': dict containing 'name', 'clinical_records', and 'target_illness'
- optional 'diagnostic_report': dict mapping model -> report
----------------
"""
class Patient:
    def __init__(self, params):
        self.name = params['patient_info']['name']
        self.clinical_records = params['patient_info']['clinical_records']
        self.target_illness = params['patient_info']['target_illness']
        self.diagnostic_reports_ = dict()
        
        all_diagnostic: dict = params.get('diagnostic_report', {})
        for model, diagnostic_report in all_diagnostic.items():
            single_diagnostic_report: dict = {}
            single_diagnostic_report[model] = diagnostic_report
            
            self.diagnostic_reports_.update(single_diagnostic_report)
        
    