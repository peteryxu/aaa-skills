# AWS Shape Catalog

## AWS Icon Style Template

All AWS4 icons use this style pattern:

```
outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor={COLOR};strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=10;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.{SHAPE};
```

Replace `{COLOR}` with the category color and `{SHAPE}` with the shape name.

## Category Colors

| Category         | Color   | Hex       |
|------------------|---------|-----------|
| Compute          | Orange  | `#ED7100` |
| Containers       | Orange  | `#ED7100` |
| Networking       | Purple  | `#8C4FFF` |
| Database         | Purple  | `#C925D1` |
| Storage          | Green   | `#7AA116` |
| Security         | Red     | `#DD344C` |
| General          | Dark    | `#232F3E` |
| Management       | Pink    | `#E7157B` |
| App Integration  | Pink    | `#E7157B` |
| Analytics        | Purple  | `#8C4FFF` |
| ML/AI            | Teal    | `#01A88D` |
| Developer Tools  | Red     | `#C7131F` |

## Shapes by Category

### Compute (`#ED7100`)

| Tool Key        | Shape Name                | Description               |
|-----------------|---------------------------|---------------------------|
| `aws-ec2`       | `instance2`               | EC2 Instance              |
| `aws-lambda`    | `lambda_function`         | Lambda Function           |
| `aws-fargate`   | `fargate`                 | Fargate                   |
| `aws-autoscaling` | `auto_scaling2`         | Auto Scaling Group        |
| `aws-beanstalk` | `elastic_beanstalk`       | Elastic Beanstalk         |
| `aws-batch`     | `batch`                   | AWS Batch                 |
| `aws-lightsail` | `lightsail`               | Lightsail                 |

### Containers (`#ED7100`)

| Tool Key    | Shape Name | Description                     |
|-------------|------------|---------------------------------|
| `aws-ecs`   | `ecs`      | Elastic Container Service       |
| `aws-eks`   | `eks`      | Elastic Kubernetes Service      |
| `aws-ecr`   | `ecr`      | Elastic Container Registry      |

### Networking (`#8C4FFF`)

| Tool Key              | Shape Name                       | Description                |
|-----------------------|----------------------------------|----------------------------|
| `aws-vpc`             | `virtual_private_cloud_vpc`      | VPC                        |
| `aws-igw`             | `internet_gateway`               | Internet Gateway           |
| `aws-nat`             | `nat_gateway`                    | NAT Gateway                |
| `aws-route53`         | `route_53`                       | Route 53                   |
| `aws-cloudfront`      | `cloudfront`                     | CloudFront                 |
| `aws-alb`             | `application_load_balancer`      | Application Load Balancer  |
| `aws-nlb`             | `network_load_balancer`          | Network Load Balancer      |
| `aws-elb`             | `elastic_load_balancing`         | Classic Load Balancer      |
| `aws-api-gw`          | `api_gateway`                    | API Gateway                |
| `aws-direct-connect`  | `direct_connect`                 | Direct Connect             |
| `aws-transit-gw`      | `transit_gateway`                | Transit Gateway            |
| `aws-vpn-gw`          | `vpn_gateway`                    | VPN Gateway                |
| `aws-endpoints`       | `endpoints`                      | VPC Endpoints              |
| `aws-global-accelerator` | `global_accelerator`          | Global Accelerator         |

### Database (`#C925D1`)

| Tool Key          | Shape Name                              | Description          |
|-------------------|-----------------------------------------|----------------------|
| `aws-rds`         | `rds_instance`                          | RDS Instance         |
| `aws-aurora`      | `aurora`                                | Aurora               |
| `aws-dynamodb`    | `dynamodb`                              | DynamoDB             |
| `aws-elasticache` | `elasticache_cache_node`                | ElastiCache          |
| `aws-neptune`     | `neptune`                               | Neptune              |
| `aws-redshift`    | `redshift`                              | Redshift             |
| `aws-documentdb`  | `documentdb_with_mongodb_compatibility` | DocumentDB           |

### Storage (`#7AA116`)

| Tool Key     | Shape Name    | Description       |
|--------------|---------------|-------------------|
| `aws-s3`     | `bucket`      | S3 Bucket         |
| `aws-ebs`    | `volume`      | EBS Volume        |
| `aws-efs`    | `file_system` | EFS File System   |
| `aws-fsx`    | `fsx`         | FSx               |
| `aws-backup` | `backup`      | AWS Backup        |

