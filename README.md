# Multi-Agent Customer Service System using MCP and A2A (Google ADK)

This project implements a fully functional multi-agent system using:

- Model Context Protocol (MCP) for database tool execution  
- Google ADK for multi-agent reasoning  
- A2A protocol for agent-to-agent communication  
- Async micro-services running inside Google Colab  

The system includes three collaborating agents:

- **Customer Data Agent**  
- **Support Agent**  
- **Router Agent**  

Together, they simulate a realistic customer-service backend capable of retrieving customer data, updating profiles, creating tickets, and resolving support issues through coordinated LLM agents.

---

## Features

### MCP Server
Implements five database tools:
- `get_customer`
- `list_customers`
- `update_customer`
- `create_ticket`
- `get_customer_history`

### Customer Data Agent
- Executes MCP tools directly  
- Handles structured data queries and updates  

### Support Agent
- Responds to customer-service questions  
- Delegates data operations to Customer Data Agent  
- Creates tickets and handles escalations  

### Router Agent
- Performs intent detection and routing  
- Decides which agent should handle the request  
- Supports multi-intent and multi-step workflows  

---

## Architecture
User → Router Agent → Support Agent
↘
Customer Data Agent → MCP Tools → SQLite DB


The Router Agent orchestrates all communication.  
The Customer Data Agent is the only agent allowed to call MCP tools.  
The Support Agent handles dialog and escalation.  

---

## Installation

Clone the repository:

```bash
git clone https://github.com/roseanne396/Multi-Agent-Customer-Service-System-with-A2A-and-MCP.git
cd https://github.com/roseanne396/Multi-Agent-Customer-Service-System-with-A2A-and-MCP.git
```
Install dependencies:
```bash
pip install -r requirements.txt
```
---

Running the MCP Server

Inside the Colab notebook:
```bash
start_server()
```

This launches:

MCP Server (port 5000)

Customer Data Agent (port 9101)

Support Agent (port 9102)

Router Agent (port 9200)

Running the Agents via A2A

Use the A2A client to send tasks:
```bash
response = await a2a_client.create_task(
    "http://localhost:9200",
    "Get customer information for ID 5"
)
print(response)
```
Test Scenarios
1. Simple Query
Get customer information for ID 5

2. Coordinated Query
I'm customer 12345 and need help upgrading my account

3. Complex Query
Show me all active customers who have open tickets

4. Escalation
I've been charged twice, please refund immediately

5. Multi-Intent Workflow
Update my email to user@example.com and show my ticket history


Summary of Learning

This project demonstrates how MCP enables standardized tool execution across agents, while A2A provides a structured communication protocol for multi-agent reasoning. Implementing this system highlighted key architectural considerations such as routing logic, agent separation, and asynchronous microservice orchestration inside Colab. The main challenges involved configuring multiple servers in one runtime, debugging A2A transport errors, ensuring strict JSON adherence during tool calls, and integrating MCP tool execution into the Customer Data Agent.
