# Documentation

You can view the latest documentation at the [`lum-ai/clu-processors` website](https://lum.ai/clu-processors/docs/).

## General Documentation

We use `mkdocs` to generate our site documentation from markdown. Markdown source files are located under the `docs` directory. To develop the documentation with live updates use the following command:

```bash
docker run --rm -it -v $PWD:/app \
    -p 8000:8000 \
    parsertongue/mkdocs:latest \
    mkdocs serve -a 0.0.0.0:8000
```

Open your browser to [localhost:8000](http://localhost:80000).
