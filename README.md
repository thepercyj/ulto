# Ulto
A imperative reversible programming language developed in Python.

### Objectives
The language is a proof of concept for showcasing reversibility nature in a software approach despite not having a deterministic hardware to develop upon. Still the language is developed as an inspiration of Landauer's principle of how minimal heat dissipations can be achieved with efficient programming language. The features set are as follows:
- The language can perform basic arithmetic operations, can perform some conditional operators such as if-else and while loops. ( more features such as efficient data structures and more constructs can be added in the future releases)
- The reversible function has been instilled with logstack + pruning operations to efficiently manage memory pools and track assignments.
- custom malloc has been programmed to limit programs to 50 mb ( this limit is set based on the requirements at the moment and also depending on balancing space complexity to profile energy)
- hybrid approach has been introduced for evaluations (i.e. lazy and eager ). based on the nature of evalutations if it cross the threshold (i.e. which is hardcoded at the moment to balance overhead costs and be precise enough to find hotspots) and also to address circular dependencies when using loops with variables that have dependency on their own.
- batch profiling has been added for better caching during runtime and also to avoid excess overhead.
- still havent found the right balance whether to use garbage collection as it introduces a greater overhead than the previous performance counters. yet to be decided for the program. ( will keep it as a future work )
- The language is still in development phase so errors are expected.

# Installation Guide

### Step 1  
Clone the package in your local directory.

```markdown
git clone https://github.com/thepercyj/ulto
```
### Step 2
Move inside the directory

```markdown
cd ulto
```
### Step 3 
Install using setup.py 
```markdown
python setup.py install
```
** OR **

Can install from dist file as well.
```markdown
pip install dist/ulto-1.0.0-py3-none-any.whl
```

### Uninstalling Ulto
The following script will uninstall necessary packages and dependencies of ulto from your system. There will be some files left which you need to manually delete later.

```markdown
python uninstaller.py
```
