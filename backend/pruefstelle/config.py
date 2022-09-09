import sys
import warnings

from dynaconf import Dynaconf

if not sys.warnoptions:
    warnings.simplefilter("ignore")

settings = Dynaconf(
    envvar_prefix="pruefstelle",
    env_switcher="ENV_FOR_PRUEFSTELLE",
    settings_files=["settings/config.toml", "settings/.secrets.toml"],
    environments=["development", "production"],
    load_dotenv=False,
)
