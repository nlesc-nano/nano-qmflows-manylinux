"""Argparse-related utilities."""

from __future__ import annotations

import argparse
import textwrap
from collections.abc import Sequence
from typing import Any, ClassVar

__all__ = ["LicenseAction"]


class LicenseAction(argparse.Action):
    """Custom action for displaying license info."""

    LICENSE: ClassVar[str] = textwrap.dedent(
        """
        Copyright 2022-2023 Nanomaterial Simulation Packages (https://github.com/nlesc-nano)

        Licensed under the GNU Lesser General Public License v3 (the "License");
        you may not use this file except in compliance with the License.
        You may obtain a copy of the License at

            https://www.gnu.org/licenses/gpl-3.0.en.html
            https://www.gnu.org/licenses/lgpl-3.0.en.html

        Unless required by applicable law or agreed to in writing, software
        distributed under the License is distributed on an "AS IS" BASIS,
        WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
        See the License for the specific language governing permissions and
        limitations under the License.
    """)

    def __init__(
        self,
        option_strings: Sequence[str],
        dest: str = argparse.SUPPRESS,
        default: str | None = argparse.SUPPRESS,
        help: str = "show program's license and exit",
    ) -> None:
        """Initialize the instance."""
        super().__init__(
            option_strings=option_strings,
            dest=dest,
            default=default,
            nargs=0,
            help=help,
        )

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: str | Sequence[Any] | None,
        option_string: str | None = None,
    ) -> None:
        """Execute the action."""
        print(self.LICENSE)
        parser.exit()
