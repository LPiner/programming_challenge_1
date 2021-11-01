from attr import attrs
import toml


@attrs(auto_attribs=True, frozen=True)
class AppConfig:
    DB_USERNAME: str
    DB_PASSWORD: str
    DB: str


def get_app_config(env: str) -> AppConfig:
    config = toml.load(f"config/{env}.toml")
    return AppConfig(
        DB_USERNAME=config["DB"]["username"],
        DB_PASSWORD=config["DB"]["password"],
        DB=config["DB"]["db"],
    )