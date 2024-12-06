# cse412_backend
backend for the CSE 412 project.

## Populating data
`cse412.sql` contains a dump of our database with the known working schema and initial data. It is meant to be restored to a database named `cse412` for the code to access. To import it, run `psql -U <youruser> cse412 < cse412.sql`.

## Development
Install [nix](https://zero-to-nix.com/start/install) for the least pain, and run `nix develop` to get a development environment.

Otherwise, just install python and the right dependencies. This is a setuptools compliant package.

## Running
Either do `nix run`, or `python3 -m cse412_backend` once you have a suitable development environment.

## Hosting
This can be hosted in a NixOS machine by adding the flake overlay to a machine configuration and enabling the "cse412\_backend" service. You also need to populate the postgres database with the database dump and create a user named `postgres` with no password for the default config. Custom configurations are supported by editing `cse412_backend/config.py`.
