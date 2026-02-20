#!/usr/bin/env python3
"""Draw.io diagram tool: create, read, modify diagrams in XML, Mermaid, and CSV formats."""

import argparse
import json
import sys
import uuid
import xml.etree.ElementTree as ET
from xml.dom import minidom

# ---------------------------------------------------------------------------
# Shape & Color Catalogs
# ---------------------------------------------------------------------------

CATEGORY_COLORS = {
    "aws-compute": "#ED7100",
    "aws-networking": "#8C4FFF",
    "aws-database": "#C925D1",
    "aws-storage": "#7AA116",
    "aws-security": "#DD344C",
    "aws-general": "#232F3E",
    "aws-management": "#E7157B",
    "aws-analytics": "#8C4FFF",
    "aws-app-integration": "#E7157B",
    "aws-ml": "#01A88D",
    "aws-containers": "#ED7100",
    "aws-devtools": "#C7131F",
    "azure-compute": "#0078D4",
    "azure-networking": "#0078D4",
    "azure-database": "#0078D4",
    "azure-storage": "#0078D4",
    "gcp-compute": "#4285F4",
    "gcp-networking": "#4285F4",
    "gcp-database": "#4285F4",
    "gcp-storage": "#4285F4",
}

# (mxgraph shape name, category key)
SHAPE_CATALOG = {
    # AWS Compute
    "aws-ec2": ("mxgraph.aws4.instance2", "aws-compute"),
    "aws-lambda": ("mxgraph.aws4.lambda_function", "aws-compute"),
    "aws-fargate": ("mxgraph.aws4.fargate", "aws-compute"),
    "aws-batch": ("mxgraph.aws4.batch", "aws-compute"),
    "aws-lightsail": ("mxgraph.aws4.lightsail", "aws-compute"),
    "aws-beanstalk": ("mxgraph.aws4.elastic_beanstalk", "aws-compute"),
    "aws-autoscaling": ("mxgraph.aws4.auto_scaling2", "aws-compute"),
    # AWS Containers
    "aws-ecs": ("mxgraph.aws4.ecs", "aws-containers"),
    "aws-eks": ("mxgraph.aws4.eks", "aws-containers"),
    "aws-ecr": ("mxgraph.aws4.ecr", "aws-containers"),
    # AWS Networking
    "aws-vpc": ("mxgraph.aws4.virtual_private_cloud_vpc", "aws-networking"),
    "aws-igw": ("mxgraph.aws4.internet_gateway", "aws-networking"),
    "aws-nat": ("mxgraph.aws4.nat_gateway", "aws-networking"),
    "aws-route53": ("mxgraph.aws4.route_53", "aws-networking"),
    "aws-cloudfront": ("mxgraph.aws4.cloudfront", "aws-networking"),
    "aws-alb": ("mxgraph.aws4.application_load_balancer", "aws-networking"),
    "aws-nlb": ("mxgraph.aws4.network_load_balancer", "aws-networking"),
    "aws-api-gw": ("mxgraph.aws4.api_gateway", "aws-networking"),
    "aws-api-gateway": ("mxgraph.aws4.api_gateway", "aws-networking"),
    "aws-direct-connect": ("mxgraph.aws4.direct_connect", "aws-networking"),
    "aws-transit-gw": ("mxgraph.aws4.transit_gateway", "aws-networking"),
    "aws-vpn-gw": ("mxgraph.aws4.vpn_gateway", "aws-networking"),
    "aws-endpoints": ("mxgraph.aws4.endpoints", "aws-networking"),
    "aws-global-accelerator": ("mxgraph.aws4.global_accelerator", "aws-networking"),
    "aws-elb": ("mxgraph.aws4.elastic_load_balancing", "aws-networking"),
    # AWS Database
    "aws-rds": ("mxgraph.aws4.rds_instance", "aws-database"),
    "aws-aurora": ("mxgraph.aws4.aurora", "aws-database"),
    "aws-dynamodb": ("mxgraph.aws4.dynamodb", "aws-database"),
    "aws-elasticache": ("mxgraph.aws4.elasticache_cache_node", "aws-database"),
    "aws-neptune": ("mxgraph.aws4.neptune", "aws-database"),
    "aws-redshift": ("mxgraph.aws4.redshift", "aws-database"),
    "aws-documentdb": ("mxgraph.aws4.documentdb_with_mongodb_compatibility", "aws-database"),
    # AWS Storage
    "aws-s3": ("mxgraph.aws4.bucket", "aws-storage"),
    "aws-ebs": ("mxgraph.aws4.volume", "aws-storage"),
    "aws-efs": ("mxgraph.aws4.file_system", "aws-storage"),
    "aws-fsx": ("mxgraph.aws4.fsx", "aws-storage"),
    "aws-backup": ("mxgraph.aws4.backup", "aws-storage"),
    # AWS Security
    "aws-iam": ("mxgraph.aws4.iam", "aws-security"),
    "aws-cognito": ("mxgraph.aws4.cognito", "aws-security"),
    "aws-waf": ("mxgraph.aws4.waf", "aws-security"),
    "aws-shield": ("mxgraph.aws4.shield", "aws-security"),
    "aws-guardduty": ("mxgraph.aws4.guardduty", "aws-security"),
    "aws-kms": ("mxgraph.aws4.kms", "aws-security"),
    "aws-secrets-manager": ("mxgraph.aws4.secrets_manager", "aws-security"),
    "aws-acm": ("mxgraph.aws4.certificate_manager_3", "aws-security"),
    # AWS General
    "aws-users": ("mxgraph.aws4.users", "aws-general"),
    "aws-client": ("mxgraph.aws4.client", "aws-general"),
    "aws-cloud": ("mxgraph.aws4.aws_cloud", "aws-general"),
    "aws-internet": ("mxgraph.aws4.internet", "aws-general"),
    "aws-office": ("mxgraph.aws4.office_building", "aws-general"),
    "aws-mobile-client": ("mxgraph.aws4.mobile_client", "aws-general"),
    # AWS Management
    "aws-cloudwatch": ("mxgraph.aws4.cloudwatch_2", "aws-management"),
    "aws-cloudformation": ("mxgraph.aws4.cloudformation", "aws-management"),
    "aws-config": ("mxgraph.aws4.config", "aws-management"),
    "aws-cloudtrail": ("mxgraph.aws4.cloudtrail", "aws-management"),
    "aws-systems-manager": ("mxgraph.aws4.systems_manager", "aws-management"),
    # AWS App Integration
    "aws-sqs": ("mxgraph.aws4.sqs", "aws-app-integration"),
    "aws-sns": ("mxgraph.aws4.sns", "aws-app-integration"),
    "aws-ses": ("mxgraph.aws4.simple_email_service", "aws-app-integration"),
    "aws-eventbridge": ("mxgraph.aws4.eventbridge", "aws-app-integration"),
    "aws-step-functions": ("mxgraph.aws4.step_functions", "aws-app-integration"),
    # AWS Analytics
    "aws-athena": ("mxgraph.aws4.athena", "aws-analytics"),
    "aws-kinesis": ("mxgraph.aws4.kinesis", "aws-analytics"),
    "aws-glue": ("mxgraph.aws4.glue", "aws-analytics"),
    "aws-quicksight": ("mxgraph.aws4.quicksight", "aws-analytics"),
    # AWS ML
    "aws-sagemaker": ("mxgraph.aws4.sagemaker", "aws-ml"),
    "aws-bedrock": ("mxgraph.aws4.bedrock", "aws-ml"),
    "aws-rekognition": ("mxgraph.aws4.rekognition", "aws-ml"),
    # GCP
    "gcp-compute-engine": ("mxgraph.gcp2.compute_engine", "gcp-compute"),
    "gcp-cloud-functions": ("mxgraph.gcp2.cloud_functions", "gcp-compute"),
    "gcp-cloud-run": ("mxgraph.gcp2.cloud_run", "gcp-compute"),
    "gcp-gke": ("mxgraph.gcp2.google_kubernetes_engine", "gcp-compute"),
    "gcp-cloud-sql": ("mxgraph.gcp2.cloud_sql", "gcp-database"),
    "gcp-bigquery": ("mxgraph.gcp2.bigquery", "gcp-database"),
    "gcp-firestore": ("mxgraph.gcp2.firestore", "gcp-database"),
    "gcp-spanner": ("mxgraph.gcp2.spanner", "gcp-database"),
    "gcp-cloud-storage": ("mxgraph.gcp2.cloud_storage", "gcp-storage"),
    "gcp-pubsub": ("mxgraph.gcp2.cloud_pubsub", "gcp-networking"),
    "gcp-vpc": ("mxgraph.gcp2.virtual_private_cloud", "gcp-networking"),
    "gcp-cloud-cdn": ("mxgraph.gcp2.cloud_cdn", "gcp-networking"),
    "gcp-cloud-dns": ("mxgraph.gcp2.cloud_dns", "gcp-networking"),
    "gcp-load-balancing": ("mxgraph.gcp2.cloud_load_balancing", "gcp-networking"),
}

