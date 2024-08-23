.. Ulto - An Imperative Reversible Programming Language documentation master file, created by
   sphinx-quickstart on Fri Aug 23 08:45:38 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Ulto - An Imperative Reversible Programming Language documentation
==================================================================

Ulto is a reversible programming language that allows you to perform forward and reverse computations. Unlike traditional programming languages where actions are typically irreversible and results in destructive process,  Ulto lets you undo operations, which can be extremely useful in situations where energy efficiency is key.

Key Features
------------
**Reversible Computation:** Ulto enables you to reverse the steps of your program, undoing changes to variables and state. This makes it easier to correct errors or explore different outcomes in your program.

**Imperative Style:** Ulto uses an imperative programming style, where instructions are given in a sequence, just like in languages such as Python or C. This makes it easier for developers who are familiar with these languages to learn Ulto.

**Memory Management:** Ulto includes advanced memory management, ensuring that your program uses resources efficiently, even when performing complex operations. It also features a LogStack to keep track of changes, allowing for easy reversal of actions.

**Hyrbid Evaluation:** In Ulto, you can choose between lazy evaluation, which delays computation until the result is needed, and eager evaluation, which computes results immediately. This flexibility helps you optimize performance based on your program's needs.

**Profiling and Logging:** Ulto’s runtime environment includes tools for profiling, which helps you monitor the performance and memory usage of your program. Detailed logs are kept of each step and reversal, allowing for easier debugging and analysis.

**Pruning Operations:** Ulto also supports pruning, a process that removes old or unnecessary data from the LogStack. This helps manage memory usage effectively, especially in long-running programs.

**Energy Efficient:** Ulto main motive was to be energy efficient while performing same tasks at high levels, the language offers performance through the use of hybrid compiler/interpreter approach where most operative tasks are handled by precompiled file written in C and remaining via optimised interpreter.

Getting Started
---------------
Ulto is designed to be easy to use while offering powerful features for reversible programming. Whether you're developing scientific applications or exploring new ways of computing, Ulto provides the tools you need.

To learn more about how to use Ulto, explore the modules in this documentation. You’ll find detailed information on the lexer, interpreter, semantic analyzer, and parser, as well as the core components like LogStack and memory management.




Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: Modules

   lexer
   interpreter
   semantic_analyser
   parser
   core

---

src package
===========

.. automodule:: src
   :members:
   :undoc-members:
   :show-inheritance:
