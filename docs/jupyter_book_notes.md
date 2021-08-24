<!-- :orphan: is needed so we don't get a TOC warning -->
```{eval-rst}
:orphan:
```

# Jupyter Book Notes


## Orphan pages

Add the following to the top of a file to avoid getting a warning
if the page isn't included in the main TOC:

````md
```{eval-rst}
:orphan:
```
````

## RHS or Secondary Sidebar expansion

TODO: I'd like these sections to expand automatically; waiting on https://github.com/executablebooks/sphinx-book-theme/issues/383


## Admonition Options

```{note}
note
```

```{attention}
attention
```

```{caution}
caution
```

```{warning}
warning
```

```{danger}
danger
```


```{error}
error
```


```{hint}
hint
```


```{important}
important
```

```{tip}
tip
```


### Custom admonitions

```{admonition} Custom!
admonition
```

```{admonition} TODO
todo
```

More customization: https://github.com/executablebooks/jupyter-book/issues/1345
