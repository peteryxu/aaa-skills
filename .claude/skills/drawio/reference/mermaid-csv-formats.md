# Mermaid and CSV Format Reference

## Mermaid JSON Schemas

The tool generates Mermaid syntax from JSON specs via `drawio_tool.py mermaid --type TYPE --input spec.json`.

### Flowchart

```json
{
  "direction": "TD",
  "nodes": [
    {"id": "A", "label": "Start", "shape": "stadium"},
    {"id": "B", "label": "Process", "shape": "box"},
    {"id": "C", "label": "Decision?", "shape": "diamond"}
  ],
  "edges": [
    {"source": "A", "target": "B", "label": "", "style": "arrow"},
    {"source": "B", "target": "C", "label": "next", "style": "dotted"}
  ]
}
```

**Direction values:** `TD` (top-down), `LR` (left-right), `BT` (bottom-top), `RL` (right-left)

**Node shapes:**

| Shape          | Mermaid Syntax  | Example             |
|----------------|-----------------|---------------------|
| `box`          | `[label]`       | `A[Process]`        |
| `round`        | `(label)`       | `A(Process)`        |
| `diamond`      | `{label}`       | `A{Decision?}`      |
| `circle`       | `((label))`     | `A((Event))`        |
| `stadium`      | `([label])`     | `A([Start])`        |
| `hexagon`      | `{{label}}`     | `A{{Prep}}`         |
| `parallelogram`| `[/label/]`     | `A[/Input/]`        |
| `cylinder`     | `[(label)]`     | `A[(Database)]`     |

**Edge styles:**

| Style     | Mermaid Arrow | Description       |
|-----------|---------------|-------------------|
| `arrow`   | `-->`         | Solid with arrow  |
| `dotted`  | `-.->`        | Dotted with arrow |
| `thick`   | `==>`         | Thick with arrow  |
| `none`    | `---`         | Solid, no arrow   |

### Sequence Diagram

```json
{
  "participants": [
    {"id": "Client", "label": "Web Client"},
    {"id": "API", "label": "API Server"},
    {"id": "DB", "label": "Database"}
  ],
  "messages": [
    {"from": "Client", "to": "API", "text": "GET /users", "type": "solid"},
    {"from": "API", "to": "DB", "text": "SELECT * FROM users", "type": "solid", "activate": true},
    {"from": "DB", "to": "API", "text": "results", "type": "dotted", "deactivate": "DB"},
    {"from": "API", "to": "Client", "text": "200 OK", "type": "dotted"}
  ]
}
```

**Message types:**

| Type          | Arrow  | Description              |
|---------------|--------|--------------------------|
| `solid`       | `->>`  | Solid line, solid head   |
| `dotted`      | `-->>`  | Dotted line, solid head  |
| `solid_open`  | `->`   | Solid line, open head    |
| `dotted_open` | `-->`  | Dotted line, open head   |

**Activation:** Set `"activate": true` to activate the target lifeline. Set `"deactivate": "participant_id"` to deactivate a lifeline.

### Entity-Relationship Diagram

```json
{
  "entities": [
    {
      "id": "USERS",
      "attributes": [
        {"type": "int", "name": "id", "constraint": "PK"},
        {"type": "string", "name": "name"},
        {"type": "string", "name": "email"}
      ]
    }
  ],
  "relationships": [
    {"from": "USERS", "to": "ORDERS", "cardinality": "||--o{", "label": "places"}
  ]
}
```

**Common cardinalities:** `||--o{` (one-to-many), `||--||` (one-to-one), `}o--o{` (many-to-many), `}|--|{` (one-or-more to one-or-more)

### Gantt Chart

```json
{
  "title": "Project Timeline",
  "date_format": "YYYY-MM-DD",
  "sections": [
    {
      "name": "Phase 1",
      "tasks": [
        {"name": "Design", "id": "t1", "start": "2026-01-01", "duration": "30d", "status": "done"},
        {"name": "Implement", "id": "t2", "after": "t1", "duration": "45d", "status": "active"}
      ]
    }
  ]
}
```

