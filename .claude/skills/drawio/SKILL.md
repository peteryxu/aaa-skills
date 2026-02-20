---
name: drawio
description: Create, read, and modify draw.io diagrams including AWS/Azure/GCP architecture, flowcharts, ERDs, network diagrams, and sequence diagrams. Outputs XML, Mermaid, and CSV formats. Use when creating diagrams, generating architecture diagrams, visualizing infrastructure, making flowcharts, or modifying .drawio files.
allowed-tools: Bash(python:*), Read, Write, Grep, Glob
---

# draw.io Diagram Skill

## 1. Overview

This skill creates, reads, and modifies draw.io diagrams using `drawio_tool.py`.

**Three output formats:**
- **XML (.drawio)** — Full draw.io native format with precise positioning, cloud provider icons, containers, and custom styling. Open directly in draw.io.
- **Mermaid (.mmd)** — Text-based diagram syntax for flowcharts, sequences, ERDs, Gantt charts, state machines, and class diagrams. Renders in GitHub, Confluence, and Mermaid-compatible tools.
- **CSV (.csv)** — Draw.io's CSV import format for org charts, tree structures, and hierarchical data. Import via draw.io's Arrange > Insert > Advanced > CSV.

**Script location:** `~/.claude/skills/drawio/scripts/drawio_tool.py`

## 2. Format Selection Guide

| Format | Best For | Output | When to Use |
|--------|----------|--------|-------------|
| XML | Complex layouts, precise positioning, cloud icons, custom styling | `.drawio` | AWS/Azure/GCP architecture, network diagrams, anything needing exact placement or cloud service icons |
| Mermaid | Flowcharts, sequences, ERDs, Gantt, state/class diagrams | `.mmd` | Quick diagrams, documentation-embedded diagrams, auto-layout preferred |
| CSV | Org charts, tree structures, hierarchical data | `.csv` | Reporting hierarchies, data-driven diagrams, bulk node generation |

**Decision shortcut:**
- Need cloud provider icons or precise coordinates? -> XML
- Need auto-layout or embedding in docs? -> Mermaid
- Need hierarchy from tabular data? -> CSV

## 3. Quick Start

Route based on task:

| Task | Go To |
|------|-------|
| Create new XML diagram (architecture, network, etc.) | Section 4 |
| Generate Mermaid diagram (flowchart, sequence, ERD, etc.) | Section 5 |
| Generate CSV diagram (org chart, tree) | Section 6 |
| Read/analyze existing .drawio file | Section 7 |
| Modify existing .drawio file | Section 8 |
| Use a built-in template | Section 9 |

## 4. Create XML Diagram

### Workflow

**Step 1: Identify diagram type.**
AWS architecture, Azure architecture, GCP architecture, flowchart, ERD, network topology, or sequence diagram.

**Step 2: Plan layout.**
Determine components, connections, grouping (containers/swimlanes), and layout strategy (left-to-right, top-to-bottom, grid).

**Step 3: Build JSON spec.**

```json
{
  "diagram_name": "My Architecture",
  "page_width": 1600,
  "page_height": 900,
  "nodes": [
    {
      "id": "vpc1",
      "label": "Production VPC",
      "type": "container",
      "style_preset": "aws-vpc",
      "parent": "1",
      "x": 100, "y": 100, "width": 800, "height": 600
    },
    {
      "id": "ec2_1",
      "label": "Web Server",
      "type": "aws",
      "shape": "ec2",
      "parent": "vpc1",
      "x": 50, "y": 80, "width": 60, "height": 60
    }
  ],
  "edges": [
    {
      "id": "e1",
      "source": "ec2_1",
      "target": "rds_1",
      "label": "port 3306",
      "style": "orthogonal",
      "color": "#232F3E",
      "width": 2
    }
  ]
}
```

**Step 4: Generate.**
```bash
python ~/.claude/skills/drawio/scripts/drawio_tool.py create --input spec.json --output diagram.drawio
```

**Step 5: Validate.**
Read the output file and verify node/edge counts match the spec.

### Node Types

| Type | `shape` Value | Examples |
|------|---------------|----------|
| `aws` | AWS service name without prefix | `ec2`, `lambda`, `rds`, `s3`, `dynamodb`, `cloudfront`, `api-gateway`, `sqs`, `sns` |
| `gcp` | GCP service name | `compute-engine`, `bigquery`, `cloud-storage`, `cloud-functions` |
| `azure` | Azure SVG name | `Virtual_Machine`, `SQL_Database`, `App_Service`, `Blob_Storage` |
| `container` | N/A (use `style_preset`) | `aws-vpc`, `aws-az`, `aws-subnet-public`, `aws-subnet-private-app`, `aws-subnet-private-data` |
| `basic` | General shape name | `box`, `diamond`, `circle`, `cylinder`, `cloud`, `person`, `start-end`, `table`, `server`, `router`, `switch`, `firewall` |
| `text` | N/A | Label-only text element for annotations and titles |

