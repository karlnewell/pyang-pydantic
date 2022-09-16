# pyang-pydantic

pyang plugin to output Pydantic models

Plugin for the [pyang](https://github.com/mbj4668/pyang) YANG parser / compiler.

## Using the plugin

1. Install [pyang](https://github.com/mbj4668/pyang) and Pydantic

    * `pip install pyang pydantic`

2. Clone / download this repository

3. `pyang -f pydantic --plugindir <.../path/to/repo/pyang-pydantic/plugins> <options> <YANG modules>`

    * `pyang -f pydantic --plugindir <.../path/to/repo/pyang-pydantic/plugins> --help` to see options

## Examples

`pyang -f pydantic --plugindir pyang-pydantic/plugins examples/turing-maching.yang`