# General / flowchart shapes (style string, no category)
GENERAL_SHAPES = {
    "box": "rounded=1;whiteSpace=wrap;html=1;",
    "rect": "whiteSpace=wrap;html=1;",
    "diamond": "rhombus;whiteSpace=wrap;html=1;",
    "circle": "ellipse;whiteSpace=wrap;html=1;aspect=fixed;",
    "cylinder": "shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;",
    "cloud": "ellipse;shape=cloud;whiteSpace=wrap;html=1;",
    "document": "shape=document;whiteSpace=wrap;html=1;",
    "parallelogram": "shape=parallelogram;perimeter=parallelogramPerimeter;whiteSpace=wrap;html=1;",
    "hexagon": "shape=hexagon;perimeter=hexagonPerimeter2;whiteSpace=wrap;html=1;",
    "person": "shape=mxgraph.basic.person;whiteSpace=wrap;html=1;",
    "start-end": "rounded=1;whiteSpace=wrap;html=1;arcSize=50;",
    "table": "shape=table;startSize=30;container=1;collapsible=0;childLayout=tableLayout;fixedRows=1;rowLines=1;fontStyle=1;strokeColor=#6c8ebf;fillColor=#dae8fc;",
    # Network
    "server": "shape=mxgraph.cisco.servers.standard_server;html=1;",
    "router": "shape=mxgraph.cisco.routers.router;html=1;",
    "switch": "shape=mxgraph.cisco.switches.layer_3_switch;html=1;",
    "firewall": "shape=mxgraph.cisco.firewalls.firewall;html=1;",
    "pc": "shape=mxgraph.cisco.computers_and_peripherals.pc;html=1;",
}


# ---------------------------------------------------------------------------
# Style Builders
# ---------------------------------------------------------------------------

def build_aws_icon_style(shape_name, fill_color=None):
    """Build the standard AWS4 icon style string."""
    if fill_color is None:
        for key, (sh, cat) in SHAPE_CATALOG.items():
            if sh == shape_name:
                fill_color = CATEGORY_COLORS.get(cat, "#232F3E")
                break
        else:
            fill_color = "#232F3E"
    return (
        f"outlineConnect=0;fontColor=#232F3E;gradientColor=none;"
        f"fillColor={fill_color};strokeColor=none;dashed=0;"
        f"verticalLabelPosition=bottom;verticalAlign=top;align=center;"
        f"html=1;fontSize=10;fontStyle=0;aspect=fixed;pointerEvents=1;"
        f"shape={shape_name};"
    )


def build_container_style(fill_color="#E8F5E9", stroke_color="#388E3C",
                           start_size=30, dashed=False):
    """Build a swimlane container style (VPC, AZ, Subnet)."""
    style = (
        f"swimlane;startSize={start_size};fillColor={fill_color};"
        f"strokeColor={stroke_color};fontStyle=1;fontSize=14;"
        f"rounded=1;arcSize=8;swimlaneLine=0;"
    )
    if dashed:
        style += "strokeDashArray=8 8;"
    return style


def build_basic_style(shape="box", fill="#FFFFFF", stroke="#000000",
                       font_size=12, font_color="#000000", **kwargs):
    """Build a style for general/flowchart shapes."""
    base = GENERAL_SHAPES.get(shape, GENERAL_SHAPES["box"])
    style = f"{base}fillColor={fill};strokeColor={stroke};fontSize={font_size};fontColor={font_color};"
    for k, v in kwargs.items():
        style += f"{k}={v};"
    return style


