from __future__ import annotations

import urllib.parse

from typing import TYPE_CHECKING
from typing import Iterable

from cleo.io.io import IO
from poetry.repositories.http import HTTPRepository


try:
    from poetry.core.packages.dependency_group import MAIN_GROUP
except ImportError:
    MAIN_GROUP = "default"


if TYPE_CHECKING:
    from pathlib import Path

    from poetry.poetry import Poetry


class Exporter:
    """
    Exporter class to export a lock file to alternative formats.
    """

    FORMAT_REQUIREMENTS_TXT = "requirements.txt"
    ALLOWED_HASH_ALGORITHMS = ("sha256", "sha384", "sha512")

    EXPORT_METHODS = {FORMAT_REQUIREMENTS_TXT: "_export_requirements_txt"}

    def __init__(self, poetry: Poetry) -> None:
        self._poetry = poetry
        self._with_hashes = True
        self._with_credentials = False
        self._with_urls = True
        self._with_markers = True
        self._extras: bool | list[str] | None = []
        self._groups: Iterable[str] = [MAIN_GROUP]

    @classmethod
    def is_format_supported(cls, fmt: str) -> bool:
        return fmt in cls.EXPORT_METHODS

    def with_extras(self, extras: bool | list[str] | None) -> Exporter:
        self._extras = extras

        return self

    def only_groups(self, groups: Iterable[str]) -> Exporter:
        self._groups = groups

        return self

    def with_urls(self, with_urls: bool = True) -> Exporter:
        self._with_urls = with_urls

        return self

    def with_hashes(self, with_hashes: bool = True) -> Exporter:
        self._with_hashes = with_hashes

        return self

    def with_credentials(self, with_credentials: bool = True) -> Exporter:
        self._with_credentials = with_credentials

        return self

    def with_markers(self, with_markers: bool = True) -> Exporter:
        self._with_markers = with_markers

        return self

    def export(self, fmt: str, cwd: Path, output: IO | str) -> None:
        if not self.is_format_supported(fmt):
            raise ValueError(f"Invalid export format: {fmt}")

        getattr(self, self.EXPORT_METHODS[fmt])(cwd, output)

    def _export_requirements_txt(self, cwd: Path, output: IO | str) -> None:
        from poetry.core.packages.utils.utils import path_to_url

        indexes = set()
        content = ""
        dependency_lines = set()

        root = self._poetry.package.with_dependency_groups(
            list(self._groups), only=True
        )

        for dependency_package in self._poetry.locker.get_project_dependency_packages(
            project_requires=root.all_requires,
            project_python_marker=root.python_marker,
            extras=self._extras,
        ):
            line = ""

            dependency = dependency_package.dependency
            package = dependency_package.package

            if package.develop:
                line += "-e "

            requirement = dependency.to_pep_508(with_extras=False)
            is_direct_local_reference = (
                dependency.is_file() or dependency.is_directory()
            )
            is_direct_remote_reference = dependency.is_vcs() or dependency.is_url()

            if is_direct_remote_reference:
                line = requirement
            elif is_direct_local_reference:
                assert dependency.source_url is not None
                dependency_uri = path_to_url(dependency.source_url)
                line = f"{package.complete_name} @ {dependency_uri}"
            else:
                line = f"{package.complete_name}=={package.version}"

            if (
                self._with_markers
                and not is_direct_remote_reference
                and ";" in requirement
            ):
                markers = requirement.split(";", 1)[1].strip()
                if markers:
                    line += f" ; {markers}"

            if (
                not is_direct_remote_reference
                and not is_direct_local_reference
                and package.source_url
            ):
                indexes.add(package.source_url)

            if package.files and self._with_hashes:
                hashes = []
                for f in package.files:
                    h = f["hash"]
                    algorithm = "sha256"
                    if ":" in h:
                        algorithm, h = h.split(":")

                        if algorithm not in self.ALLOWED_HASH_ALGORITHMS:
                            continue

                    hashes.append(f"{algorithm}:{h}")

                hashes.sort()

                for h in hashes:
                    line += f" \\\n    --hash={h}"

            dependency_lines.add(line)

        content += "\n".join(sorted(dependency_lines))
        content += "\n"

        if indexes and self._with_urls:
            # If we have extra indexes, we add them to the beginning of the output
            indexes_header = ""
            for index in sorted(indexes):
                repositories = [
                    r
                    for r in self._poetry.pool.repositories
                    if isinstance(r, HTTPRepository) and r.url == index.rstrip("/")
                ]
                if not repositories:
                    continue
                repository = repositories[0]
                if (
                    self._poetry.pool.has_default()
                    and repository is self._poetry.pool.repositories[0]
                ):
                    url = (
                        repository.authenticated_url
                        if self._with_credentials
                        else repository.url
                    )
                    indexes_header = f"--index-url {url}\n"
                    continue

                url = (
                    repository.authenticated_url
                    if self._with_credentials
                    else repository.url
                )
                parsed_url = urllib.parse.urlsplit(url)
                if parsed_url.scheme == "http":
                    indexes_header += f"--trusted-host {parsed_url.netloc}\n"
                indexes_header += f"--extra-index-url {url}\n"

            content = indexes_header + "\n" + content

        self._output(content, cwd, output)

    def _output(self, content: str, cwd: Path, output: IO | str) -> None:
        if isinstance(output, IO):
            output.write(content)
        else:
            filepath = cwd / output
            with filepath.open("w", encoding="utf-8") as f:
                f.write(content)
