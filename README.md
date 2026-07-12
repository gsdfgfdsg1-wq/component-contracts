# component-contracts

A dependency-free CLI for detecting breaking API changes between component contract snapshots.

## Quick start

```bash
python contracts.py before.json after.json
```

Snapshots map component names to `props`. Each prop can declare `required`, `default`, and an allowed `values` list. The tool detects removed components and props, new required props, narrowed enums, and default changes. It returns nonzero for a major compatibility break and emits a JSON version-bump recommendation.

## Test

```bash
python -m unittest discover -v
```

## License

MIT.
