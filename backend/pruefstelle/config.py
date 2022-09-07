# Switching environments: `ENV_FOR_PRUEFSTELLE=production pruefstelle run`
import os
from dynaconf import Dynaconf

HERE = os.path.dirname(os.path.abspath(__file__))

settings = Dynaconf(
    envvar_prefix="pruefstelle",
    env_switcher="ENV_FOR_PRUEFSTELLE",
    settings_files=["settings/.secrets.toml"],
    environments=["development", "production"],
    load_dotenv=False,
)
