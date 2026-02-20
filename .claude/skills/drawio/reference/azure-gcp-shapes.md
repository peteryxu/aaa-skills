# Azure, GCP, and General Shapes

## Azure Shapes

Azure icons use image-based SVG references. No fill color needed -- the SVG contains the icon art.

### Style Template

```
shape=image;aspect=fixed;image=img/lib/mscae/{SERVICE}.svg;fillColor=none;strokeColor=none;
```

### Common Azure Services

| Tool Key                | Image Path (SERVICE)              | Description                |
|-------------------------|-----------------------------------|----------------------------|
| `azure-vm`              | `Virtual_Machine`                 | Virtual Machine            |
| `azure-app-service`     | `App_Service`                     | App Service                |
| `azure-sql`             | `SQL_Database`                    | SQL Database               |
| `azure-storage`         | `Storage_Accounts`                | Storage Accounts           |
| `azure-functions`       | `Function_Apps`                   | Function Apps              |
| `azure-cosmos`          | `Azure_Cosmos_DB`                 | Cosmos DB                  |
| `azure-keyvault`        | `Key_Vaults`                      | Key Vault                  |
| `azure-vnet`            | `Virtual_Network`                 | Virtual Network            |
| `azure-aks`             | `Azure_Kubernetes_Service`        | AKS                        |
| `azure-devops`          | `Azure_DevOps`                    | Azure DevOps               |
| `azure-monitor`         | `Azure_Monitor`                   | Azure Monitor              |
| `azure-lb`              | `Load_Balancers`                  | Load Balancer              |
| `azure-firewall`        | `Azure_Firewall`                  | Azure Firewall             |
| `azure-app-gw`          | `Application_Gateways`            | Application Gateway        |
| `azure-redis`           | `Azure_Cache_for_Redis`           | Azure Cache for Redis      |
| `azure-container`       | `Container_Instances`             | Container Instances        |
| `azure-logic-apps`      | `Logic_Apps`                      | Logic Apps                 |
| `azure-event-hub`       | `Event_Hubs`                      | Event Hubs                 |
| `azure-service-bus`     | `Service_Bus`                     | Service Bus                |
| `azure-blob`            | `Blob_Storage`                    | Blob Storage               |

### Azure Style Example

```xml
<mxCell id="vm1" value="Web Server"
        style="shape=image;aspect=fixed;image=img/lib/mscae/Virtual_Machine.svg;fillColor=none;strokeColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="50" height="50" as="geometry"/>
</mxCell>
```

### Azure Category Colors (for containers/grouping)

Use these for Azure resource group or subscription containers if needed:

| Element           | Color     |
|-------------------|-----------|
| Subscription      | `#0078D4` |
| Resource Group    | `#7FBA00` |
| Virtual Network   | `#0078D4` |

---

## GCP Shapes

GCP shapes use the `mxgraph.gcp2.{service}` shape library with `#4285F4` as the standard fill color.

### Style Template

```
outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#4285F4;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=10;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.gcp2.{SHAPE};
```

### Common GCP Services

| Tool Key              | Shape Name                    | Description            |
|-----------------------|-------------------------------|------------------------|
| `gcp-compute-engine`  | `compute_engine`              | Compute Engine         |
| `gcp-cloud-functions` | `cloud_functions`             | Cloud Functions        |
| `gcp-cloud-run`       | `cloud_run`                   | Cloud Run              |
| `gcp-gke`             | `google_kubernetes_engine`    | GKE                    |
| `gcp-cloud-sql`       | `cloud_sql`                   | Cloud SQL              |
| `gcp-bigquery`        | `bigquery`                    | BigQuery               |
| `gcp-firestore`       | `firestore`                   | Firestore              |
| `gcp-spanner`         | `spanner`                     | Cloud Spanner          |
| `gcp-cloud-storage`   | `cloud_storage`               | Cloud Storage          |
| `gcp-pubsub`          | `cloud_pubsub`                | Cloud Pub/Sub          |
| `gcp-vpc`             | `virtual_private_cloud`       | VPC                    |
| `gcp-cloud-cdn`       | `cloud_cdn`                   | Cloud CDN              |
| `gcp-cloud-dns`       | `cloud_dns`                   | Cloud DNS              |
| `gcp-load-balancing`  | `cloud_load_balancing`        | Cloud Load Balancing   |

### GCP Category Colors

All GCP services default to `#4285F4`. The tool maps them to sub-categories:

| Category       | Color     |
|----------------|-----------|
| gcp-compute    | `#4285F4` |
| gcp-networking | `#4285F4` |
| gcp-database   | `#4285F4` |
| gcp-storage    | `#4285F4` |

---

## General / Flowchart Shapes

Built-in shapes that don't require external stencil libraries.

| Shape Key       | Style String                                                                 | Typical Use         |
|-----------------|------------------------------------------------------------------------------|---------------------|
| `box`           | `rounded=1;whiteSpace=wrap;html=1;`                                          | Process step        |
| `rect`          | `whiteSpace=wrap;html=1;`                                                    | Generic rectangle   |
| `diamond`       | `rhombus;whiteSpace=wrap;html=1;`                                            | Decision            |
| `circle`        | `ellipse;whiteSpace=wrap;html=1;aspect=fixed;`                               | State / event       |
| `cylinder`      | `shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;` | Database       |
| `cloud`         | `ellipse;shape=cloud;whiteSpace=wrap;html=1;`                                | Cloud / Internet    |
| `document`      | `shape=document;whiteSpace=wrap;html=1;`                                     | Document            |
| `parallelogram` | `shape=parallelogram;perimeter=parallelogramPerimeter;whiteSpace=wrap;html=1;` | I/O               |
| `hexagon`       | `shape=hexagon;perimeter=hexagonPerimeter2;whiteSpace=wrap;html=1;`          | Preparation step    |
| `person`        | `shape=mxgraph.basic.person;whiteSpace=wrap;html=1;`                         | User / actor        |
| `start-end`     | `rounded=1;whiteSpace=wrap;html=1;arcSize=50;`                              | Terminal (pill)     |
| `table`         | `shape=table;startSize=30;container=1;collapsible=0;childLayout=tableLayout;fixedRows=1;rowLines=1;fontStyle=1;strokeColor=#6c8ebf;fillColor=#dae8fc;` | ERD table |

## Network Shapes (Cisco Library)

| Shape Key    | Style Shape                                        | Description       |
|--------------|----------------------------------------------------|-------------------|
| `server`     | `mxgraph.cisco.servers.standard_server`            | Standard server   |
| `router`     | `mxgraph.cisco.routers.router`                     | Router            |
| `switch`     | `mxgraph.cisco.switches.layer_3_switch`            | L3 Switch         |
| `firewall`   | `mxgraph.cisco.firewalls.firewall`                 | Firewall          |
| `pc`         | `mxgraph.cisco.computers_and_peripherals.pc`       | PC / Workstation  |

Network shapes use the base style: `shape={SHAPE};html=1;` plus optional `fillColor`, `strokeColor`, `fontSize`.
