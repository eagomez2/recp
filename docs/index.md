# Welcome to recp
`recp` (short for recipe) is a tool designed to automate processes that involve executing multiple sequential command-line steps. A recipe is defined in a `.yaml` file, which outlines the steps to be performed. Each step can include a tags, description, a set of environment variables to be set for that step, and one or more commands to be executed. Additionally, commands can be preprocessed, allowing a single instruction to be expanded into multiple commands, thereby eliminating the need for tedious repeated and error-prone manual steps or scripts lacking flexibility.

A single recipe `.yaml` file can define multiple steps, which can be selected or filtered based on the task at hand. This flexibility allows you to execute only a subset of a larger recipe when needed. The `--dry-run` option enables generating the commands without actually running them, allowing you to verify that everything works as expected before executing time-consuming processes.

## Guides
To begin using `recp`, refer to the guides below:

- [Installation](install.md)
- [Quickstart](quickstart.md)

For a more detailed description of individual features, see the [Reference](reference.md) section.
