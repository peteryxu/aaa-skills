# Diagram Layout Patterns and Sizing

## Grid Layout

Best for: service inventories, icon grids, comparison charts.

- Horizontal spacing: 150px between column centers
- Vertical spacing: 120px between row centers
- Formula: `x = margin + col * spacing_x`, `y = margin + row * spacing_y`
- Typical margin: 60-80px

```
x = 80 + col * 150
y = 80 + row * 120
```

## Hierarchical (Top-to-Bottom)

Best for: org charts, dependency trees, flowcharts.

- Levels spaced 150-200px vertically
- Nodes centered horizontally within their level
- Decision diamonds need extra vertical space (80px tall vs 60px)

## Left-to-Right Flow

Best for: data pipelines, request flows, serverless architectures.

- External actors on the far left
- Processing/compute in the middle
- Data stores on the far right
- Horizontal spacing: 170-200px between columns

## Swimlane Containers (AWS VPC Pattern)

Best for: AWS architecture, network diagrams with zones.

Nesting hierarchy: VPC > AZ > Subnet > Resources

### Reference Layout (from aws-3tier template)

```
VPC Container:          x=120,  y=100,  w=1360,  h=740
  AZ1:                  x=30,   y=50,   w=620,   h=660   (relative to VPC)
    Public Subnet:      x=20,   y=40,   w=580,   h=150   (relative to AZ1)
    App Subnet:         x=20,   y=220,  w=580,   h=170   (relative to AZ1)
    Data Subnet:        x=20,   y=420,  w=580,   h=210   (relative to AZ1)
  AZ2:                  x=690,  y=50,   w=620,   h=660   (relative to VPC)
    Public Subnet:      x=20,   y=40,   w=580,   h=150   (relative to AZ2)
    App Subnet:         x=70,   y=220,  w=580,   h=170   (relative to AZ2)
    Data Subnet:        x=20,   y=420,  w=580,   h=210   (relative to AZ2)
```

Key spacing rules:
- Container-to-child padding: 20-30px on sides, 40-50px from top (below header)
- Vertical gap between subnets: ~30px
- AZ gap from each other: ~40px (690 - 30 - 620 = 40)
- Icons inside subnets: 40px from top of subnet, spaced 150-200px apart

## Sizing Reference

| Element              | Width     | Height    | Notes                          |
|----------------------|-----------|-----------|--------------------------------|
| AWS icon             | 48-60     | 48-60     | `aspect=fixed`, use 50 default |
| Flowchart box        | 120-160   | 60        | Wider for long labels          |
| Decision diamond     | 140       | 80        | Needs extra space for text     |
| Start/End terminal   | 120       | 40        | Pill shape                     |
| Text label (tier)    | 60-120    | 80-120    | No border, rotated sometimes   |
| Container (small)    | 300       | 200       | Single service group           |
| Container (subnet)   | 460-580   | 110-210   | Depends on content count       |
| Container (AZ)       | 500-620   | 490-660   | Depends on subnet count        |
| Container (VPC)      | 1100-1400 | 560-740   | Depends on AZ count            |
| Page (standard)      | 1600      | 900       | 16:9 aspect ratio              |
| Page (wide)          | 1920      | 1080      | Full HD equivalent             |
| Page (tall)          | 1200      | 1600      | Portrait for flowcharts        |

## Edge Routing

| Style                  | Use Case                  | Width | Color     |
|------------------------|---------------------------|-------|-----------|
| `orthogonalEdgeStyle`  | Default, clean right-angles | 2   | varies    |
| `elbowEdgeStyle`       | Simple L-shaped routes    | 2     | varies    |
| `curved=1`             | Organic / informal        | 2     | varies    |
| `entityRelationEdgeStyle` | ERD relationships      | 1     | `#6c8ebf` |
| Straight (no edgeStyle)| Direct point-to-point     | 2     | varies    |

### Color coding for edges

| Flow Type        | Color     | Style         |
|------------------|-----------|---------------|
| Main traffic     | `#232F3E` | solid, width=2 |
| Networking       | `#8C4FFF` | solid, width=2 |
| Compute          | `#ED7100` | solid, width=2 |
| Data             | `#C925D1` | solid, width=2 |
| Storage          | `#3F8624` | dashed         |
| Replication      | `#C925D1` | dashed         |
| Secondary        | `#999999` | solid, width=1 |

### Edge label placement

- Use `value="Label"` on the mxCell for edge labels
- Labels auto-center on the edge midpoint
- For replication/sync labels, use dashed edges with descriptive text
