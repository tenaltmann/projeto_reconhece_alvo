import subprocess

execute_action = "arduino-cli upload -p COM3 --fqbn arduino:avr:uno C:/Users/tenaltmann/Desktop/www/acionamento_coleira_com_Node_e_Arduino/acionamento_remoto"

def run_action():

    subprocess.run(execute_action, shell=True)