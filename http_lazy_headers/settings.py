# -*- coding: utf-8 -*-


class Settings:

    def __init__(
            self,
            header_values_max=25,
            value_params_max=25,
            header_max_len=4 * 1024,
            content_max_size=1024 * 1024,
            host_unsafe_allow=False,
            debug=True):
        # Maximum number of header values willing to parse
        self.HEADER_VALUES_MAX = header_values_max

        # Maximum number of value params willing to parse
        self.VALUE_PARAMS_MAX = value_params_max

        # Maximum length for a header line.
        # Should be greater (or equal) than
        # request_line_max_len
        self.HEADER_MAX_LEN = header_max_len

        # Maximum size in bytes for the body message/payload
        self.CONTENT_MAX_SIZE = content_max_size
        self.CONTENT_MAX_CHARS = len(str(content_max_size))

        # This prevents common attacks,
        # when it's `False`, it only allows
        # valid domains or IPs
        self.HOST_UNSAFE_ALLOW = host_unsafe_allow

        # Debug mode for logging
        self.DEBUG = debug


settings = Settings()


def set_settings(settings_obj):
    assert isinstance(settings_obj, Settings)

    for attr in vars(settings_obj):
        if (attr.startswith('__') and
                attr.endswith('__')):
            continue

        setattr(
            settings,
            attr,
            getattr(settings_obj, attr))
