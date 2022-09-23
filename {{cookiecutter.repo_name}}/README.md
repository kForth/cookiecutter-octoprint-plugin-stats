# {{cookiecutter.repo_name}}
Github Pages site tracking my OctoPrint plugin statistics over time.

## Want to use this to track your own stats? Feel free!
And I'll even give you a little how-to. After forking this repository:

1. Delete the stats file, `data/stats.json`
2. Edit the target `PLUGIN_AUTHOR` in the `scripts/get_data.py` file, [here](https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.repo_name}}/blob/main/scripts/get_data.py#L14)
3. Run the script, either using the Github action (manually triggered) or via `python scripts/get_data.py` to generate the initial data
4. Update the name mapping in the `static/js/name-map.js` file [here](https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.repo_name}}/blob/main/static/js/name_map.js), 
mapping plugin id to human readable name.
5. Update the links in `_includes/navbar.html` & the name in `index.html` to your own ones, not mine!
6. Make sure you have enabled the actions in repository settings. Last time I checked actions were disabled for forks by default.

That should be all, if you have any questions let me know!
