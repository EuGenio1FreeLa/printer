# N8N Printer - Complete MCP & Skills Reference

> **Mission**: This folder is your ultimate N8N workflow factory. Use the n8n-mcp server and n8n-skills to build flawless, production-ready n8n workflows through AI assistance.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Local Installation](#local-installation)
3. [MCP Server Overview](#mcp-server-overview)
4. [All MCP Tools Reference](#all-mcp-tools-reference)
5. [The 7 Skills Explained](#the-7-skills-explained)
6. [Expression Syntax Guide](#expression-syntax-guide)
7. [JavaScript Code Patterns](#javascript-code-patterns)
8. [Python Code Patterns](#python-code-patterns)
9. [Workflow Patterns & Architecture](#workflow-patterns--architecture)
10. [Validation Profiles & Error Handling](#validation-profiles--error-handling)
11. [Workflow Creation Checklist](#workflow-creation-checklist)
12. [Best Practices](#best-practices)
13. [Quick Reference Cards](#quick-reference-cards)
14. [Resend Email Integration](#skill-8-resend-email-mcp)

---

## Quick Start

### Prerequisites
- n8n-mcp MCP server installed and configured (LOCAL - see below)
- Claude Code with MCP access
- n8n instance (optional, for deployment)

### MCP Configuration (LOCAL INSTALLATION)

This project has the MCP server installed locally. The `.mcp.json` is already configured:

```json
{
  "mcpServers": {
    "n8n-mcp": {
      "command": "node",
      "args": ["x:/DevOps/N8N Printer/n8n-mcp/dist/mcp/index.js"],
      "env": {
        "MCP_MODE": "stdio",
        "LOG_LEVEL": "error"
      }
    }
  }
}
```

### To connect to your n8n instance, update `.mcp.json`:

```json
{
  "mcpServers": {
    "n8n-mcp": {
      "command": "node",
      "args": ["x:/DevOps/N8N Printer/n8n-mcp/dist/mcp/index.js"],
      "env": {
        "MCP_MODE": "stdio",
        "LOG_LEVEL": "error",
        "N8N_API_URL": "https://your-n8n-instance.com/api/v1",
        "N8N_API_KEY": "your-api-key"
      }
    }
  }
}
```

---

## Local Installation

### Installed Repositories

This N8N Printer folder contains:

```
N8N Printer/
├── .mcp.json              # MCP configuration (ready to use)
├── claude.md              # This comprehensive guide
├── n8n-mcp/               # MCP Server (installed & built)
│   ├── dist/              # Compiled JavaScript
│   ├── data/              # Node database
│   └── src/               # Source code
└── n8n-skills/            # Skills Documentation
    └── skills/            # 7 skill guides
        ├── n8n-code-javascript/
        ├── n8n-code-python/
        ├── n8n-expression-syntax/
        ├── n8n-mcp-tools-expert/
        ├── n8n-node-configuration/
        ├── n8n-validation-expert/
        └── n8n-workflow-patterns/
```

### Update MCP Server

```bash
cd n8n-mcp
git pull
npm install
npm run build
```

### Update Skills

```bash
cd n8n-skills
git pull
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `MCP_MODE` | Yes | Set to `stdio` for Claude Desktop |
| `LOG_LEVEL` | No | Set to `error` to suppress debug output |
| `N8N_API_URL` | No* | Your n8n instance API endpoint |
| `N8N_API_KEY` | No* | API key for n8n authentication |
| `WEBHOOK_SECURITY_MODE` | No | Set to `moderate` for localhost |
| `N8N_MCP_TELEMETRY_DISABLED` | No | Set to `true` to disable telemetry |
| `SQLJS_SAVE_INTERVAL_MS` | No | Database save interval (default: 5000ms) |

*Required only for workflow management tools

---

## MCP Server Overview

### Coverage Statistics
- **1,084 nodes**: 537 core + 547 community (301 verified)
- **2,709 workflow templates** with 100% metadata
- **2,646 pre-extracted configurations** from templates
- **265 AI-capable tool variants**
- **87% documentation coverage**
- **99% node properties coverage**
- **~12ms average query response time**

### Tool Categories

| Category | Tools | Purpose |
|----------|-------|---------|
| Discovery | 2 | Find and explore nodes |
| Configuration | 1 | Get detailed node info |
| Validation | 2 | Validate configurations |
| Templates | 2 | Search and retrieve templates |
| Workflow Management | 10 | Create, update, execute workflows |
| System | 2 | Documentation and health checks |

---

## All MCP Tools Reference

### 1. `tools_documentation`

**Purpose**: Get documentation for any MCP tool. **Start here when unsure which tool to use.**

```
Parameters: None required
Returns: Documentation for all available tools
```

**Usage**: Call this first to understand available capabilities.

---

### 2. `search_nodes`

**Purpose**: Full-text search across all 1,084 nodes.

```
Parameters:
  - query: string (required) - Search term
  - source: 'community' | 'verified' | 'all' (optional)
  - includeExamples: boolean (optional) - Returns top 2 configurations per node
```

**Examples**:
```
search_nodes({ query: "slack" })
search_nodes({ query: "http request", source: "verified", includeExamples: true })
search_nodes({ query: "database", source: "community" })
```

---

### 3. `get_node`

**Purpose**: Unified node information retrieval with multiple modes.

#### Info Mode (Default)
```
Parameters:
  - nodeType: string (required) - e.g., "n8n-nodes-base.slack"
  - detail: 'minimal' | 'standard' | 'full' (optional)
  - includeExamples: boolean (optional)
```

#### Documentation Mode
```
Parameters:
  - nodeType: string (required)
  - mode: 'docs'
```

#### Property Search Mode
```
Parameters:
  - nodeType: string (required)
  - mode: 'search_properties'
  - propertyQuery: string (required)
```

#### Version Modes
```
Parameters:
  - nodeType: string (required)
  - mode: 'versions' | 'compare' | 'breaking' | 'migrations'
```

**NodeType Formats** (IMPORTANT):
- Core nodes: `n8n-nodes-base.nodeName` (e.g., `n8n-nodes-base.slack`)
- Community nodes: `n8n-nodes-community.nodeName`
- Sometimes: `nodes-base.nodeName` (legacy format)

**Examples**:
```
get_node({ nodeType: "n8n-nodes-base.httpRequest", detail: "full", includeExamples: true })
get_node({ nodeType: "n8n-nodes-base.code", mode: "docs" })
get_node({ nodeType: "n8n-nodes-base.slack", mode: "search_properties", propertyQuery: "channel" })
```

---

### 4. `validate_node`

**Purpose**: Validate node configuration before deployment.

#### Minimal Mode (Quick ~100ms)
```
Parameters:
  - nodeType: string (required)
  - configuration: object (required)
  - mode: 'minimal'
```

#### Full Mode (Comprehensive)
```
Parameters:
  - nodeType: string (required)
  - configuration: object (required)
  - mode: 'full'
  - profile: 'minimal' | 'runtime' | 'ai-friendly' | 'strict'
```

**Validation Profiles**:

| Profile | Use Case | Strictness |
|---------|----------|------------|
| `minimal` | Quick required fields check | Low |
| `runtime` | Pre-execution validation | Medium |
| `ai-friendly` | AI-generated configs (recommended) | Medium-High |
| `strict` | Production deployment | High |

**Example**:
```
validate_node({
  nodeType: "n8n-nodes-base.slack",
  configuration: {
    resource: "message",
    operation: "post",
    channel: "#general",
    text: "Hello!"
  },
  mode: "full",
  profile: "ai-friendly"
})
```

---

### 5. `validate_workflow`

**Purpose**: Complete workflow validation including AI Agent validation, connections, and expressions.

```
Parameters:
  - workflow: object (required) - Complete workflow JSON
  - profile: 'minimal' | 'runtime' | 'ai-friendly' | 'strict' (optional)
```

**Validates**:
- Node configurations
- Connection validity
- Expression syntax
- AI Agent tool connections
- Credential references

---

### 6. `search_templates`

**Purpose**: Unified template search with multiple discovery modes.

#### Keyword Search (Default)
```
Parameters:
  - searchMode: 'keyword'
  - query: string (required)
```

#### By Nodes
```
Parameters:
  - searchMode: 'by_nodes'
  - nodeTypes: string[] (required)
```

#### By Task
```
Parameters:
  - searchMode: 'by_task'
  - task: string (required) - Common task types
```

#### By Metadata
```
Parameters:
  - searchMode: 'by_metadata'
  - complexity: 'beginner' | 'intermediate' | 'advanced' (optional)
  - requiredService: string (optional)
  - targetAudience: string (optional)
```

**Examples**:
```
search_templates({ searchMode: "keyword", query: "slack notification" })
search_templates({ searchMode: "by_nodes", nodeTypes: ["n8n-nodes-base.slack", "n8n-nodes-base.webhook"] })
search_templates({ searchMode: "by_task", task: "send notifications" })
search_templates({ searchMode: "by_metadata", complexity: "beginner" })
```

---

### 7. `get_template`

**Purpose**: Retrieve complete workflow template JSON.

```
Parameters:
  - templateId: string (required)
  - mode: 'nodes_only' | 'structure' | 'full' (optional)
```

**Modes**:
- `nodes_only`: Just the node configurations
- `structure`: Nodes + connections
- `full`: Complete workflow with all metadata

---

### 8. `n8n_create_workflow`

**Purpose**: Create a new workflow on your n8n instance.

```
Parameters:
  - name: string (required)
  - nodes: array (required) - Array of node configurations
  - connections: object (required) - Node connection mappings
  - settings: object (optional)
  - active: boolean (optional, default: false)
```

**Example**:
```
n8n_create_workflow({
  name: "My Workflow",
  nodes: [
    {
      name: "Webhook",
      type: "n8n-nodes-base.webhook",
      position: [250, 300],
      parameters: {
        path: "my-webhook",
        httpMethod: "POST"
      }
    },
    {
      name: "Slack",
      type: "n8n-nodes-base.slack",
      position: [450, 300],
      parameters: {
        resource: "message",
        operation: "post",
        channel: "#alerts",
        text: "={{ $json.body.message }}"
      }
    }
  ],
  connections: {
    "Webhook": {
      "main": [[{ "node": "Slack", "type": "main", "index": 0 }]]
    }
  }
})
```

---

### 9. `n8n_get_workflow`

**Purpose**: Retrieve workflow from n8n instance.

```
Parameters:
  - workflowId: string (required)
  - mode: 'full' | 'details' | 'structure' | 'minimal' (optional)
```

---

### 10. `n8n_update_full_workflow`

**Purpose**: Complete workflow replacement.

```
Parameters:
  - workflowId: string (required)
  - workflow: object (required) - Complete workflow JSON
```

**Warning**: This replaces the entire workflow. Use `n8n_update_partial_workflow` for incremental changes.

---

### 11. `n8n_update_partial_workflow`

**Purpose**: Diff-based updates with 17 operation types. **Most used tool (38,287 uses, 99.0% success rate)**.

```
Parameters:
  - workflowId: string (required)
  - operations: array (required) - Array of update operations
```

**Available Operations**:

| Operation | Description |
|-----------|-------------|
| `add_node` | Add a new node |
| `remove_node` | Remove a node |
| `update_node` | Update node parameters |
| `rename_node` | Rename a node |
| `move_node` | Change node position |
| `add_connection` | Connect two nodes |
| `remove_connection` | Disconnect nodes |
| `update_settings` | Modify workflow settings |
| `set_active` | Activate/deactivate workflow |
| ... | (and more) |

**Example**:
```
n8n_update_partial_workflow({
  workflowId: "123",
  operations: [
    {
      operation: "add_node",
      node: {
        name: "HTTP Request",
        type: "n8n-nodes-base.httpRequest",
        position: [650, 300],
        parameters: { url: "https://api.example.com" }
      }
    },
    {
      operation: "add_connection",
      from: "Webhook",
      to: "HTTP Request"
    }
  ]
})
```

**Token Savings**: 80-90% compared to full workflow updates.

---

### 12. `n8n_delete_workflow`

**Purpose**: Permanently delete a workflow.

```
Parameters:
  - workflowId: string (required)
```

**Warning**: This action is irreversible.

---

### 13. `n8n_list_workflows`

**Purpose**: List workflows with filtering and pagination.

```
Parameters:
  - limit: number (optional)
  - cursor: string (optional)
  - active: boolean (optional)
  - tags: string[] (optional)
```

---

### 14. `n8n_validate_workflow`

**Purpose**: Validate a deployed workflow by ID.

```
Parameters:
  - workflowId: string (required)
  - profile: 'minimal' | 'runtime' | 'ai-friendly' | 'strict' (optional)
```

---

### 15. `n8n_autofix_workflow`

**Purpose**: Automatically correct common workflow errors.

```
Parameters:
  - workflowId: string (required)
  - dryRun: boolean (optional) - Preview fixes without applying
```

**Auto-fixes**:
- Missing required fields
- Invalid connections
- Expression syntax errors
- Deprecated node versions

---

### 16. `n8n_workflow_versions`

**Purpose**: Manage version history and rollback.

```
Parameters:
  - workflowId: string (required)
  - action: 'list' | 'get' | 'rollback' (required)
  - versionId: string (optional, for get/rollback)
```

---

### 17. `n8n_deploy_template`

**Purpose**: Deploy templates directly to n8n with auto-fix.

```
Parameters:
  - templateId: string (required)
  - name: string (optional) - Override template name
  - autofix: boolean (optional) - Apply auto-fixes during deployment
```

---

### 18. `n8n_test_workflow`

**Purpose**: Test/trigger workflow execution with auto-detection of trigger types.

```
Parameters:
  - workflowId: string (required)
  - inputData: object (optional) - Test data for manual triggers
  - waitForCompletion: boolean (optional)
```

---

### 19. `n8n_executions`

**Purpose**: Manage workflow executions.

```
Parameters:
  - action: 'list' | 'get' | 'delete' (required)
  - workflowId: string (optional)
  - executionId: string (optional, for get/delete)
  - limit: number (optional)
  - status: 'success' | 'error' | 'waiting' (optional)
```

---

### 20. `n8n_health_check`

**Purpose**: Verify API connectivity to n8n instance.

```
Parameters: None
Returns: Connection status, version info, available features
```

---

## The 7 Skills Explained

### Skill 1: n8n Expression Syntax (CRITICAL)

**When to use**: Any time you need to reference data between nodes or use dynamic values.

#### Core Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `$json` | Current item's JSON data | `{{ $json.email }}` |
| `$json.body` | **Webhook payload** (CRITICAL) | `{{ $json.body.message }}` |
| `$node` | Access other nodes' data | `{{ $node["Node Name"].json.field }}` |
| `$input` | Input data reference | `{{ $input.first().json }}` |
| `$now` | Current timestamp | `{{ $now.toISO() }}` |
| `$today` | Today's date | `{{ $today }}` |
| `$env` | Environment variables | `{{ $env.API_KEY }}` |
| `$vars` | Workflow variables | `{{ $vars.myVariable }}` |
| `$execution` | Execution metadata | `{{ $execution.id }}` |
| `$workflow` | Workflow metadata | `{{ $workflow.name }}` |
| `$itemIndex` | Current item index | `{{ $itemIndex }}` |
| `$runIndex` | Current run index | `{{ $runIndex }}` |

#### Expression Syntax Rules

```javascript
// Basic field access
{{ $json.fieldName }}

// Nested field access
{{ $json.user.profile.name }}

// Array access
{{ $json.items[0].name }}

// Conditional (ternary)
{{ $json.status === 'active' ? 'Yes' : 'No' }}

// String interpolation
{{ 'Hello ' + $json.name }}

// Method calls
{{ $json.email.toLowerCase() }}

// Date formatting
{{ $now.format('yyyy-MM-dd') }}

// Math operations
{{ $json.price * 1.1 }}

// Null coalescing
{{ $json.optionalField ?? 'default' }}
```

#### CRITICAL: Webhook Data Access

**WRONG**:
```javascript
{{ $json.message }}  // This won't work for webhook data!
```

**CORRECT**:
```javascript
{{ $json.body.message }}  // Webhook payloads are under $json.body
{{ $json.headers }}       // Access headers
{{ $json.query }}         // Access query parameters
```

#### Common Mistakes & Fixes

| Mistake | Fix |
|---------|-----|
| `$json.webhookData` | `$json.body.webhookData` |
| `{{ $json.field }` (missing `}}`) | `{{ $json.field }}` |
| `$json["field name"]` without expression | `{{ $json["field name"] }}` |
| Using expressions in Code node | Use direct JavaScript instead |

---

### Skill 2: n8n MCP Tools Expert (HIGHEST PRIORITY)

**When to use**: Every time you interact with n8n-mcp tools.

#### Tool Selection Guide

| Task | Tool | Key Parameters |
|------|------|----------------|
| Find a node | `search_nodes` | `query`, `source` |
| Get node details | `get_node` | `nodeType`, `detail`, `mode` |
| Validate config | `validate_node` | `profile: "ai-friendly"` |
| Find templates | `search_templates` | `searchMode` |
| Create workflow | `n8n_create_workflow` | `nodes`, `connections` |
| Update workflow | `n8n_update_partial_workflow` | `operations` |
| Fix errors | `n8n_autofix_workflow` | `workflowId` |

#### NodeType Format Rules

```
Core nodes:     n8n-nodes-base.{nodeName}
Community:      n8n-nodes-community.{nodeName}
Legacy format:  nodes-base.{nodeName}
```

**Tip**: If one format fails, try the other.

#### Validation Profile Selection

| Stage | Profile | Why |
|-------|---------|-----|
| Initial development | `minimal` | Quick feedback loop |
| Testing | `runtime` | Catch execution issues |
| AI-generated | `ai-friendly` | Balanced for AI patterns |
| Production | `strict` | Maximum safety |

#### Smart Parameters

- **IF Node**: Use `branch="true"` parameter for conditional routing
- **Switch Node**: Map cases to output indices
- **Merge Node**: Specify merge mode explicitly

---

### Skill 3: n8n Workflow Patterns

**When to use**: Designing workflow architecture.

#### Pattern 1: Webhook Processing

```
Webhook → Process → Respond/Action
```

**Use for**: API endpoints, form submissions, external triggers

**Key nodes**: `Webhook`, `Respond to Webhook`, `HTTP Request`

```javascript
// Webhook configuration
{
  "type": "n8n-nodes-base.webhook",
  "parameters": {
    "path": "my-endpoint",
    "httpMethod": "POST",
    "responseMode": "responseNode"  // or "onReceived"
  }
}
```

#### Pattern 2: HTTP API Integration

```
Trigger → HTTP Request → Transform → Action
```

**Use for**: External API calls, data fetching, integrations

**Key nodes**: `HTTP Request`, `Set`, `Code`

```javascript
// HTTP Request with auth
{
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "url": "https://api.example.com/data",
    "authentication": "genericCredentialType",
    "method": "GET",
    "options": {
      "response": { "response": { "fullResponse": true } }
    }
  }
}
```

#### Pattern 3: Database Workflows

```
Trigger → Query/Insert → Transform → Output
```

**Use for**: Data sync, CRUD operations, reporting

**Key nodes**: `Postgres`, `MySQL`, `MongoDB`, `Supabase`

#### Pattern 4: AI-Driven Automation

```
Trigger → AI Agent → Tool Calls → Response
```

**Use for**: Intelligent automation, chatbots, content generation

**Key nodes**: `AI Agent`, `OpenAI`, `Anthropic`, `Tools`

**AI Connection Types**:
1. `ai_languageModel` - Main LLM connection
2. `ai_tool` - Tool connections for agent
3. `ai_memory` - Conversation memory
4. `ai_outputParser` - Response parsing
5. `ai_retriever` - RAG retrieval
6. `ai_document` - Document loaders
7. `ai_textSplitter` - Text chunking
8. `ai_embedding` - Vector embeddings

#### Pattern 5: Scheduled Tasks

```
Schedule Trigger → Fetch Data → Process → Store/Notify
```

**Use for**: Cron jobs, periodic syncs, automated reports

**Key nodes**: `Schedule Trigger`, `Cron`

---

### Skill 4: n8n Validation Expert

**When to use**: Debugging validation errors.

#### Common Error Categories

| Error Type | Cause | Fix |
|------------|-------|-----|
| Missing required field | Field not provided | Add the required parameter |
| Invalid operation | Wrong operation for resource | Check `get_node` for valid operations |
| Connection error | Nodes not properly linked | Verify connection object structure |
| Expression error | Invalid expression syntax | Check brackets, quotes, variable names |
| Credential error | Missing/invalid credentials | Add credentials to n8n and reference |

#### Error Interpretation

```
"validation.required.missing" → Add the missing field
"validation.type.mismatch" → Check expected type (string, number, etc.)
"validation.enum.invalid" → Use one of the allowed values
"validation.connection.invalid" → Fix node connection structure
```

#### False Positives

Some validations may be overly strict. Common false positives:

- Optional fields marked as required
- Dynamic values not recognized
- Expression results not evaluated

**Solution**: Use `ai-friendly` profile which is more tolerant.

#### Auto-Fix Capabilities

`n8n_autofix_workflow` can automatically fix:
- Missing default values
- Deprecated parameter names
- Invalid position values
- Common expression typos

---

### Skill 5: n8n Node Configuration

**When to use**: Setting up individual nodes correctly.

#### Property Dependencies

Some properties require others to be set:

| Property | Requires |
|----------|----------|
| `sendBody` | `contentType` |
| `sendQuery` | Query parameters |
| `authentication` | Credential type |
| `responseMode: "responseNode"` | `Respond to Webhook` node |

#### Operation-Specific Configuration

Different operations require different parameters:

```javascript
// Slack: Post Message
{
  "resource": "message",
  "operation": "post",
  "channel": "#channel-name",  // Required
  "text": "Message content"     // Required
}

// Slack: Get Message
{
  "resource": "message",
  "operation": "get",
  "channel": "#channel-name",  // Required
  "messageTs": "1234567890.123" // Required
}
```

#### AI Node Configuration

```javascript
// AI Agent setup
{
  "type": "@n8n/n8n-nodes-langchain.agent",
  "parameters": {
    "promptType": "define",
    "text": "You are a helpful assistant...",
    "options": {
      "systemMessage": "System prompt here"
    }
  }
}
```

---

### Skill 6: n8n Code JavaScript

**When to use**: Custom logic in Code nodes.

#### Data Access Patterns

```javascript
// Get all input items
const items = $input.all();

// Get first item only
const firstItem = $input.first();

// Get current item (in "Run Once for Each Item" mode)
const currentItem = $input.item;

// Access specific node's output
const nodeData = $node["Node Name"].json;

// Access by index
const thirdItem = $input.all()[2];
```

#### CRITICAL: Return Format

**Always return an array of objects with `json` property**:

```javascript
// CORRECT - Single item
return [{ json: { result: "value" } }];

// CORRECT - Multiple items
return [
  { json: { id: 1, name: "First" } },
  { json: { id: 2, name: "Second" } }
];

// CORRECT - Transform input items
return $input.all().map(item => ({
  json: {
    ...item.json,
    newField: "added value"
  }
}));

// WRONG - Missing json wrapper
return [{ result: "value" }];  // Will fail!

// WRONG - Not an array
return { json: { result: "value" } };  // Will fail!
```

#### Built-in Helpers

```javascript
// HTTP Request
const response = await $helpers.httpRequest({
  method: 'GET',
  url: 'https://api.example.com/data',
  headers: { 'Authorization': 'Bearer token' }
});

// DateTime (Luxon)
const now = DateTime.now();
const formatted = now.toFormat('yyyy-MM-dd');
const parsed = DateTime.fromISO('2024-01-15');

// Access environment variables
const apiKey = $env.API_KEY;

// Access workflow variables
const configValue = $vars.myConfig;
```

#### Top 5 Error Patterns (62%+ of failures)

1. **Wrong return format** → Always use `[{ json: {...} }]`
2. **Accessing $json.body directly** → Use `$input.first().json.body`
3. **Forgetting await on async** → Add `await` for HTTP calls
4. **Undefined variable access** → Check with optional chaining `?.`
5. **Type errors** → Validate data types before operations

#### Production-Tested Patterns

```javascript
// Pattern 1: Safe data transformation
return $input.all().map(item => {
  const data = item.json;
  return {
    json: {
      id: data.id ?? 'unknown',
      name: (data.name || '').trim(),
      processed: true
    }
  };
});

// Pattern 2: Filter items
return $input.all().filter(item => item.json.status === 'active');

// Pattern 3: Aggregate data
const items = $input.all();
const total = items.reduce((sum, item) => sum + (item.json.amount || 0), 0);
return [{ json: { total, count: items.length } }];

// Pattern 4: API call with error handling
try {
  const response = await $helpers.httpRequest({
    method: 'POST',
    url: 'https://api.example.com/data',
    body: $input.first().json,
    headers: { 'Content-Type': 'application/json' }
  });
  return [{ json: response }];
} catch (error) {
  return [{ json: { error: error.message, success: false } }];
}

// Pattern 5: Date processing
const items = $input.all();
return items.map(item => ({
  json: {
    ...item.json,
    createdAt: DateTime.fromISO(item.json.date).toFormat('dd/MM/yyyy'),
    isRecent: DateTime.fromISO(item.json.date) > DateTime.now().minus({ days: 7 })
  }
}));
```

---

### Skill 7: n8n Code Python

**When to use**: Only when Python is specifically required (~5% of cases).

#### Critical Limitations

**NOT AVAILABLE**:
- `requests` library
- `pandas`
- `numpy`
- Any external packages

**AVAILABLE** (Standard Library):
- `json`
- `datetime`
- `re` (regex)
- `math`
- `collections`
- `itertools`
- `functools`

#### Data Access in Python

```python
# Get all items
items = _input.all()

# Get first item
first_item = _input.first()

# Access JSON data
data = first_item['json']

# Access specific field
value = first_item['json']['fieldName']
```

#### Return Format (Python)

```python
# CORRECT - Single item
return [{"json": {"result": "value"}}]

# CORRECT - Multiple items
return [
    {"json": {"id": 1}},
    {"json": {"id": 2}}
]

# CORRECT - Transform items
return [{"json": {**item["json"], "new_field": "value"}} for item in _input.all()]
```

#### Workarounds for Missing Libraries

```python
# Instead of requests, use n8n's HTTP Request node before Code node
# Then access the response:
response_data = _input.first()['json']

# Instead of pandas for CSV:
import csv
from io import StringIO

csv_string = _input.first()['json']['csvData']
reader = csv.DictReader(StringIO(csv_string))
rows = list(reader)
return [{"json": row} for row in rows]

# Instead of datetime parsing with pandas:
from datetime import datetime

date_str = _input.first()['json']['date']
parsed = datetime.strptime(date_str, '%Y-%m-%d')
```

---

## Skill 8: Resend Email MCP

**When to use**: Sending transactional emails from workflows - notifications, alerts, reports, onboarding.

### Configuration

Added to `.mcp.json` alongside n8n-mcp:

```json
"resend": {
  "command": "node",
  "args": ["x:/DevOps/N8N Printer/resend-mcp/build/index.js"],
  "env": {
    "RESEND_API_KEY": "your-api-key",
    "SENDER_EMAIL_ADDRESS": "onboarding@resend.dev"
  }
}
```

### send_email Tool

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `to` | Yes | string/string[] | Recipient(s) |
| `subject` | Yes | string | Subject line |
| `text` | Yes* | string | Plain text content |
| `html` | Yes* | string | HTML content |
| `from` | No | string | Override sender |
| `cc` | No | string[] | CC recipients |
| `bcc` | No | string[] | BCC recipients |
| `replyTo` | No | string | Reply-to address |
| `scheduledAt` | No | string | ISO 8601 scheduled time |

*Provide either `text` OR `html`, not both.

### Quick Examples

```typescript
// Plain text notification
send_email({
  to: "admin@example.com",
  subject: "Workflow Alert",
  text: "Your workflow completed successfully."
})

// HTML report to multiple recipients
send_email({
  to: ["manager@example.com", "analyst@example.com"],
  subject: "Daily Report",
  html: "<h1>Report</h1><p>All systems operational.</p>"
})

// Scheduled email with CC
send_email({
  to: "user@example.com",
  cc: ["team@example.com"],
  subject: "Reminder",
  text: "Weekly sync in 1 hour.",
  scheduledAt: "2026-02-01T09:00:00Z"
})
```

### Integration Patterns

| Pattern | Flow | Use Case |
|---------|------|----------|
| Webhook Notification | `Webhook --> Code --> Email` | Email on external events |
| Error Alerting | `Error Trigger --> Code --> Email` | DevOps error alerts |
| Scheduled Reports | `Schedule --> Fetch --> Code --> Email` | Daily/weekly reports |
| Conditional Email | `Trigger --> IF --> Email A / Email B` | Different emails by condition |

### Critical Requirements

1. **API Key** - Get from resend.com/api-keys, set in .mcp.json
2. **Domain Verification** - Required for production (resend.com/domains)
3. **Test Sender** - Use `onboarding@resend.dev` for testing
4. **Rate Limits** - Free tier: 100 emails/day, 1/second

**Full documentation:** `n8n-skills/skills/resend-email-mcp/SKILL.md`

---

## Validation Profiles & Error Handling

### Profile Comparison

| Profile | Required Fields | Type Checking | Expression Validation | Credential Check | Use Case |
|---------|----------------|---------------|----------------------|------------------|----------|
| `minimal` | Yes | No | No | No | Quick iteration |
| `runtime` | Yes | Yes | Basic | Yes | Pre-execution |
| `ai-friendly` | Yes | Lenient | Yes | Lenient | AI-generated |
| `strict` | Yes | Strict | Full | Full | Production |

### Validation Workflow

```
1. Create/Update workflow
2. Validate with ai-friendly profile
3. Fix any errors
4. Re-validate with strict profile (for production)
5. Deploy or test
```

### Common Validation Errors

#### Required Field Missing
```
Error: "validation.required.missing: field 'channel' is required"
Fix: Add the channel parameter to your node configuration
```

#### Invalid Operation
```
Error: "validation.operation.invalid: 'sendMessage' is not valid for resource 'channel'"
Fix: Use get_node to find valid operations for the resource
```

#### Expression Error
```
Error: "validation.expression.invalid: unclosed bracket"
Fix: Check your {{ }} brackets match and are properly closed
```

---

## Workflow Creation Checklist

### Before Starting
- [ ] Identify the trigger type (webhook, schedule, manual, app trigger)
- [ ] List all required integrations/nodes
- [ ] Plan the data flow between nodes
- [ ] Identify required credentials

### Node Configuration
- [ ] Use correct nodeType format (`n8n-nodes-base.*`)
- [ ] Set all required parameters for each operation
- [ ] Use proper expression syntax for dynamic values
- [ ] Configure credentials where needed

### Connections
- [ ] Connect all nodes in correct order
- [ ] Handle multiple outputs (IF, Switch nodes)
- [ ] Verify no orphan nodes exist

### Validation
- [ ] Run `validate_workflow` with `ai-friendly` profile
- [ ] Fix all validation errors
- [ ] Run `validate_workflow` with `strict` profile for production

### Testing
- [ ] Use `n8n_test_workflow` for execution testing
- [ ] Verify data transforms correctly between nodes
- [ ] Check error handling paths

### Deployment
- [ ] Export workflow backup
- [ ] Deploy to test environment first
- [ ] Activate workflow only when ready

---

## Best Practices

### 1. Safety First
> **Never edit production workflows directly with AI. Always:**
> - Copy the workflow first
> - Test in development environment
> - Export backups before changes
> - Validate thoroughly

### 2. Use Partial Updates
Prefer `n8n_update_partial_workflow` over `n8n_update_full_workflow`:
- 80-90% token savings
- Lower risk of data loss
- Better audit trail

### 3. Validate Early and Often
```
Create → Validate → Fix → Validate → Test → Deploy
```

### 4. Expression Best Practices
- Always use `$json.body` for webhook data
- Use optional chaining for potentially undefined values: `$json.data?.field`
- Test expressions in n8n's expression editor first

### 5. Code Node Guidelines
- Use JavaScript for 95% of cases
- Always return `[{ json: {...} }]` format
- Handle errors gracefully
- Avoid external HTTP calls in Code nodes (use HTTP Request node instead)

### 6. Template Attribution
When using templates, always include:
```
"Based on template by [author] (@username). View at: [url]"
```

---

## Quick Reference Cards

### Expression Cheat Sheet

```javascript
// Data access
{{ $json.field }}                    // Current item field
{{ $json.body.field }}               // Webhook payload field
{{ $node["Name"].json.field }}       // Other node's field
{{ $input.first().json.field }}      // First input item

// Conditionals
{{ $json.status === 'active' ? 'Yes' : 'No' }}
{{ $json.value ?? 'default' }}       // Null coalescing

// Dates
{{ $now }}                           // Current datetime
{{ $now.toISO() }}                   // ISO format
{{ $now.format('yyyy-MM-dd') }}      // Custom format
{{ $today }}                         // Today's date

// String operations
{{ $json.name.toUpperCase() }}
{{ $json.text.replace('old', 'new') }}
{{ 'Hello ' + $json.name }}

// Numbers
{{ Math.round($json.value) }}
{{ $json.price * 1.1 }}
```

### Tool Usage Cheat Sheet

```
Find node:        search_nodes({ query: "slack" })
Get node info:    get_node({ nodeType: "n8n-nodes-base.slack", detail: "full" })
Validate:         validate_node({ nodeType: "...", configuration: {...}, profile: "ai-friendly" })
Find template:    search_templates({ searchMode: "keyword", query: "notification" })
Create workflow:  n8n_create_workflow({ name: "...", nodes: [...], connections: {...} })
Update workflow:  n8n_update_partial_workflow({ workflowId: "...", operations: [...] })
Auto-fix:         n8n_autofix_workflow({ workflowId: "..." })
Test:             n8n_test_workflow({ workflowId: "..." })
```

### Code Node Return Formats

```javascript
// JavaScript - Always use this format:
return [{ json: { key: "value" } }];

// Multiple items:
return [
  { json: { id: 1 } },
  { json: { id: 2 } }
];

// Transform input:
return $input.all().map(item => ({
  json: { ...item.json, newField: "value" }
}));
```

```python
# Python - Always use this format:
return [{"json": {"key": "value"}}]

# Multiple items:
return [
    {"json": {"id": 1}},
    {"json": {"id": 2}}
]
```

### Connection Object Structure

```javascript
{
  "Source Node Name": {
    "main": [
      [{ "node": "Target Node Name", "type": "main", "index": 0 }]
    ]
  }
}

// For nodes with multiple outputs (IF, Switch):
{
  "IF": {
    "main": [
      [{ "node": "True Branch Node", "type": "main", "index": 0 }],  // True output
      [{ "node": "False Branch Node", "type": "main", "index": 0 }]  // False output
    ]
  }
}
```

---

## MCP Tool Usage Patterns

### Most Common Pattern
```
search_nodes → get_node (avg 18s between steps)
```

### Most Common Validation Pattern
```
n8n_update_partial_workflow → n8n_validate_workflow
(7,841 occurrences; avg 23s thinking, 58s fixing)
```

### Recommended Workflow Building Pattern

1. **Discovery**: `search_nodes` → Find relevant nodes
2. **Learn**: `get_node` with `detail: "full"` → Understand configuration
3. **Template**: `search_templates` → Find similar workflows
4. **Create**: `n8n_create_workflow` → Build initial workflow
5. **Validate**: `validate_workflow` → Check for errors
6. **Fix**: `n8n_autofix_workflow` or manual fixes → Resolve issues
7. **Test**: `n8n_test_workflow` → Verify execution
8. **Iterate**: `n8n_update_partial_workflow` → Refine as needed

---

## Troubleshooting

### MCP Connection Issues
1. Verify `MCP_MODE=stdio` is set
2. Check Claude Desktop config path
3. Restart Claude Desktop after config changes
4. Run `n8n_health_check` to verify connectivity

### Validation Failures
1. Start with `ai-friendly` profile
2. Use `get_node` to verify correct parameters
3. Check expression syntax (brackets, quotes)
4. Verify nodeType format

### Workflow Execution Failures
1. Check credentials are properly configured in n8n
2. Verify webhook URLs are accessible
3. Check for expression evaluation errors
4. Review execution logs in n8n

---

*Conceived by Romuald Czlonkowski - www.aiadvisors.pl/en*

*Documentation compiled for N8N Printer project*
