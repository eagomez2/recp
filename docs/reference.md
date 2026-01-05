## Recipe structure
A recipe file with all available fields is shown below. Each field is described afterward.


```yaml title="recipe.yaml with all available fields"
minimum_required_version: 0.1.0

recipe:
  first_step:
    tag:
      - first
    
    description: >
        Description of the first step
    
    env:
        USER_NAME: !input
            name: MY_NAME
            default: Juhani
            required: false 
    
    run:
        - echo 'Hello from $SOME_ENV_VAR
        - cmd: echo "My name is XX and today is MM"
          apply:
            - fn: date
              args:
                token: "{YEAR}"
                format: "%Y"
            - fn: replace
              args:

```
A recipe file is a `.yaml` file where:

- `minimum_required_version` is an **optional** field specifying the minimum `recp` version required to run it.
- `recipe` is the **required** root key containing the description of each step to be run.

Each step has:

- A **required** name key (`first_step`) containing the information relative to that particular step.
- An **optional** `tag` key containing a list of strings, each one corresponding to a tag that can be use to select a certain subset of steps to be run with the `--tag` option.
- An **optional** `description` key containing a string that describes that the step does. This is only for documentation purposes, and will be printed to the terminal when the recipe is run.
- An **optional** `env` key containing environmental variables to be used in that step. The environmental variables of a specific step are isolated from all other steps. To share variable across steps you can use [yaml anchors and aliases](https://support.atlassian.com/bitbucket-cloud/docs/yaml-anchors/). Additionally, environmental variables can be defined directly in the `.yaml` file, or defined by the user when running the recipe. User defined variables can be configured using the `!input` constructor that has a mandatory `name` key, and an optional `default` key to define the default value, and an optional `required` key containing a `bool` value to specify whether that variable is required or optional.
- A **required** `run` key that contains a list of the commands to be run. A command can be a `str` or a `dict` containing the `cmd` key and the `apply` key containing a list of modifiers to be applied to that command as a pre-processing step to generate one or multiple commands. Each modifier is defined by a `fn` key with the modifier function name, and an `args` key with the corresponding arguments.

A recipe can be run using:
```bash
recp run /path/to/your/recipe.yaml
```

Additionally, you can show the commands without running them with the `--dry-run` option, that can be used for debugging purposes.

```bash
recp run /path/to/your/recipe.yaml --dry-run 
```

To filter steps by tag, you can use:
```bash
recp run /path/to/your/recipe.yaml --tag first 
```

This will only collect steps containing the tag `first`. Multiple tags can be used to filter a step, in which case only steps containing all of them will be selected. 

For further options on `recp run`, you can run:
```bash
recp run --help
```

## Constructors
A recipe `.yaml` file can be created using a certain set of custom constructors to facilitate expressing your commands.

### !input constructor
The `!input` constructor allows you to introduce user variables provided through the terminal into your recipe. It is typically used in the `env` key as exemplified below.

```yaml title="input_constructor_example.yaml"
minimum_required_version: 0.1.0

recipe:
  step:
    env:
      USER_VAR: !input
        name: USER_VAR
        default: default_value
        required: false
    run:
      - "echo 'print user variable: $USER_VAR'"
```

In this case:

- `name` is a **required** key with the name of the environmental variable to be provided by the user. This name can be the same as its parent key or different.
- `default` is an **optional** key. It sets the value to use if the user does not provide the variable.
- `required` is an **optional** key. If `true`, the user must provide the variable to run the recipe.

The recipe can be run as:
```bash
USER_VAR="Juhani" recp run /path/to/input_constructor_example.yaml
```

It will result in the following output:
```bash
Using recipe '/path/to/input_constructor_example.yaml' ...
1 step(s) found
Pre-processing recipe data ...
Recipe pre-processing successfully completed
Parsing step environments ...
Step environments processing successfully completed
Pre-processing recipe commands ...
Recipe commands successfully completed
Running commands ...
[1/1] Running step 'step' ...
      Command:     echo 'print user variable: Juhani'
print user variable: Juhani
```

### !expr constructor
The `!expr` constructor allows using `python` expressions to be evaluated at runtime.

!!! warning
    This constructor uses `eval()` internally and is considered unsafe. By default, it is disabled, but you can enable it by using the `--unsafe` option when running the recipe.

This constructor can be used in any part of your recipe as follows:

```yaml title="expr_constructor_example.yaml"
minimum_required_version: 0.1.0

recipe:
  step:
    env:
      RESULT: !expr 24 * 60 * 60
    run:
      - echo 'A day has $RESULT seconds'
```

To run this recipe and enable the `!expr` constructor, you must use the `--unsafe` option
as follows:

```bash
recp run /path/to/expr_constructor_example.yaml --unsafe
```

It will result in the following output:
```bash
Using recipe '/path/to/expr_constructor_example.yaml' ...
1 step(s) found
Pre-processing recipe data ...
Recipe pre-processing successfully completed
Parsing step environments ...
Step environments processing successfully completed
Pre-processing recipe commands ...
Recipe commands successfully completed
Running commands ...
[1/1] Running step 'step' ...
      Command:     echo 'A day has 86400 seconds'
A day has 86400 seconds
```

## Modifiers
Modifiers are functions that take a command as input and transform it into one or more commands according to some logic. They can be used to write more compact recipes and to add variation or dynamic behavior to your commands.

To use a modifier, you can include then in the `run` key as follows:
```yaml title="modifier_example.yaml"
minimum_required_version: 0.1.0

recipe:
  step:
    run:
      - cmd: echo 'This message will be repeated multiple times'
        apply:
          - fn: repeat
            args:
              n: 3
```
In this case:

- The command in the `run` key is now a `dict`.
- The `apply` key contains all modifiers to be applied. It is a list where each item is a `dict` with a `fn` key (the modifier function) and an `args` key (the arguments passed to the modifier).
- When multiple modifiers are defined, they are applied sequentially: the output of one modifier becomes the input to the next.

In this example, the `repeat` modifier will be applied to the command, causing it to be run multiple times, resulting in:

```bash
Using recipe '/path/to/modifier_example.yaml' ...
1 step(s) found
Pre-processing recipe data ...
Recipe pre-processing successfully completed
Parsing step environments ...
Step environments processing successfully completed
Pre-processing recipe commands ...
Recipe commands successfully completed
Running commands ...
[1/1] Running step 'step' ...
      Command:     echo 'This message will be repeated multiple times'
This message will be repeated multiple times
      Command:     echo 'This message will be repeated multiple times'
This message will be repeated multiple times
      Command:     echo 'This message will be repeated multiple times'
This message will be repeated multiple times
```

!!! info
    Note that the commands are unwrapped before being run, thus, you can use `--dry-run` the preview the commands that will be run after all modifiers are applied.

A list of supported modifiers is provided below. You can also implement your own by adding it to the `src/recp/utils/apply.py` file.

## Recipe shortcuts
You can store frequently used recipes in a folder that `recp` reads automatically, and then refer to a recipe just by its name.

To add a new recipe shortcut this way, simply use:
```bash
recp config --add /path/to/your/custom_recipe.yaml
```

Then this recipe can be run as:
```bash
recp run custom_recipe
```

You can see the folder location and other `recp` settings by running:
```bash
recp config
```

To change the default recipes folder you can use:
```bash
recp config --set recipes.dir /path/to/your/new/recipes/folder
```