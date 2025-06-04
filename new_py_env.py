"""
For setting up a new python development project
- conda python environment
- uv manage packages
- autoenv for automatically setting the environment when entering/leaving the directory
- API keys pulled in from ~/.ssh as environment variables
"""


from pathlib import Path
from dataclasses import dataclass, field
import subprocess


def create_new_environment():
    env = get_env_details()

    # create each file
    create_gitignore()
    create_autoenv(env.environment_name, env.api_keys)

    # create the conda environment
    subprocess.run(["conda", "create", "-n", env.environment_name, f"python={env.python_version}"], check=True)

    # create the uv environment
    subprocess.run(["uv", "init"], check=True)



@dataclass
class EnvSetup:
    environment_name: str
    python_version: str
    api_keys: dict[str, str] = field(default_factory=dict)


def select_multiple(prompt: str, options: list[str]) -> list[str]:
    print(prompt)
    for i, option in enumerate(options, 1):
        print(f"[{i}] {option}")
    print("Enter numbers separated by commas (or press Enter to skip):")
    choice = input("Selection: ").strip()
    indices = map(int, filter(None, map(lambda x: x.strip(), choice.split(','))))
    selected = [options[i-1] for i in indices]

    return selected

def make_default_key(stem: str) -> str:
    try:
        chunks = stem.split("_")
        final = '_'.join(chunks[-3:])
        return final.upper()
    except:
        pass

    print(f'failed to process key. returning unprocessed stem "{stem}"')
    return f"{stem.upper()}"

def get_env_details() -> EnvSetup:
    env_name = input("Enter environment name: ").strip()
    py_version = input("Select Python version: ").strip()

    ssh_path = Path.home() / ".ssh"
    key_files = list(ssh_path.glob("*api_key.txt"))
    key_files = [f.name for f in key_files]
    key_files = sorted(key_files)
    selected_files = select_multiple("Select API key files:", key_files)

    api_keys = {}
    for file in selected_files:
        stem = Path(file).stem.upper()
        default_key_name = make_default_key(stem)
        custom_key = input(f"Enter key name for {file} (default: {default_key_name}): ").strip()
        key_name = custom_key if custom_key else default_key_name
        api_keys[key_name] = file

    return EnvSetup(
        environment_name=env_name,
        python_version=py_version,
        api_keys=api_keys
    )



def create_gitignore():
    Path(".gitignore").write_text("""\
# autoenv files
.autoenv
.autoleave

# python cache
__pycache__/
""")



def create_autoenv(conda_env_name:str, api_keys:dict[str, str]) -> tuple[str, str]:

    # set up the autoenv file
    autoenv_src = f"""\
# set up UV to work with the conda virtual environment
conda activate {conda_env_name}
VIRTUAL_ENV=$(echo $CONDA_PREFIX)
UV_PROJECT_ENVIRONMENT=$(echo $VIRTUAL_ENV)
UV_PYTHON=$(which python)
"""
    if api_keys:
        autoenv_src += "\n# pull in API keys for accessing LLMs\n" + "\n".join([f"export {key}=$(cat ~/.ssh/{value})" for key, value in api_keys.items()])
    Path(".autoenv").write_text(autoenv_src)

    # set up the autoleave file
    autoleave_src = f"""\
    conda deactivate
    """
    if api_keys:
        autoleave_src += "\n# remove API keys for accessing LLMs\n" + "\n".join([f"export {key}=''" for key in api_keys.keys()])
    Path(".autoleave").write_text(autoleave_src)








if __name__ == "__main__":
    create_new_environment()