### Security (`#DD344C`)

| Tool Key              | Shape Name              | Description           |
|-----------------------|-------------------------|-----------------------|
| `aws-iam`             | `iam`                   | IAM                   |
| `aws-cognito`         | `cognito`               | Cognito               |
| `aws-waf`             | `waf`                   | WAF                   |
| `aws-shield`          | `shield`                | Shield                |
| `aws-guardduty`       | `guardduty`             | GuardDuty             |
| `aws-kms`             | `kms`                   | KMS                   |
| `aws-secrets-manager` | `secrets_manager`       | Secrets Manager       |
| `aws-acm`             | `certificate_manager_3` | Certificate Manager   |

### General (`#232F3E`)

| Tool Key      | Shape Name        | Description      |
|---------------|-------------------|------------------|
| `aws-users`   | `users`           | Users            |
| `aws-cloud`   | `aws_cloud`       | AWS Cloud        |
| `aws-internet`| `internet`        | Internet globe   |
| `aws-office`  | `office_building` | Office Building  |

### Management (`#E7157B`)

| Tool Key               | Shape Name        | Description        |
|------------------------|-------------------|--------------------|
| `aws-cloudwatch`       | `cloudwatch_2`    | CloudWatch         |
| `aws-cloudformation`   | `cloudformation`  | CloudFormation     |
| `aws-config`           | `config`          | AWS Config         |
| `aws-cloudtrail`       | `cloudtrail`      | CloudTrail         |
| `aws-systems-manager`  | `systems_manager` | Systems Manager    |

### App Integration (`#E7157B`)

| Tool Key             | Shape Name       | Description      |
|----------------------|------------------|------------------|
| `aws-sqs`            | `sqs`            | SQS              |
| `aws-sns`            | `sns`            | SNS              |
| `aws-eventbridge`    | `eventbridge`    | EventBridge      |
| `aws-step-functions` | `step_functions` | Step Functions   |

### Analytics (`#8C4FFF`)

| Tool Key         | Shape Name   | Description   |
|------------------|--------------|---------------|
| `aws-athena`     | `athena`     | Athena        |
| `aws-kinesis`    | `kinesis`    | Kinesis       |
| `aws-glue`       | `glue`       | Glue          |
| `aws-quicksight` | `quicksight` | QuickSight    |

### ML/AI (`#01A88D`)

| Tool Key          | Shape Name    | Description   |
|-------------------|---------------|---------------|
| `aws-sagemaker`   | `sagemaker`   | SageMaker     |
| `aws-bedrock`     | `bedrock`     | Bedrock       |
| `aws-rekognition` | `rekognition` | Rekognition   |

### Developer Tools (`#C7131F`)

The developer tools category color exists but has no shapes in the current catalog. Use `shape=mxgraph.aws4.{service_name}` with `fillColor=#C7131F` directly.

## Container Style Presets

Used for VPC architecture diagrams. These are swimlane containers, not icons.

| Preset                     | Fill      | Stroke    | startSize | Dashed |
|----------------------------|-----------|-----------|-----------|--------|
| `aws-vpc`                  | `#E8F5E9` | `#388E3C` | 30        | No     |
| `aws-az`                   | `#E3F2FD` | `#1565C0` | 25        | Yes    |
| `aws-subnet-public`        | `#FFF3E0` | `#E65100` | 22        | No     |
| `aws-subnet-private-app`   | `#FCE4EC` | `#C62828` | 22        | No     |
| `aws-subnet-private-data`  | `#F3E5F5` | `#6A1B9A` | 22        | No     |

Container style template:
```
swimlane;startSize={SIZE};fillColor={FILL};strokeColor={STROKE};fontStyle=1;fontSize=14;rounded=1;arcSize=8;swimlaneLine=0;
```

Add `strokeDashArray=8 8;` for dashed borders (AZ style).

## Resource Icon Pattern

For services that use the resource-icon variant instead of a dedicated shape:

```
shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.{service};
```

This renders a square icon with the service logo inside. Use when no dedicated shape exists in the catalog above.