**Task fields:** `name` (required), `id`, `start` (date) or `after` (task id), `duration` (e.g. `30d`), `status` (`done`, `active`, `crit`, or empty)

### State Diagram

```json
{
  "states": [
    {"id": "Idle", "label": "Idle State"},
    {"id": "Running", "label": "Running"}
  ],
  "transitions": [
    {"from": "[*]", "to": "Idle"},
    {"from": "Idle", "to": "Running", "label": "start"},
    {"from": "Running", "to": "[*]", "label": "complete"}
  ]
}
```

Use `[*]` for start/end pseudo-states.

### Class Diagram

```json
{
  "classes": [
    {
      "id": "Animal",
      "attributes": ["+String name", "#int age"],
      "methods": ["+speak() void", "+move(int distance) void"]
    }
  ],
  "relationships": [
    {"from": "Dog", "to": "Animal", "type": "--|>", "label": "inherits"}
  ]
}
```

**Relationship types:** `--|>` (inheritance), `--*` (composition), `--o` (aggregation), `-->` (dependency), `--` (association)

---

## CSV Format (draw.io Import)

The CSV format generates draw.io's native CSV import syntax, which can be pasted into draw.io via Extras > Import CSV.

### Header Directives

Directives are comment lines starting with `#` at the top of the CSV file.

| Directive    | Description                                    | Example                                      |
|--------------|------------------------------------------------|----------------------------------------------|
| `# label:`   | Template for node labels using `%column%`      | `# label: %name%`                            |
| `# style:`   | Default style for all nodes                    | `# style: rounded=1;whiteSpace=wrap;html=1;` |
| `# connect:` | JSON defining parent-child connections         | `# connect: {"from":"parent","to":"name"}`   |
| `# layout:`  | Auto-layout algorithm                          | `# layout: auto`                             |
| `# width:`   | Default node width                             | `# width: 120`                               |
| `# height:`  | Default node height                            | `# height: 60`                               |
| `# padding:`  | Padding around labels                          | `# padding: 10`                              |
| `# ignore:`  | Columns to exclude from label/tooltip          | `# ignore: id,parent`                        |

### Connect Directive

```json
{"from": "parent_column", "to": "name_column", "invert": true, "style": "curved=1;"}
```

- `from` -- column containing the parent reference
- `to` -- column containing the value that `from` references
- `invert` -- if true, arrow points from parent to child
- `style` -- optional edge style override

### Layout Options

| Layout           | Description                                |
|------------------|--------------------------------------------|
| `auto`           | Automatic layout (default)                 |
| `tree`           | Vertical tree                              |
| `horizontaltree` | Horizontal tree                            |
| `organic`        | Force-directed organic layout              |
| `circle`         | Circular arrangement                       |

### Example: Org Chart

**JSON input:**
```json
{
  "label": "%name%<br><i>%role%</i>",
  "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;",
  "connect": {"from": "manager", "to": "name", "invert": true},
  "layout": "tree",
  "width": 160,
  "height": 60,
  "columns": ["name", "role", "manager"],
  "data": [
    {"name": "Alice", "role": "CEO", "manager": ""},
    {"name": "Bob", "role": "CTO", "manager": "Alice"},
    {"name": "Carol", "role": "VP Eng", "manager": "Bob"},
    {"name": "Dave", "role": "CFO", "manager": "Alice"}
  ]
}
```

**Generated CSV output:**
```
# label: %name%<br><i>%role%</i>
# style: rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;
# connect: {"from": "manager", "to": "name", "invert": true}
# layout: tree
# width: 160
# height: 60

name,role,manager
Alice,CEO,
Bob,CTO,Alice
Carol,VP Eng,Bob
Dave,CFO,Alice
```