def build_edge_style(edge_type="orthogonal", color="#232F3E", width=2,
                      dashed=False, dash_pattern="8 8"):
    """Build an edge/connection style string."""
    styles = {
        "orthogonal": "edgeStyle=orthogonalEdgeStyle;",
        "elbow": "edgeStyle=elbowEdgeStyle;",
        "straight": "",
        "curved": "curved=1;",
        "entity": "edgeStyle=entityRelationEdgeStyle;",
    }
    style = styles.get(edge_type, styles["orthogonal"])
    style += f"strokeColor={color};strokeWidth={width};"
    if dashed:
        style += f"dashed=1;dashPattern={dash_pattern};"
    return style


def resolve_style(node):
    """Resolve a node's style from its spec dict."""
    # Explicit style string
    if "style" in node and isinstance(node["style"], str) and "=" in node["style"]:
        return node["style"]

    node_type = node.get("type", "basic")
    shape = node.get("shape", "box")

    if node_type == "container":
        preset = node.get("style_preset", "")
        presets = {
            "aws-vpc": ("#E8F5E9", "#388E3C", 30, False),
            "aws-az": ("#E3F2FD", "#1565C0", 25, True),
            "aws-subnet-public": ("#FFF3E0", "#E65100", 22, False),
            "aws-subnet-private-app": ("#FCE4EC", "#C62828", 22, False),
            "aws-subnet-private-data": ("#F3E5F5", "#6A1B9A", 22, False),
        }
        if preset in presets:
            return build_container_style(*presets[preset])
        return build_container_style(
            fill_color=node.get("fill", "#E8F5E9"),
            stroke_color=node.get("stroke", "#388E3C"),
            start_size=node.get("start_size", 30),
            dashed=node.get("dashed", False),
        )

    if node_type == "aws":
        preset = node.get("style_preset", "")
        if preset in SHAPE_CATALOG:
            mxshape, cat = SHAPE_CATALOG[preset]
            return build_aws_icon_style(mxshape, node.get("fill"))
        catalog_key = f"aws-{shape}"
        if catalog_key in SHAPE_CATALOG:
            mxshape, cat = SHAPE_CATALOG[catalog_key]
            return build_aws_icon_style(mxshape, node.get("fill"))
        # Try direct shape name
        return build_aws_icon_style(f"mxgraph.aws4.{shape}", node.get("fill"))

    if node_type == "gcp":
        preset = node.get("style_preset", "")
        if preset in SHAPE_CATALOG:
            mxshape, cat = SHAPE_CATALOG[preset]
            return build_aws_icon_style(mxshape, CATEGORY_COLORS.get(cat, "#4285F4"))
        catalog_key = f"gcp-{shape}"
        if catalog_key in SHAPE_CATALOG:
            mxshape, cat = SHAPE_CATALOG[catalog_key]
            return build_aws_icon_style(mxshape, CATEGORY_COLORS.get(cat, "#4285F4"))
        return build_aws_icon_style(f"mxgraph.gcp2.{shape}", node.get("fill", "#4285F4"))

    if node_type == "azure":
        return (
            f"shape=image;aspect=fixed;image=img/lib/mscae/{shape}.svg;"
            f"fillColor=none;strokeColor=none;"
        )

    if node_type == "text":
        return (
            f"text;html=1;align=center;verticalAlign=middle;"
            f"fontSize={node.get('font_size', 13)};fontStyle={node.get('font_style', 1)};"
            f"fontColor={node.get('font_color', '#000000')};fillColor=none;strokeColor=none;"
        )

    # General / basic shapes
    return build_basic_style(
        shape=shape,
        fill=node.get("fill", "#FFFFFF"),
        stroke=node.get("stroke", "#000000"),
        font_size=node.get("font_size", 12),
        font_color=node.get("font_color", "#000000"),
    )


def resolve_edge_style(edge):
    """Resolve an edge's style from its spec dict."""
    if "style" in edge and isinstance(edge["style"], str) and "=" in edge["style"]:
        return edge["style"]
    return build_edge_style(
        edge_type=edge.get("style", "orthogonal"),
        color=edge.get("color", "#232F3E"),
        width=edge.get("width", 2),
        dashed=edge.get("dashed", False),
        dash_pattern=edge.get("dash_pattern", "8 8"),
    )


# ---------------------------------------------------------------------------
# XML Generation
# ---------------------------------------------------------------------------

def create_mxfile(diagram_name="Page-1", page_width=1600, page_height=900):
    """Create the skeleton mxfile XML tree."""
    mxfile = ET.Element("mxfile", host="drawio-skill")
    diagram = ET.SubElement(mxfile, "diagram", name=diagram_name, id=_uid())
    model = ET.SubElement(diagram, "mxGraphModel",
                          dx="1326", dy="843", grid="1", gridSize="10",
                          guides="1", tooltips="1", connect="1", arrows="1",
                          fold="1", page="1", pageScale="1",
                          pageWidth=str(page_width), pageHeight=str(page_height),
                          math="0", shadow="0")
    root = ET.SubElement(model, "root")
    ET.SubElement(root, "mxCell", id="0")
    ET.SubElement(root, "mxCell", id="1", parent="0")
    return mxfile, root


def add_vertex(root, cell_id, value, style, parent="1", x=0, y=0, w=120, h=60):
    """Append a vertex mxCell to root."""
    cell = ET.SubElement(root, "mxCell",
                         id=cell_id, value=value, style=style,
                         parent=parent, vertex="1")
    ET.SubElement(cell, "mxGeometry",
                  x=str(x), y=str(y), width=str(w), height=str(h),
                  **{"as": "geometry"})
    return cell


def add_edge(root, cell_id, source, target, style, value="", parent="1"):
    """Append an edge mxCell to root."""
    attrs = dict(id=cell_id, style=style, parent=parent, edge="1")
    if source:
        attrs["source"] = source
    if target:
        attrs["target"] = target
    if value:
        attrs["value"] = value
    cell = ET.SubElement(root, "mxCell", **attrs)
    geo = ET.SubElement(cell, "mxGeometry", relative="1", **{"as": "geometry"})
    return cell


def _uid():
    return uuid.uuid4().hex[:12]


def pretty_xml(element):
    """Return pretty-printed XML string."""
    rough = ET.tostring(element, encoding="unicode")
    dom = minidom.parseString(rough)
    lines = dom.toprettyxml(indent="    ").split("\n")
    # Remove the XML declaration line
    return "\n".join(line for line in lines if not line.startswith("<?xml"))


