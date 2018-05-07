import ipaddress

from typing import Tuple

from crawlino.models.plugins_models import PluginReturnedData


class SourceData(PluginReturnedData):
    """
    This data type map different sources. Each type are included as a string
    in property: 'source_type'.

    Allowed values for 'source_type' are:

    - ip
    - file
    - handler: for file descriptors or ttys
    - web
    - uri: a generic case of web
    - domain
    """

    __slots__ = ("target", "source_type")

    def __init__(self,
                 target: Tuple[str, str] or str):
        """
        Handling file:

        >>> SourceData(target="file://home/user/file-name.txt")

        Handling IP

        >>> SourceData(target=("127.0.0.1", 9000))

        Handling Domain

        >>> SourceData(target="http://mysite.com:8000"))

        Handling tty

        >>> SourceData(target="/dev/tty0"))
        """
        self.target = target
        self.source_type: str = None

        # fixing source type
        if not self.source_type:
            try:
                ipaddress.IPv4Address(self.target)
                self.source_type = "ip"
            except ipaddress.AddressValueError:

                if self.target.startswith("file"):
                    self.source_type = "file"
                elif self.target.startswith("/dev"):
                    self.source_type = "handler"
                elif "http://" in self.target or "https://" in self.target:
                    self.source_type = "web"
                elif "://" in self.target:
                    self.source_type = "uri"
                else:
                    self.source_type = "domain"

    def __str__(self):
        if self.source_type == "ip":
            ip, port = self.target
            return f"{ip}_{port}"
        else:
            return self.target

    @property
    def to_dict(self):
        return dict(
            target=self.target,
            source_type=self.source_type
        )


__all__ = ("SourceData", )
