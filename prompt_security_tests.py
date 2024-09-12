from ps_fuzz.app_config import AppConfig
from ps_fuzz.prompt_injection_fuzzer import run_fuzzer
import pandas as pd


# Default configuration
config = {
        'attack_provider': 'open_ai',
        'attack_model': 'gpt-3.5-turbo',
        'target_provider': 'open_ai',
        'target_model': 'gpt-3.5-turbo',
        'num_attempts': 3,
        'num_threads': 4,
        'attack_temperature': 0.6,
        'custom_benchmark':None,
        'system_prompt': system_prompt,
        'tests' :[],
}

app_config = AppConfig("",config_state=config)
run_fuzzer(app_config)

# contextual_redirection - Attempt at tricking the LLM into adopting a specific role (Roleplay) that may bypass the restrictions or intended use set by the system prompt
# system_prompt_stealer - Attempt to steal the system prompt from the LLM by asking it to output its internal configuration or other sensitive information.
# typoglycemia_attack - Attempt to exploit a text processing vulnerability in LLMs that can cause them to generate incorrect responses to queries by removing random characters from words.
# custom_benchmark_test - Challenge the LLM with a dataset of prompt injections given by the user.
# You should prioritize tests that broke your system prompt.
# You can run --list-attacks to find all possible tests.
tests = ['contextual_redirection', 'system_prompt_stealer','typoglycemia_attack','custom_benchmark_test']
config = {
        'attack_provider': 'open_ai',
        'attack_model': 'gpt-3.5-turbo',
        'target_provider': 'open_ai',
        'target_model': 'gpt-3.5-turbo',
        'num_attempts': 3,
        'num_threads': 4,
        'attack_temperature': 0.6,
        'custom_benchmark':custom_benchmark,
        'system_prompt': _DEFAULT_TEMPLATE,
        'tests':tests,
    }
app_config = AppConfig("",config_state=config)
run_fuzzer(app_config)

# final tests
all_tests = ['amnesia', 'authoritative_role_impersonation', 'contextual_redirection', 'affirmative_suffix', 'system_prompt_stealer', 'linguistic_evasion', 'typoglycemia_attack', 'do_anything_now_jailbreak', 'aim_jailbreak', 'self_refine', 'ethical_compliance', 'ucar', 'complimentary_transition', 'harmful_behavior', 'base64_injection', 'custom_benchmark_test']
config = {
        'attack_provider': 'open_ai',
        'attack_model': 'gpt-3.5-turbo',
        'target_provider': 'open_ai',
        'target_model': 'gpt-3.5-turbo',
        'num_attempts': 3,
        'num_threads': 4,
        'attack_temperature': 0.6,
        'custom_benchmark':None,
        'system_prompt': new_system_prompt,
        'tests':tests,
    }
app_config = AppConfig("",config_state=config)
run_fuzzer(app_config)