# ---------------------------------------------------------------------------
# Create from JSON spec
# ---------------------------------------------------------------------------

def cmd_create(args):
    """Create a new .drawio diagram from a JSON spec or template."""
    if args.template:
        return cmd_create_template(args)

    with open(args.input) as f:
        spec = json.load(f)

    name = spec.get("diagram_name", "Page-1")
    pw = spec.get("page_width", 1600)
    ph = spec.get("page_height", 900)

    mxfile, root = create_mxfile(name, pw, ph)

    for node in spec.get("nodes", []):
        style = resolve_style(node)
        add_vertex(root, node["id"], node.get("label", ""),
                   style, parent=node.get("parent", "1"),
                   x=node.get("x", 0), y=node.get("y", 0),
                   w=node.get("width", 120), h=node.get("height", 60))

    for edge in spec.get("edges", []):
        style = resolve_edge_style(edge)
        add_edge(root, edge["id"], edge.get("source", ""),
                 edge.get("target", ""), style,
                 value=edge.get("label", ""),
                 parent=edge.get("parent", "1"))

    xml_str = pretty_xml(mxfile)
    with open(args.output, "w") as f:
        f.write(xml_str)
    print(f"Created {args.output}")


# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

def create_aws_3tier(**vars):
    """Generate AWS 3-tier architecture diagram."""
    mxfile, root = create_mxfile("AWS 3-Tier Architecture", 1600, 900)
    region = vars.get("region", "us-east-1")
    app = vars.get("app_name", "Application")

    # External
    add_vertex(root, "users", "Users", build_aws_icon_style("mxgraph.aws4.users", "#232F3E"),
               x=80, y=27, w=55, h=55)
    add_vertex(root, "r53", "Route 53", build_aws_icon_style("mxgraph.aws4.route_53"),
               x=300, y=30, w=50, h=50)
    add_vertex(root, "cf", f"CloudFront\nDistribution",
               build_aws_icon_style("mxgraph.aws4.cloudfront"), x=530, y=30, w=50, h=50)
    add_vertex(root, "igw", f"Internet\nGateway",
               build_aws_icon_style("mxgraph.aws4.internet_gateway"), x=775, y=30, w=50, h=50)
    add_vertex(root, "s3", f"S3 Bucket\n(Static Assets)",
               build_aws_icon_style("mxgraph.aws4.bucket", "#3F8624"), x=1030, y=30, w=50, h=50)

    # VPC
    add_vertex(root, "vpc", f"VPC (10.0.0.0/16)",
               build_container_style("#E8F5E9", "#388E3C"), x=120, y=100, w=1360, h=740)

    # AZs
    for i, (az_id, az_x, az_label) in enumerate([
        ("az1", 30, f"Availability Zone 1 ({region}a)"),
        ("az2", 690, f"Availability Zone 2 ({region}b)"),
    ]):
        add_vertex(root, az_id, az_label,
                   build_container_style("#E3F2FD", "#1565C0", 25, dashed=True),
                   parent="vpc", x=az_x, y=50, w=620, h=660)

        pub_id = f"pubsub{i+1}"
        add_vertex(root, pub_id, f"Public Subnet (10.0.{i+1}.0/24)",
                   build_container_style("#FFF3E0", "#E65100", 22),
                   parent=az_id, x=20, y=40, w=580, h=150)

        add_vertex(root, f"nat{i+1}", "NAT Gateway",
                   build_aws_icon_style("mxgraph.aws4.nat_gateway"),
                   parent=pub_id, x=40, y=40, w=50, h=50)
        add_vertex(root, f"alb{i+1}", f"Application\nLoad Balancer",
                   build_aws_icon_style("mxgraph.aws4.application_load_balancer"),
                   parent=pub_id, x=250, y=35, w=60, h=60)

        app_sub_id = f"privsub_app{i+1}"
        x_offset = 70 if i == 1 else 20
        add_vertex(root, app_sub_id, f"Private Subnet - App (10.0.{i+3}.0/24)",
                   build_container_style("#FCE4EC", "#C62828", 22),
                   parent=az_id, x=x_offset, y=220, w=580, h=170)

        for j, ec2_x in enumerate([160, 370]):
            add_vertex(root, f"ec2_{i+1}{chr(97+j)}", f"EC2 Instance\n(App Server)",
                       build_aws_icon_style("mxgraph.aws4.instance2"),
                       parent=app_sub_id, x=ec2_x, y=40, w=48, h=48)
        add_vertex(root, f"asg{i+1}", "Auto Scaling Group",
                   "text;html=1;strokeColor=#ED7100;fillColor=none;align=center;verticalAlign=middle;"
                   "whiteSpace=wrap;rounded=1;dashed=1;dashPattern=8 8;fontSize=10;fontColor=#ED7100;",
                   parent=app_sub_id, x=130, y=105, w=320, h=25)

        db_sub_id = f"privsub_db{i+1}"
        add_vertex(root, db_sub_id, f"Private Subnet - Data (10.0.{i+5}.0/24)",
                   build_container_style("#F3E5F5", "#6A1B9A", 22),
                   parent=az_id, x=20, y=420, w=580, h=210)

        rds_label = "RDS Primary\n(MySQL/PostgreSQL)" if i == 0 else "RDS Standby\n(Multi-AZ)"
        add_vertex(root, f"rds{i+1}", rds_label,
                   build_aws_icon_style("mxgraph.aws4.rds_instance"),
                   parent=db_sub_id, x=140, y=40, w=48, h=48)

        cache_label = "ElastiCache\n(Redis)" if i == 0 else "ElastiCache\nReplica"
        add_vertex(root, f"cache{i+1}", cache_label,
                   build_aws_icon_style("mxgraph.aws4.elasticache_cache_node"),
                   parent=db_sub_id, x=380, y=40, w=48, h=48)

    # Tier labels
    for label, y, color in [
        ("PRESENTATION TIER", 170, "#E65100"),
        ("APPLICATION TIER", 370, "#C62828"),
        ("DATA TIER", 570, "#6A1B9A"),
    ]:
        add_vertex(root, _uid(), label,
                   f"text;html=1;align=center;verticalAlign=middle;fontSize=13;"
                   f"fontStyle=1;fontColor={color};fillColor=none;strokeColor=none;",
                   x=1500, y=y, w=60, h=120)

    # Edges
    edges = [
        ("e1", "users", "r53", "#232F3E"), ("e2", "r53", "cf", "#232F3E"),
        ("e3", "cf", "igw", "#232F3E"),
        ("e4", "igw", "alb1", "#8C4FFF"), ("e5", "igw", "alb2", "#8C4FFF"),
        ("e6", "alb1", "ec2_1a", "#ED7100"), ("e7", "alb1", "ec2_1b", "#ED7100"),
        ("e8", "alb2", "ec2_2a", "#ED7100"), ("e9", "alb2", "ec2_2b", "#ED7100"),
        ("e10", "ec2_1a", "rds1", "#C925D1"), ("e11", "ec2_1b", "cache1", "#C925D1"),
        ("e12", "ec2_2a", "rds2", "#C925D1"), ("e13", "ec2_2b", "cache2", "#C925D1"),
    ]
    for eid, src, tgt, color in edges:
        add_edge(root, eid, src, tgt, build_edge_style(color=color))

    # Dashed S3 edge
    add_edge(root, "e3b", "cf", "s3",
             build_edge_style(color="#3F8624", dashed=True))

    # Replication edges
    add_edge(root, "e14", "rds1", "rds2",
             build_edge_style(color="#C925D1", dashed=True), value="Sync Replication")
    add_edge(root, "e15", "cache1", "cache2",
             build_edge_style(color="#C925D1", dashed=True), value="Replication")

    return mxfile


