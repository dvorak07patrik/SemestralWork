import subprocess
import sys

def run_script(script_name):
    try:
        # Run the script and wait for it to complete
        result = subprocess.run([sys.executable, script_name], check=True)
        print(f"Script {script_name} completed successfully with return code {result.returncode}")
    except subprocess.CalledProcessError as e:
        print(f"Script {script_name} failed with return code {e.returncode}")
    except Exception as e:
        print(f"An error occurred while running script {script_name}: {str(e)}")

if __name__ == "__main__":
    scripts_to_run = ['uploadCircuits.py', 'uploadConstructors.py', 'uploadDrivers.py', 'uploadRaces.py', 'uploadResults.py', 'uploadDriverStandings.py', 'uploadConstructorStandings.py', 'uploadLapTimes.py', 'uploadPitStops.py', 'uploadQualifying.py']

    for script in scripts_to_run:
        run_script(script)
