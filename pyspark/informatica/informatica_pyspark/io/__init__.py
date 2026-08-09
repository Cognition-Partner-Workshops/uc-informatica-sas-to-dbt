from .base import ORDINAL_COL, SourceReader, TargetWriter
from .local_csv import LocalCsvReader, LocalCsvWriter
import base64
from pathlib import Path
from .snowflake import SnowflakeReader, SnowflakeWriter


def _snowflake_options(config, schema):
    options = {
        key: value
        for key, value in {
            "sfURL": config.account,
            "sfUser": config.user,
            "sfRole": config.role,
            "sfWarehouse": config.warehouse,
            "sfDatabase": config.database,
            "sfSchema": schema,
    }.items()
        if value
    }
    if config.private_key_path:
        from cryptography.hazmat.primitives import serialization

        key = serialization.load_pem_private_key(
            Path(config.private_key_path).read_bytes(), password=None
        )
        options["pem_private_key"] = base64.b64encode(
            key.private_bytes(
                serialization.Encoding.DER,
                serialization.PrivateFormat.PKCS8,
                serialization.NoEncryption(),
            )
        ).decode("ascii")
    return options


def get_reader(config):
    if config.io_mode == "local":
        return LocalCsvReader(None, config.source_dir, config.source_variant)
    return SnowflakeReader(None, _snowflake_options(config, config.source_schema))


def get_writer(config):
    if config.io_mode == "local":
        return LocalCsvWriter(config.target_dir)
    return SnowflakeWriter(_snowflake_options(config, config.target_schema))