def create_flowchart(**vars):
    """Generate a simple flowchart template."""
    mxfile, root = create_mxfile("Flowchart", 800, 600)
    title = vars.get("title", "Process Flow")

    nodes = [
        ("start", "Start", "start-end", 300, 40, 120, 40, "#d5e8d4", "#82b366"),
        ("process1", "Process Step", "box", 280, 130, 160, 60, "#dae8fc", "#6c8ebf"),
        ("decision", "Decision?", "diamond", 290, 240, 140, 80, "#fff2cc", "#d6b656"),
        ("process2", "Yes Path", "box", 120, 380, 140, 60, "#dae8fc", "#6c8ebf"),
        ("end", "End", "start-end", 480, 380, 120, 40, "#f8cecc", "#b85450"),
    ]
    for nid, label, shape, x, y, w, h, fill, stroke in nodes:
        add_vertex(root, nid, label, build_basic_style(shape, fill, stroke), x=x, y=y, w=w, h=h)

    edges = [
        ("e1", "start", "process1", ""), ("e2", "process1", "decision", ""),
        ("e3", "decision", "process2", "Yes"), ("e4", "decision", "end", "No"),
        ("e5", "process2", "end", ""),
    ]
    for eid, src, tgt, label in edges:
        add_edge(root, eid, src, tgt, build_edge_style(), value=label)

    return mxfile


def create_erd(**vars):
    """Generate a simple ERD template with 3 tables."""
    mxfile, root = create_mxfile("ERD", 1000, 600)

    tables = [
        ("users_tbl", "Users", 100, 100, 200, 160,
         ["id (PK)", "name", "email", "created_at"]),
        ("orders_tbl", "Orders", 400, 100, 200, 180,
         ["id (PK)", "user_id (FK)", "total", "status", "created_at"]),
        ("products_tbl", "Products", 700, 100, 200, 160,
         ["id (PK)", "name", "price", "stock"]),
    ]

    for tid, title, x, y, w, h, columns in tables:
        # Table header
        add_vertex(root, tid, title,
                   "shape=table;startSize=30;container=1;collapsible=0;childLayout=tableLayout;"
                   "fixedRows=1;rowLines=1;fontStyle=1;strokeColor=#6c8ebf;fillColor=#dae8fc;",
                   x=x, y=y, w=w, h=h)
        # Rows
        for i, col in enumerate(columns):
            row_style = ("text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;"
                         "spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;whiteSpace=wrap;html=1;")
            add_vertex(root, f"{tid}_r{i}", col, row_style,
                       parent=tid, x=0, y=30 + i * 30, w=w, h=30)

    # Relationships
    add_edge(root, "rel1", "users_tbl", "orders_tbl",
             build_edge_style("entity", "#6c8ebf"), value="1:N")
    add_edge(root, "rel2", "orders_tbl", "products_tbl",
             build_edge_style("entity", "#6c8ebf"), value="N:M")

    return mxfile


def create_aws_vpc(**vars):
    """Generate an AWS VPC diagram with 2 AZs and subnets."""
    mxfile, root = create_mxfile("AWS VPC", 1200, 700)
    region = vars.get("region", "us-east-1")

    add_vertex(root, "igw", "Internet\nGateway",
               build_aws_icon_style("mxgraph.aws4.internet_gateway"), x=550, y=20, w=50, h=50)
    add_vertex(root, "vpc", f"VPC (10.0.0.0/16)",
               build_container_style("#E8F5E9", "#388E3C"), x=50, y=90, w=1100, h=560)

    for i, az_x in enumerate([30, 560]):
        az_id = f"az{i+1}"
        add_vertex(root, az_id, f"AZ {region}{chr(97+i)}",
                   build_container_style("#E3F2FD", "#1565C0", 25, dashed=True),
                   parent="vpc", x=az_x, y=40, w=500, h=490)

        add_vertex(root, f"pub{i+1}", f"Public Subnet (10.0.{i*2+1}.0/24)",
                   build_container_style("#FFF3E0", "#E65100", 22),
                   parent=az_id, x=20, y=40, w=460, h=130)
        add_vertex(root, f"nat{i+1}", "NAT GW",
                   build_aws_icon_style("mxgraph.aws4.nat_gateway"),
                   parent=f"pub{i+1}", x=200, y=40, w=48, h=48)

        add_vertex(root, f"priv{i+1}", f"Private Subnet (10.0.{i*2+2}.0/24)",
                   build_container_style("#FCE4EC", "#C62828", 22),
                   parent=az_id, x=20, y=200, w=460, h=130)

        add_vertex(root, f"data{i+1}", f"Data Subnet (10.0.{i*2+10}.0/24)",
                   build_container_style("#F3E5F5", "#6A1B9A", 22),
                   parent=az_id, x=20, y=360, w=460, h=110)

    add_edge(root, "e_igw_pub1", "igw", "pub1", build_edge_style(color="#8C4FFF"))
    add_edge(root, "e_igw_pub2", "igw", "pub2", build_edge_style(color="#8C4FFF"))

    return mxfile


