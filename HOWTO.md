# How to maintain the GROK toolkit versions page

The [GROK toolkit version configuration page](./README.md) and the linked
version and requirements files are built from a special branch of the
[groktoolkit GitHub repository](https://github.com/zopefoundation/groktoolkit).

```bash
  $ git clone -b gh-pages git@github.com:zopefoundation/groktoolkit
  $ cd groktoolkit
  $ ./build_indexes.sh
  $ git add README.md releases/
  $ git commit -m "Add new GROK toolkit release(s)."
  $ git push origin gh-pages
```

The end result is available at https://zopefoundation.github.io/groktoolkit/.
