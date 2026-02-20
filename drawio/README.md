# drawio skill

Create, read, and modify draw.io diagrams — AWS/Azure/GCP architecture, flowcharts, ERDs, state diagrams, Mermaid, and CSV.

## Install

```bash
# From the repo root:
./install.sh drawio

# Manual copy:
cp -r .claude/skills/drawio ~/.claude/skills/drawio
# or project-level:
cp -r .claude/skills/drawio /path/to/your/project/.claude/skills/drawio
```

Restart Claude Code after installing.

## Quick start

Say any of these to Claude Code after installing the skill:

| What you want | Example prompt |
|---------------|----------------|
| AWS architecture | `Draw an AWS 3-tier architecture with ALB, EC2 in two AZs, RDS, and ElastiCache. Save to arch.drawio.` |
| Serverless architecture | `Create a serverless diagram: API Gateway → Lambda → DynamoDB, with S3 for assets and SNS for notifications.` |
| Flowchart | `Generate a Mermaid flowchart for a user login flow with happy path and error handling.` |
| Sequence diagram | `Make a sequence diagram: browser → API Gateway → Lambda → DynamoDB, in Mermaid format.` |
| ERD | `Create an ERD for a blog app with Users, Posts, Comments, and Tags.` |
| Org chart | `Generate a CSV org chart: CTO → two VPs → four team leads.` |
| Read a diagram | `Read arch.drawio and describe what's in it.` |
| Modify a diagram | `Add a CloudWatch node to arch.drawio connected to the Lambda function.` |

## Viewers

Standalone browser tools — no install needed, just open in any browser:

| File | Description |
|------|-------------|
| [viewers/drawioxml_viewer.html](viewers/drawioxml_viewer.html) | Paste or load a `.drawio` XML file and render it inline using the official draw.io viewer library |
| [viewers/mermaid_viewer.html](viewers/mermaid_viewer.html) | Paste or load a `.mmd` Mermaid file and render it — includes 8 built-in examples and 5 themes |

## Examples

```
examples/
├── microservices.drawio   # AWS microservices architecture (Lambda, API GW, DynamoDB, SNS)
├── ec2_lifecycle.drawio   # EC2 instance state machine with AWS icons
└── ec2_lifecycle.mmd      # Same diagram in Mermaid format
```

## Skill reference

Full documentation is in [`.claude/skills/drawio/SKILL.md`](../.claude/skills/drawio/SKILL.md).