def create_aws_serverless(**vars):
    """Generate an AWS serverless architecture diagram."""
    mxfile, root = create_mxfile("AWS Serverless", 1200, 600)

    nodes = [
        ("users", "Users", "aws-users", 50, 220, 55, 55),
        ("cognito", "Cognito", "aws-cognito", 200, 220, 50, 50),
        ("apigw", "API Gateway", "aws-api-gw", 370, 220, 50, 50),
        ("lambda1", "Lambda\n(API)", "aws-lambda", 550, 120, 50, 50),
        ("lambda2", "Lambda\n(Worker)", "aws-lambda", 550, 320, 50, 50),
        ("dynamo", "DynamoDB", "aws-dynamodb", 750, 120, 50, 50),
        ("s3", "S3 Bucket", "aws-s3", 750, 320, 50, 50),
        ("sns", "SNS", "aws-sns", 950, 220, 50, 50),
    ]
    for nid, label, shape_key, x, y, w, h in nodes:
        cat_key = shape_key
        if cat_key in SHAPE_CATALOG:
            mxshape, cat = SHAPE_CATALOG[cat_key]
            style = build_aws_icon_style(mxshape)
        else:
            style = build_aws_icon_style(f"mxgraph.aws4.{shape_key}", "#232F3E")
        add_vertex(root, nid, label, style, x=x, y=y, w=w, h=h)

    edges = [
        ("e1", "users", "cognito"), ("e2", "cognito", "apigw"),
        ("e3", "apigw", "lambda1"), ("e4", "apigw", "lambda2"),
        ("e5", "lambda1", "dynamo"), ("e6", "lambda2", "s3"),
        ("e7", "lambda1", "sns"), ("e8", "lambda2", "sns"),
    ]
    for eid, src, tgt in edges:
        add_edge(root, eid, src, tgt, build_edge_style(color="#232F3E"))

    return mxfile


TEMPLATES = {
    "aws-3tier": ("AWS 3-tier architecture (Route53, CloudFront, ALB, EC2, RDS, ElastiCache)", create_aws_3tier),
    "aws-serverless": ("AWS serverless (API Gateway, Lambda, DynamoDB, S3, SNS, Cognito)", create_aws_serverless),
    "aws-vpc": ("AWS VPC with 2 AZs, public/private/data subnets, NAT, IGW", create_aws_vpc),
    "flowchart": ("Simple flowchart: Start, Process, Decision, End", create_flowchart),
    "erd": ("3-table ERD with relationships", create_erd),
}


def cmd_create_template(args):
    """Create diagram from a named template."""
    name = args.template
    if name not in TEMPLATES:
        print(f"Unknown template: {name}")
        print(f"Available: {', '.join(TEMPLATES.keys())}")
        sys.exit(1)

    kvars = {}
    if args.vars:
        for item in args.vars:
            k, v = item.split("=", 1)
            kvars[k] = v

    _, fn = TEMPLATES[name]
    mxfile = fn(**kvars)
    xml_str = pretty_xml(mxfile)
    with open(args.output, "w") as f:
        f.write(xml_str)
    print(f"Created {args.output} from template '{name}'")


# ---------------------------------------------------------------------------
# Read / Analyze
# ---------------------------------------------------------------------------

def read_diagram(filepath):
    """Parse a .drawio file and return structured data."""
    tree = ET.parse(filepath)
    mxfile = tree.getroot()
    pages = []
    for diagram in mxfile.findall("diagram"):
        model = diagram.find("mxGraphModel")
        if model is None:
            continue
        root_elem = model.find("root")
        if root_elem is None:
            continue

        nodes, edges, containers = [], [], []
        for cell in root_elem.findall("mxCell"):
            cid = cell.get("id", "")
            if cid in ("0", "1"):
                continue

            style = cell.get("style", "")
            value = cell.get("value", "")
            parent = cell.get("parent", "1")

            if cell.get("edge") == "1":
                edges.append({
                    "id": cid, "label": value,
                    "source": cell.get("source", ""),
                    "target": cell.get("target", ""),
                    "style": style,
                })
            elif cell.get("vertex") == "1":
                geo = cell.find("mxGeometry")
                entry = {
                    "id": cid, "label": value.replace("&#xa;", "\n"),
                    "parent": parent, "style": style,
                }
                if geo is not None:
                    entry.update({
                        "x": float(geo.get("x", 0)),
                        "y": float(geo.get("y", 0)),
                        "width": float(geo.get("width", 0)),
                        "height": float(geo.get("height", 0)),
                    })
                if "swimlane" in style:
                    containers.append(entry)
                else:
                    nodes.append(entry)

        pages.append({
            "name": diagram.get("name", ""),
            "nodes": nodes,
            "edges": edges,
            "containers": containers,
            "page_width": model.get("pageWidth", ""),
            "page_height": model.get("pageHeight", ""),
        })
    return {"pages": pages}


def summarize_diagram(data):
    """Return a human-readable summary."""
    lines = []
    for i, page in enumerate(data["pages"]):
        lines.append(f"Page: {page['name']} ({page['page_width']}x{page['page_height']})")
        lines.append(f"  Containers: {len(page['containers'])}")
        for c in page["containers"]:
            lines.append(f"    - {c['id']}: {c['label']}")
        lines.append(f"  Nodes: {len(page['nodes'])}")
        for n in page["nodes"]:
            shape = ""
            if "shape=" in n.get("style", ""):
                for part in n["style"].split(";"):
                    if part.startswith("shape="):
                        shape = f" [{part.split('=',1)[1]}]"
            lines.append(f"    - {n['id']}: {n['label']}{shape} (parent={n['parent']})")
        lines.append(f"  Edges: {len(page['edges'])}")
        for e in page["edges"]:
            label = f" '{e['label']}'" if e.get("label") else ""
            lines.append(f"    - {e['id']}: {e['source']} -> {e['target']}{label}")
    return "\n".join(lines)


def cmd_read(args):
    """Read and summarize a .drawio file."""
    data = read_diagram(args.input)
    if args.format == "json":
        print(json.dumps(data, indent=2))
    else:
        print(summarize_diagram(data))


