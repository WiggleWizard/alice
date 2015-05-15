Installing a plugin
===================

Put all plugins in the plugin folder in the root of Alice. The plugin folder path may vary however based on how Alice's config is set up. Consult your `config.ini` for the plugin path.

Plugins usually come in a folder, named after the plugin. Ensure that the folder contains at least a `plugin.py` file, which holds all core functionality for the plugin. There may be specific instructions for installing any 3rd party software in the readme that comes with the plugin.


## Configuring

Most of the plugins that come with Alice are configurable to some degree. 3rd party plugins however may not provide configuration by default. Plugins usually come packaged with a `README.md`. Ensure that you read this file as it should provide the necessary information needed to configure that specific plugin.

Plugin configuration variables are written in `plugin_config.ini` file in the root of Alice. The file follows the INI standards of PEP8: Sections are named after the plugin's name and are enclosed with `[]`. Following each section should be that plugin's configuration variables following the `key = value` standard:

```
[plugin1_name]
key = value

[plugin2_name]
key = value
```