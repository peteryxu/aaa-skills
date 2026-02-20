# Draw.io XML Format Reference

## File Structure

```xml
<mxfile host="drawio-skill">
  <diagram name="Page-1" id="unique-id">
    <mxGraphModel dx="1326" dy="843" grid="1" gridSize="10"
                  guides="1" tooltips="1" connect="1" arrows="1"
                  fold="1" page="1" pageScale="1"
                  pageWidth="1600" pageHeight="900"
                  math="0" shadow="0">
      <root>
        <mxCell id="0"/>              <!-- root layer (required) -->
        <mxCell id="1" parent="0"/>   <!-- default parent (required) -->
        <!-- all vertices and edges go here -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## mxGraphModel Attributes

| Attribute  | Typical Value | Description                         |
|------------|---------------|-------------------------------------|
| dx         | 1326          | Horizontal scroll offset            |
| dy         | 843           | Vertical scroll offset              |
| grid       | 1             | Show grid (0/1)                     |
| gridSize   | 10            | Grid snap size in pixels            |
| guides     | 1             | Show alignment guides               |
| tooltips   | 1             | Show tooltips on hover              |
| connect    | 1             | Allow connections                   |
| arrows     | 1             | Show arrows on edges                |
| fold       | 1             | Allow container collapse            |
| page       | 1             | Show page boundary                  |
| pageScale  | 1             | Page zoom scale                     |
| pageWidth  | 1600          | Page width in pixels                |
| pageHeight | 900           | Page height in pixels               |
| math       | 0             | Enable LaTeX math rendering         |
| shadow     | 0             | Global shadow on shapes             |

## mxCell: Vertex (Shape/Node)

```xml
<mxCell id="node1" value="Label Text" style="rounded=1;whiteSpace=wrap;html=1;"
        parent="1" vertex="1">
  <mxGeometry x="100" y="200" width="120" height="60" as="geometry"/>
</mxCell>
```

**Required attributes:**
- `id` -- unique string identifier
- `vertex="1"` -- marks this as a shape (not an edge)
- `parent` -- id of parent cell ("1" for top-level, container id for nested)

**Optional attributes:**
- `value` -- label text (HTML allowed when `html=1` in style)
- `style` -- semicolon-separated style string

**mxGeometry for vertices:**
- `x`, `y` -- position (absolute if parent="1", relative to container otherwise)
- `width`, `height` -- dimensions in pixels

## mxCell: Edge (Connection/Arrow)

```xml
<mxCell id="edge1" style="edgeStyle=orthogonalEdgeStyle;strokeColor=#232F3E;"
        parent="1" edge="1" source="node1" target="node2" value="">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

**Required attributes:**
- `id` -- unique string identifier
- `edge="1"` -- marks this as a connection
- `parent` -- usually "1"

**Optional attributes:**
- `source` -- id of source vertex
- `target` -- id of target vertex
- `value` -- edge label text

**mxGeometry for edges:**
- `relative="1"` -- always set for edges
- Can contain `<mxPoint>` children for waypoints

## mxCell: Container (Swimlane)

Containers are vertices with `swimlane` in their style. Children reference the container's id as their `parent`. Child coordinates are RELATIVE to the container's top-left corner.

```xml
<!-- Container -->
<mxCell id="vpc" value="VPC" style="swimlane;startSize=30;fillColor=#E8F5E9;"
        parent="1" vertex="1">
  <mxGeometry x="120" y="100" width="1360" height="740" as="geometry"/>
</mxCell>

<!-- Child inside container -- x,y relative to vpc's top-left -->
<mxCell id="az1" value="AZ 1" style="swimlane;startSize=25;"
        parent="vpc" vertex="1">
  <mxGeometry x="30" y="50" width="620" height="660" as="geometry"/>
</mxCell>
```

**Key rule:** When a node has `parent="vpc"`, its x=30 means 30px from the LEFT edge of the VPC container, not from the page origin.

## Style String Format

Styles are semicolon-separated `key=value` pairs. This is NOT CSS.

```
rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;
```

### Common Style Keys

| Key                    | Values / Example     | Description                          |
|------------------------|----------------------|--------------------------------------|
| `shape`                | `mxgraph.aws4.ec2`  | Shape stencil identifier             |
| `rounded`              | 0, 1                 | Rounded corners                      |
| `whiteSpace`           | `wrap`               | Enable text wrapping                 |
| `html`                 | 1                    | Enable HTML in labels                |
| `fillColor`            | `#dae8fc`            | Background fill color                |
| `strokeColor`          | `#6c8ebf`            | Border color                         |
| `fontColor`            | `#232F3E`            | Text color                           |
| `fontSize`             | 10, 12, 14           | Font size in points                  |
| `fontStyle`            | 0=normal, 1=bold, 2=italic, 3=bold+italic | Font style bitmask |
| `align`                | left, center, right  | Horizontal text alignment            |
| `verticalAlign`        | top, middle, bottom  | Vertical text alignment              |
| `verticalLabelPosition` | bottom, top, middle | Label position relative to shape     |
| `aspect`               | `fixed`              | Lock aspect ratio                    |
| `strokeWidth`          | 1, 2, 3              | Border thickness                     |
| `dashed`               | 0, 1                 | Dashed border                        |
| `dashPattern`          | `8 8`                | Dash pattern (space-separated)       |
| `opacity`              | 0-100                | Transparency                         |
| `swimlane`             | (presence)           | Marks as container                   |
| `startSize`            | 22, 25, 30           | Container header height              |
| `container`            | 1                    | Explicitly mark as container         |
| `collapsible`          | 0, 1                 | Allow collapse                       |
| `edgeStyle`            | orthogonalEdgeStyle, elbowEdgeStyle, entityRelationEdgeStyle | Edge routing |
| `curved`               | 1                    | Curved edges                         |
| `gradientColor`        | `none`, hex          | Gradient second color                |
| `outlineConnect`       | 0                    | Disable outline connect points       |
| `pointerEvents`        | 1                    | Enable mouse events on shape         |
| `arcSize`              | 8, 50                | Corner radius (with rounded=1)       |

## Multi-Page Diagrams

Multiple `<diagram>` elements inside `<mxfile>`:

```xml
<mxfile>
  <diagram name="Overview" id="page1">
    <mxGraphModel>...</mxGraphModel>
  </diagram>
  <diagram name="Detail" id="page2">
    <mxGraphModel>...</mxGraphModel>
  </diagram>
</mxfile>
```

## Value Encoding

- Newlines in labels: `&#xa;` (e.g., `value="Line 1&#xa;Line 2"`)
- Standard XML escaping: `&amp;` `&lt;` `&gt;` `&quot;`
- HTML in labels (when `html=1`): `<br>`, `<b>`, `<i>`, `<font color="...">` are supported