# ---------------------------------------------------------------------------
# Modify
# ---------------------------------------------------------------------------

def cmd_modify(args):
    """Modify an existing .drawio file based on operations JSON."""
    tree = ET.parse(args.input)
    mxfile = tree.getroot()
    model = mxfile.find(".//mxGraphModel")
    root_elem = model.find("root")

    with open(args.operations) as f:
        ops = json.load(f)

    for op in ops.get("operations", []):
        action = op.get("action")

        if action == "add_node":
            style = resolve_style(op)
            add_vertex(root_elem, op["id"], op.get("label", ""),
                       style, parent=op.get("parent", "1"),
                       x=op.get("x", 0), y=op.get("y", 0),
                       w=op.get("width", 120), h=op.get("height", 60))

        elif action == "add_edge":
            style = resolve_edge_style(op)
            add_edge(root_elem, op["id"], op.get("source", ""),
                     op.get("target", ""), style,
                     value=op.get("label", ""))

        elif action == "remove":
            target_id = op["id"]
            for cell in root_elem.findall("mxCell"):
                if cell.get("id") == target_id:
                    root_elem.remove(cell)
                    break
            # Also remove edges connected to removed node
            for cell in list(root_elem.findall("mxCell")):
                if cell.get("source") == target_id or cell.get("target") == target_id:
                    root_elem.remove(cell)

        elif action == "update":
            target_id = op["id"]
            for cell in root_elem.findall("mxCell"):
                if cell.get("id") == target_id:
                    if "label" in op:
                        cell.set("value", op["label"])
                    if "style" in op:
                        cell.set("style", op["style"])
                    if "x" in op or "y" in op or "width" in op or "height" in op:
                        geo = cell.find("mxGeometry")
                        if geo is not None:
                            for attr in ("x", "y", "width", "height"):
                                if attr in op:
                                    geo.set(attr, str(op[attr]))
                    break

    xml_str = pretty_xml(mxfile)
    with open(args.output, "w") as f:
        f.write(xml_str)
    print(f"Modified diagram saved to {args.output}")


# ---------------------------------------------------------------------------
# Mermaid Generation
# ---------------------------------------------------------------------------

def cmd_mermaid(args):
    """Generate Mermaid syntax from a JSON spec."""
    with open(args.input) as f:
        spec = json.load(f)

    dtype = args.type
    lines = []

    if dtype == "flowchart":
        direction = spec.get("direction", "TD")
        lines.append(f"graph {direction}")
        for node in spec.get("nodes", []):
            nid = node["id"]
            label = node.get("label", nid)
            shape = node.get("shape", "box")
            shapes = {
                "box": (f"[{label}]"),
                "round": (f"({label})"),
                "diamond": (f"{{{label}}}"),
                "circle": (f"(({label}))"),
                "stadium": (f"([{label}])"),
                "hexagon": (f"{{{{{label}}}}}"),
                "parallelogram": (f"[/{label}/]"),
                "cylinder": (f"[({label})]"),
            }
            lines.append(f"    {nid}{shapes.get(shape, f'[{label}]')}")
        for edge in spec.get("edges", []):
            src = edge["source"]
            tgt = edge["target"]
            label = edge.get("label", "")
            style = edge.get("style", "arrow")
            arrows = {"arrow": "-->", "dotted": "-.->", "thick": "==>", "none": "---"}
            arrow = arrows.get(style, "-->")
            if label:
                lines.append(f"    {src} {arrow}|{label}| {tgt}")
            else:
                lines.append(f"    {src} {arrow} {tgt}")

    elif dtype == "sequence":
        lines.append("sequenceDiagram")
        for participant in spec.get("participants", []):
            pid = participant.get("id", participant.get("name", ""))
            label = participant.get("label", pid)
            lines.append(f"    participant {pid} as {label}")
        for msg in spec.get("messages", []):
            src = msg["from"]
            tgt = msg["to"]
            text = msg.get("text", "")
            mtype = msg.get("type", "solid")
            arrows = {"solid": "->>", "dotted": "-->>", "solid_open": "->", "dotted_open": "-->"}
            arrow = arrows.get(mtype, "->>")
            lines.append(f"    {src}{arrow}{tgt}: {text}")
            if msg.get("activate"):
                lines.append(f"    activate {tgt}")
            if msg.get("deactivate"):
                lines.append(f"    deactivate {msg['deactivate']}")

    elif dtype == "erd":
        lines.append("erDiagram")
        for entity in spec.get("entities", []):
            eid = entity["id"]
            for attr in entity.get("attributes", []):
                atype = attr.get("type", "string")
                aname = attr.get("name", "")
                constraint = attr.get("constraint", "")
                if constraint:
                    lines.append(f"    {eid} {{{atype} {aname} {constraint}}}")
                else:
                    lines.append(f"    {eid} {{{atype} {aname}}}")
        for rel in spec.get("relationships", []):
            src = rel["from"]
            tgt = rel["to"]
            label = rel.get("label", "")
            card = rel.get("cardinality", "||--o{")
            lines.append(f"    {src} {card} {tgt} : \"{label}\"")

    elif dtype == "gantt":
        lines.append("gantt")
        lines.append(f"    title {spec.get('title', 'Project Schedule')}")
        lines.append(f"    dateFormat {spec.get('date_format', 'YYYY-MM-DD')}")
        for section in spec.get("sections", []):
            lines.append(f"    section {section['name']}")
            for task in section.get("tasks", []):
                status = task.get("status", "")
                after = task.get("after", "")
                duration = task.get("duration", "")
                start = task.get("start", "")
                parts = [task["name"], "  :"]
                if status:
                    parts.append(f"{status},")
                parts.append(f"{task.get('id', '')},")
                if after:
                    parts.append(f"after {after},")
                elif start:
                    parts.append(f"{start},")
                parts.append(duration)
                lines.append(f"    {''.join(parts)}")

    elif dtype == "state":
        lines.append("stateDiagram-v2")
        for state in spec.get("states", []):
            sid = state["id"]
            label = state.get("label", sid)
            if label != sid:
                lines.append(f"    {sid} : {label}")
        for transition in spec.get("transitions", []):
            src = transition.get("from", "[*]")
            tgt = transition.get("to", "[*]")
            label = transition.get("label", "")
            if label:
                lines.append(f"    {src} --> {tgt} : {label}")
            else:
                lines.append(f"    {src} --> {tgt}")

    elif dtype == "class":
        lines.append("classDiagram")
        for cls in spec.get("classes", []):
            cid = cls["id"]
            for attr in cls.get("attributes", []):
                lines.append(f"    {cid} : {attr}")
            for method in cls.get("methods", []):
                lines.append(f"    {cid} : {method}")
        for rel in spec.get("relationships", []):
            src = rel["from"]
            tgt = rel["to"]
            rtype = rel.get("type", "-->")
            label = rel.get("label", "")
            if label:
                lines.append(f"    {src} {rtype} {tgt} : {label}")
            else:
                lines.append(f"    {src} {rtype} {tgt}")

    else:
        print(f"Unknown mermaid type: {dtype}")
        print("Available: flowchart, sequence, erd, gantt, state, class")
        sys.exit(1)

    output = "\n".join(lines) + "\n"
    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Mermaid diagram saved to {args.output}")
    else:
        print(output)


