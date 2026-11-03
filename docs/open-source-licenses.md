# Open-source licensing notes

This is educational information, not legal advice. Check the exact license
text and seek qualified advice when a distribution decision has legal impact.

## GPL and copyleft

The GNU General Public License (GPL) is a family of free-software licenses
that permits use, study, modification, and redistribution subject to its
terms. GPL licenses are copyleft: when covered derivative works are
distributed, applicable source-code and license obligations generally require
the work to remain under the same GPL version or a compatible license. The
exact obligations depend on the GPL version, how components are combined, and
how the software is conveyed. GPLv3 also contains provisions addressing
patents and installation information for certain user products.

## GPL, MIT, and Apache 2.0

| License | General model | Key consideration |
| --- | --- | --- |
| GPL (for example GPLv3) | Strong copyleft | Distribution of covered derivative works carries source and same-license obligations, subject to the license terms. |
| MIT | Permissive | Redistribution, including in proprietary products, is generally allowed if the copyright and permission notice is retained. It has no explicit patent grant. |
| Apache License 2.0 | Permissive | Includes an express patent license and patent-termination terms, plus notice and attribution requirements. |

These are not interchangeable summaries of every legal condition. Whether
two components can be combined depends on the exact versions, licensing,
distribution, and manner of use. Network use alone does not generally trigger
the GPL's distribution obligations; the AGPL is a separate license with
network-interaction provisions.

## Compatibility and dependencies

Projects must review both direct and transitive dependency licenses before
redistribution. Retain required notices, comply with attribution and source
availability conditions, and avoid assuming that an application's license
replaces a dependency's license. Check the license files and package metadata
for the exact dependency versions in use.

## This project's license

The repository includes an MIT `LICENSE` for the project code. This is a
permissive project-level choice; it does not relicense bundled or separately
installed dependencies. Third-party components remain subject to their own
licenses and notices. No claim is made that this project is GPL-licensed.
