# Template Catalog

## Available Templates

| Template         | Description                                                        | Nodes | Layout       |
|------------------|--------------------------------------------------------------------|-------|--------------|
| `aws-3tier`      | AWS 3-tier architecture with Route53, CloudFront, ALB, EC2, RDS    | 25+   | Swimlane     |
| `aws-serverless` | AWS serverless with API Gateway, Lambda, DynamoDB, S3, SNS         | 8     | Left-to-right|
| `aws-vpc`        | AWS VPC with 2 AZs, public/private/data subnets, NAT, IGW         | 15    | Swimlane     |
| `flowchart`      | Simple flowchart: Start, Process, Decision, End                    | 5     | Top-to-bottom|
| `erd`            | 3-table ERD (Users, Orders, Products) with relationships           | 3     | Entity-relation|

---

## aws-3tier

Full AWS 3-tier web architecture across 2 Availability Zones.

**Components:**
- External: Users, Route 53, CloudFront, Internet Gateway, S3 (static assets)
- VPC container with 2 AZs, each containing:
  - Public Subnet: NAT Gateway + Application Load Balancer
  - App Subnet: 2x EC2 instances with Auto Scaling Group label
  - Data Subnet: RDS instance + ElastiCache node
- Replication edges between AZ1/AZ2 databases
- Tier labels on the right margin

**Variables:**

| Variable   | Default       | Description              |
|------------|---------------|--------------------------|
| `region`   | `us-east-1`   | AWS region for AZ labels |
| `app_name` | `Application`  | Application name         |

**Example:**
```bash
python3 drawio_tool.py create --template aws-3tier --output arch.drawio --vars region=eu-west-1 app_name=MyApp
```

**Page size:** 1600 x 900

---

## aws-serverless

Serverless architecture showing request flow from users through API Gateway and Lambda to data stores.

**Components:**
- Users -> Cognito -> API Gateway
- API Gateway fans out to 2 Lambda functions (API + Worker)
- Lambda API -> DynamoDB
- Lambda Worker -> S3
- Both Lambdas -> SNS

**Variables:** None (uses defaults)

**Example:**
```bash
python3 drawio_tool.py create --template aws-serverless --output serverless.drawio
```

**Page size:** 1200 x 600

---

## aws-vpc

VPC networking diagram focused on subnet layout.

**Components:**
- Internet Gateway (external)
- VPC container (10.0.0.0/16) with 2 AZs
- Each AZ contains:
  - Public Subnet with NAT Gateway
  - Private Subnet
  - Data Subnet
- Edges from IGW to both public subnets

**Variables:**

| Variable | Default     | Description              |
|----------|-------------|--------------------------|
| `region` | `us-east-1` | AWS region for AZ labels |

**Example:**
```bash
python3 drawio_tool.py create --template aws-vpc --output vpc.drawio --vars region=ap-southeast-1
```

**Page size:** 1200 x 700

---

## flowchart

Basic process flowchart with decision branching.

**Components:**
- Start (green pill) -> Process Step (blue box) -> Decision (yellow diamond)
- Decision branches: Yes -> Yes Path (blue box), No -> End (red pill)
- Yes Path -> End

**Variables:**

| Variable | Default        | Description    |
|----------|----------------|----------------|
| `title`  | `Process Flow` | Diagram title  |

**Example:**
```bash
python3 drawio_tool.py create --template flowchart --output flow.drawio --vars title="Deploy Process"
```

**Page size:** 800 x 600

---

## erd

Entity-Relationship Diagram with 3 tables and relationships.

**Components:**
- Users table: id (PK), name, email, created_at
- Orders table: id (PK), user_id (FK), total, status, created_at
- Products table: id (PK), name, price, stock
- Relationships: Users 1:N Orders, Orders N:M Products
- Uses table shape with row-based layout
- Entity-relation edge style

**Variables:** None

**Example:**
```bash
python3 drawio_tool.py create --template erd --output schema.drawio
```

**Page size:** 1000 x 600

---

## Creating Custom Templates

Templates are defined as Python functions in `drawio_tool.py`. Each function:
1. Calls `create_mxfile(name, width, height)` to get the XML skeleton
2. Uses `add_vertex()` and `add_edge()` to build the diagram
3. Uses style builder functions: `build_aws_icon_style()`, `build_container_style()`, `build_basic_style()`, `build_edge_style()`
4. Returns the `mxfile` element

Register new templates in the `TEMPLATES` dict:
```python
TEMPLATES = {
    "my-template": ("Description text", create_my_template_function),
}
```

Template functions accept `**vars` for user-customizable parameters passed via `--vars key=value`.
