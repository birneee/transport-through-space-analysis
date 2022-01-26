> all qlog files are gzipped, otherwise they would exceed the 100MB file size limit of GitHub

## Unzipping all QLOG Files
```bash
find . -name '*.qlog.gz' -exec gunzip -k {} \;
```

## Zipping all QLOG Files
```bash
find . -name '*.qlog' -exec gzip -k {} \;
```

## Deleting all Unzipped QLOG Files
```bash
find . -name '*.qlog' -exec rm -rf {} \;
```