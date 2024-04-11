# wherefore

A common requirement when working on an unfamiliar code base (or a previously familiar one, after the passing of time): what does this symbol mean? Where is it defined? How is it used?

Wherefore uses an existing tool such as `rg` or `ag` to search for occurrences of a symbol (with a few context lines in each case), feeds the result to GPT with a request for explanation, prints the response. ("Wherefore" sounds like it might mean *where*, but actually means *why*.)

```
usage: wherefore.py [-h] [-C CONTEXT] [-d] [-m MODEL] [-s SEARCHER]
                    name [path]

Explain the meaning of a symbol in code

positional arguments:
  name                  The symbol to search for
  path                  The path to search (default: current directory)

options:
  -h, --help            show this help message and exit
  -C CONTEXT, --context CONTEXT
                        The number of context lines to show around matches
                        (default: 5)
  -d, --dump            Also dump the searcher output
  -m MODEL, --model MODEL
                        The GPT model (default: 'gpt-3.5-turbo')
  -s SEARCHER, --searcher SEARCHER
                        The searcher tool to use (default: 'rg')
```

Requires an OpenAI API account, with the key in the environment variable `OPENAI_API_KEY`.

## C example

An example query, in the code of [the E theorem prover](https://github.com/eprover/eprover):

```
C:\wherefore> python wherefore.py OPT_ASSUME_COMPLETENESS \src\eprover
```

And the response:

The `OPT_ASSUME_COMPLETENESS` option is defined in the file `e_options.h` in the code base. It is part of a list of possible options that can be passed to the prover. Here is a snippet of the code where `OPT_ASSUME_COMPLETENESS` is defined:

```c
\src\eprover\PROVER\e_options.h:   {OPT_ASSUME_COMPLETENESS,
\src\eprover\PROVER\e_options.h-    '\0', "assume-completeness",
\src\eprover\PROVER\e_options.h-    NoArg, NULL,
\src\eprover\PROVER\e_options.h-    "There are various ways (e.g. the next few options) to configure the "
\src\eprover\PROVER\e_options.h-    "prover to be strongly incomplete in the general case. E will detect"
\src\eprover\PROVER\e_options.h-    " when such an option is selected and return corresponding exit "
```

This indicates that using the `assume-completeness` option configures the prover to be strongly incomplete in the general case.

In the file `eprover.c`, there is a case where `OPT_ASSUME_COMPLETENESS` is used:

```c
\src\eprover\PROVER\eprover.c:      case OPT_ASSUME_COMPLETENESS:
\src\eprover\PROVER\eprover.c-            assume_inf_sys_complete = true;
\src\eprover\PROVER\eprover.c-            break;
```

In this context, when `OPT_ASSUME_COMPLETENESS` is encountered as an option being passed to the prover, it sets the variable `assume_inf_sys_complete` to true, which presumably triggers or enables some behavior related to assuming completeness within the prover.

Overall, `OPT_ASSUME_COMPLETENESS` seems to be an option that can be set to configure the prover to assume completeness in its reasoning, with specific effects on the behavior of the prover when solving problems.