### Edge Styles
- `orthogonal` — Right-angle connectors (default for architecture)
- `straight` — Direct line
- `curved` — Smooth curve
- `dashed` — Dashed line (add `"dashed": true` to any style)

## 5. Generate Mermaid

Supported types: `flowchart`, `sequence`, `erd`, `gantt`, `state`, `class`

### Flowchart

```json
{
  "direction": "TD",
  "nodes": [
    {"id": "A", "label": "Start", "shape": "stadium"},
    {"id": "B", "label": "Process", "shape": "box"},
    {"id": "C", "label": "Decision?", "shape": "diamond"},
    {"id": "D", "label": "End", "shape": "stadium"}
  ],
  "edges": [
    {"source": "A", "target": "B", "style": "arrow"},
    {"source": "B", "target": "C", "style": "arrow"},
    {"source": "C", "target": "D", "label": "yes", "style": "arrow"},
    {"source": "C", "target": "B", "label": "no", "style": "dotted"}
  ]
}
```

Node shapes: `box`, `round`, `stadium`, `diamond`, `hexagon`, `parallelogram`, `circle`, `double-circle`
Edge styles: `arrow`, `dotted`, `thick`, `open`

### Sequence

```json
{
  "participants": [
    {"id": "U", "label": "User", "type": "actor"},
    {"id": "S", "label": "Server", "type": "participant"},
    {"id": "D", "label": "Database", "type": "participant"}
  ],
  "messages": [
    {"from": "U", "to": "S", "text": "HTTP Request", "type": "solid"},
    {"from": "S", "to": "D", "text": "Query", "type": "solid"},
    {"from": "D", "to": "S", "text": "Results", "type": "dashed"},
    {"from": "S", "to": "U", "text": "Response", "type": "dashed"}
  ]
}
```

Message types: `solid`, `dashed`, `async` (open arrowhead)

### ERD

```json
{
  "entities": [
    {
      "name": "User",
      "attributes": [
        {"name": "id", "type": "int", "key": "PK"},
        {"name": "email", "type": "varchar"}
      ]
    }
  ],
  "relationships": [
    {"from": "User", "to": "Order", "label": "places", "cardinality": "one-to-many"}
  ]
}
```

Cardinality: `one-to-one`, `one-to-many`, `many-to-many`, `zero-to-one`, `zero-to-many`

### Command

```bash
python ~/.claude/skills/drawio/scripts/drawio_tool.py mermaid --type flowchart --input spec.json --output diagram.mmd
```

Replace `--type` with: `flowchart`, `sequence`, `erd`, `gantt`, `state`, `class`

## 6. Generate CSV

For org charts, tree structures, and hierarchical data. Draw.io imports CSV directly via Arrange > Insert > Advanced > CSV.

### JSON Input Format

```json
{
  "label": "%name%",
  "style": "rounded=1;whiteSpace=wrap;html=1;",
  "connect": {
    "from": "manager",
    "to": "name",
    "invert": true
  },
  "layout": "auto",
  "columns": ["name", "manager", "title"],
  "data": [
    {"name": "CEO", "manager": "", "title": "Chief Executive"},
    {"name": "CTO", "manager": "CEO", "title": "Chief Technology"},
    {"name": "CFO", "manager": "CEO", "title": "Chief Financial"},
    {"name": "Dev Lead", "manager": "CTO", "title": "Development Lead"}
  ]
}
```

- `label` — Template using `%column%` placeholders
- `connect.from` — Column containing the parent reference
- `connect.to` — Column containing the node identity
- `connect.invert` — `true` means arrows point from parent to child
- `layout` — `auto`, `horizontal`, `vertical`

### Command

```bash
python ~/.claude/skills/drawio/scripts/drawio_tool.py csv --input spec.json --output diagram.csv
```

## 7. Read/Analyze Diagram

Read an existing `.drawio` file and extract its structure.

### Text Format (human-readable)

```bash
python ~/.claude/skills/drawio/scripts/drawio_tool.py read --input diagram.drawio --format text
```

Output shows:
- **Containers** — Name, bounds, child count
- **Nodes** — Label, shape type, parent container, position
- **Edges** — Source node -> Target node, label, style

### JSON Format (programmatic)

```bash
python ~/.claude/skills/drawio/scripts/drawio_tool.py read --input diagram.drawio --format json
```

Returns structured data with all node/edge properties. Use this when you need to inspect specific IDs, coordinates, or styles before modifying.

## 8. Modify Diagram

Apply add, update, and remove operations to an existing `.drawio` file.

### Operations JSON

```json
{
  "operations": [
    {
      "action": "add_node",
      "id": "new1",
      "label": "New Lambda",
      "type": "aws",
      "shape": "lambda",
      "parent": "vpc1",
      "x": 200, "y": 150, "width": 50, "height": 50
    },
    {
      "action": "add_edge",
      "id": "e_new",
      "source": "new1",
      "target": "dynamodb1",
      "label": "writes",
      "style": "orthogonal",
      "color": "#C925D1"
    },
    {
      "action": "update",
      "id": "existing_node",
      "label": "Updated Label",
      "x": 300, "y": 200
    },
    {
      "action": "remove",
      "id": "old_node"
    }
  ]
}
```