# ---------------------------------------------------------------------------
# CSV Generation (draw.io import format)
# ---------------------------------------------------------------------------

def cmd_csv(args):
    """Generate draw.io CSV import format from a JSON spec."""
    with open(args.input) as f:
        spec = json.load(f)

    lines = []

    # Header directives
    label_tmpl = spec.get("label", "%name%")
    lines.append(f"# label: {label_tmpl}")

    style = spec.get("style", "rounded=1;whiteSpace=wrap;html=1;")
    lines.append(f"# style: {style}")

    if "connect" in spec:
        conn = spec["connect"]
        lines.append(f'# connect: {json.dumps(conn)}')

    layout = spec.get("layout", "auto")
    lines.append(f"# layout: {layout}")

    if "width" in spec:
        lines.append(f"# width: {spec['width']}")
    if "height" in spec:
        lines.append(f"# height: {spec['height']}")
    if "padding" in spec:
        lines.append(f"# padding: {spec['padding']}")
    if "ignore" in spec:
        lines.append(f"# ignore: {spec['ignore']}")

    lines.append("")

    # Column headers
    columns = spec.get("columns", [])
    if columns:
        lines.append(",".join(columns))
    elif spec.get("data"):
        columns = list(spec["data"][0].keys())
        lines.append(",".join(columns))

    # Data rows
    for row in spec.get("data", []):
        if isinstance(row, dict):
            values = [str(row.get(c, "")) for c in columns]
        else:
            values = [str(v) for v in row]
        # Quote values containing commas
        quoted = []
        for v in values:
            if "," in v or '"' in v:
                quoted.append(f'"{v}"')
            else:
                quoted.append(v)
        lines.append(",".join(quoted))

    output = "\n".join(lines) + "\n"
    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"CSV diagram saved to {args.output}")
    else:
        print(output)


# ---------------------------------------------------------------------------
# List Commands
# ---------------------------------------------------------------------------

def cmd_list_templates(args):
    """List available templates."""
    print("Available templates:")
    for name, (desc, _) in TEMPLATES.items():
        print(f"  {name:20s} {desc}")


def cmd_list_shapes(args):
    """List shapes by category."""
    cat = args.category
    if cat == "general":
        print("General / Flowchart shapes:")
        for name, style in sorted(GENERAL_SHAPES.items()):
            print(f"  {name:20s} style=\"{style}\"")
        return

    prefix = f"{cat}-"
    matches = {k: v for k, v in SHAPE_CATALOG.items() if k.startswith(prefix)}
    if not matches:
        # Try matching category key
        matches = {k: v for k, v in SHAPE_CATALOG.items() if v[1] and v[1].startswith(cat)}

    if not matches:
        print(f"No shapes found for category: {cat}")
        print(f"Available prefixes: aws, azure, gcp, general")
        return

    print(f"Shapes for '{cat}':")
    for name, (shape, category) in sorted(matches.items()):
        color = CATEGORY_COLORS.get(category, "")
        print(f"  {name:30s} shape={shape}  color={color}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Draw.io diagram tool: create, read, modify diagrams")
    sub = parser.add_subparsers(dest="command")

    # create
    p_create = sub.add_parser("create", help="Create a new diagram")
    p_create.add_argument("--input", "-i", help="JSON spec file")
    p_create.add_argument("--output", "-o", required=True, help="Output .drawio file")
    p_create.add_argument("--template", "-t", help="Template name")
    p_create.add_argument("--vars", nargs="*", help="Template variables (key=value)")

    # read
    p_read = sub.add_parser("read", help="Read and summarize a diagram")
    p_read.add_argument("--input", "-i", required=True, help="Input .drawio file")
    p_read.add_argument("--format", "-f", choices=["text", "json"], default="text")

    # modify
    p_modify = sub.add_parser("modify", help="Modify an existing diagram")
    p_modify.add_argument("--input", "-i", required=True, help="Input .drawio file")
    p_modify.add_argument("--operations", required=True, help="Operations JSON file")
    p_modify.add_argument("--output", "-o", required=True, help="Output .drawio file")

    # mermaid
    p_mermaid = sub.add_parser("mermaid", help="Generate Mermaid syntax")
    p_mermaid.add_argument("--type", "-t", required=True,
                           choices=["flowchart", "sequence", "erd", "gantt", "state", "class"])
    p_mermaid.add_argument("--input", "-i", required=True, help="JSON spec file")
    p_mermaid.add_argument("--output", "-o", help="Output .mmd file (stdout if omitted)")

    # csv
    p_csv = sub.add_parser("csv", help="Generate draw.io CSV import format")
    p_csv.add_argument("--input", "-i", required=True, help="JSON spec file")
    p_csv.add_argument("--output", "-o", help="Output .csv file (stdout if omitted)")

    # list-templates
    sub.add_parser("list-templates", help="List available templates")

    # list-shapes
    p_shapes = sub.add_parser("list-shapes", help="List shapes by category")
    p_shapes.add_argument("--category", "-c", required=True,
                          help="Category: aws, gcp, azure, general, or specific like aws-compute")

    args = parser.parse_args()

    commands = {
        "create": cmd_create,
        "read": cmd_read,
        "modify": cmd_modify,
        "mermaid": cmd_mermaid,
        "csv": cmd_csv,
        "list-templates": cmd_list_templates,
        "list-shapes": cmd_list_shapes,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
