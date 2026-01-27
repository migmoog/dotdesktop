# dotdesktop

<p align="center">
    <img src="dotdesktop_logo.png"/>
</p>

A convenient CLI that allows users to create `.desktop` files 
with a single command.

## Examples
Minimal file creation
```bash
# run a specific executable
$ dotdesktop -e myexe
```

Provide an icon
```bash
$ dotdesktop -e myexe -i coolicon.png
```

Name the file your own way, with additional categories
```
$ dotdesktop -e myexe -n "Foo" -c Game Scientific
```