### Supported Actions

| Action | Required Fields | Optional Fields |
|--------|----------------|-----------------|
| `add_node` | `id`, `label`, `type`, `parent`, `x`, `y`, `width`, `height` | `shape`, `style_preset`, `color` |
| `add_edge` | `id`, `source`, `target` | `label`, `style`, `color`, `width`, `dashed` |
| `update` | `id` | `label`, `x`, `y`, `width`, `height`, `color` |
| `remove` | `id` | — |

### Command

```bash
python ~/.claude/skills/drawio/scripts/drawio_tool.py modify --input diagram.drawio --operations ops.json --output modified.drawio
```

Always read the diagram first (Section 7) to get existing node IDs before modifying.

## 9. Templates

### List Available Templates

```bash
python ~/.claude/skills/drawio/scripts/drawio_tool.py list-templates
```

### Built-in Templates

| Template | Description |
|----------|-------------|
| `aws-3tier` | Route53, CloudFront, ALB, EC2 (2 AZs), RDS, ElastiCache |
| `aws-serverless` | API Gateway, Lambda, DynamoDB, S3, SNS, Cognito |
| `aws-vpc` | VPC with 2 AZs, public/private/data subnets |
| `flowchart` | Start, Process, Decision, End |
| `erd` | 3-table ERD with relationships |

### Usage

```bash
python ~/.claude/skills/drawio/scripts/drawio_tool.py create --template aws-3tier --output diagram.drawio --vars region=us-west-2 app_name=MyApp
```

Template variables (`--vars`) are key=value pairs separated by spaces. They replace `${variable}` placeholders in the template.

## 10. AWS Category Colors

Quick reference for consistent AWS architecture diagrams.

| Category | Hex Color | Services |
|----------|-----------|----------|
| Compute | `#ED7100` | EC2, Lambda, Fargate, ECS, EKS, Batch |
| Networking | `#8C4FFF` | VPC, ALB, NLB, CloudFront, Route53, API Gateway, Transit Gateway |
| Database | `#C925D1` | RDS, Aurora, DynamoDB, ElastiCache, Neptune, Redshift |
| Storage | `#7AA116` | S3, EBS, EFS, FSx, Glacier |
| Security | `#DD344C` | IAM, Cognito, WAF, Shield, GuardDuty, KMS, Secrets Manager |
| App Integration | `#E7157B` | SQS, SNS, EventBridge, Step Functions |
| Management | `#E7157B` | CloudWatch, CloudTrail, Config, Systems Manager |
| General | `#232F3E` | AWS Cloud, Users, Internet, Corporate Data Center |

Container colors:
- **VPC**: `#248814` (green border)
- **AZ**: `#147EBA` (blue border)
- **Public Subnet**: `#248814` (green, lighter fill)
- **Private Subnet**: `#147EBA` (blue, lighter fill)

## 11. Critical Rules

**XML structure:**
- Every mxCell needs a unique `id` value
- Always include root cells: `id="0"` (root) and `id="1" parent="0"` (default layer)
- NEVER use `--` inside XML comments (breaks XML parsing)

**Positioning:**
- Child node coordinates are RELATIVE to their parent container
- A node at `(50, 80)` inside a container at `(100, 100)` renders at `(150, 180)` on the canvas

**Labels and escaping:**
- Use `&#xa;` for line breaks in labels
- Escape `&` as `&amp;`, `<` as `&lt;`, `>` as `&gt;` in XML attribute values

**Edges:**
- Edge `source` and `target` must reference valid vertex IDs
- Orphaned edges (referencing deleted nodes) cause rendering errors

**Validation:**
- Always read the output file after generation to verify correctness
- Check node count and edge count match your spec

## 12. Reference

Detailed reference docs are in the `reference/` directory:

- **XML format details:** [reference/xml-format.md](reference/xml-format.md)
- **AWS shapes catalog:** [reference/aws-shapes.md](reference/aws-shapes.md)
- **Azure/GCP/general shapes:** [reference/azure-gcp-shapes.md](reference/azure-gcp-shapes.md)
- **Layout patterns:** [reference/diagram-patterns.md](reference/diagram-patterns.md)
- **Mermaid & CSV formats:** [reference/mermaid-csv-formats.md](reference/mermaid-csv-formats.md)
- **Templates:** [reference/templates.md](reference/templates.md)

### List Available Shapes

```bash
python ~/.claude/skills/drawio/scripts/drawio_tool.py list-shapes --category aws
python ~/.claude/skills/drawio/scripts/drawio_tool.py list-shapes --category gcp
python ~/.claude/skills/drawio/scripts/drawio_tool.py list-shapes --category azure
python ~/.claude/skills/drawio/scripts/drawio_tool.py list-shapes --category general
```
