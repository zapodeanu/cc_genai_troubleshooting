
# Catalyst Center Troubleshooting IssuesPilot


The repo includes the files to:

- Create and run a Chrom DB vector database server.
It will create the folder to store the data and start the server.
A second app will allow to erase the vector database and/or create a new vector database.

- Create Embeddings 
Create embeddings and save them to local or server vector database.

- Client App:
Query and answer: Similarity searches using GPT-4o
Conversational: GPT-4o and Anthropic Sonnet 4

Sample Output:

Your input: Can you check the active issues, devices impacted and provide a summary of your findings

IssuesPilot: 
## Active Issues Summary

### **Critical BGP Failures - P1 Priority**

**Issue 1: PDX-RO BGP Down**
- **Device**: PDX-RO (CSR1000V, SN: 9XIF5ZTLXRB)
- **Problem**: BGP session down with neighbor 10.93.141.42
- **Status**: Idle state (completely down)
- **Timestamp**: Fri Jun 6 11:41:51 2025
- **Duration**: Ongoing for ~19 minutes

**Issue 2: PDX-RN BGP Down** 
- **Device**: PDX-RN (CSR1000V, SN: 92ML86IWCBN)
- **Problem**: BGP session down with neighbor 10.93.141.41  
- **Status**: Active state (attempting connection but failing)
- **Timestamp**: Fri Jun 6 11:41:51 2025
- **Duration**: Ongoing for ~13 minutes

## Devices Impacted

### **Primary Impact:**
- **PDX-RO** - Edge router in AS 65002 at Global/OR/PDX/Floor-2
- **PDX-RN** - Edge router in AS 65001 at Global/OR/PDX/Floor-2

### **Secondary Impact:**
- **Inter-AS connectivity** between AS 65001 and AS 65002 compromised
- **Site-wide routing** potentially affected (both devices at same location)
- **Upstream/downstream traffic flows** likely impacted

## Key Findings Summary

### **Root Cause Analysis:**

1. **Definitive Cause - Access Control List Issue:**
   - **PDX-RN has WAN ACL explicitly blocking ALL BGP traffic**
   - ACL rules `10 deny tcp any eq bgp any` (93 matches) and `15 deny tcp any any eq bgp` (104 matches)
   - **This is actively blocking BGP sessions and causing the failures**

2. **Timing Correlation:**
   - Both BGP sessions failed simultaneously at 11:41:51
   - Recent configuration changes detected on both devices around the same timeframe
   - PDX-RO config change at 11:41:10 (41 seconds before BGP failure)

3. **Network Architecture Concerns:**
   - Both critical edge routers at same physical site
   - Single points of failure for inter-AS connectivity
   - No apparent BGP session redundancy

### **Compliance Status:**
- **PDX-RO**: All compliance checks PASSED (IMAGE, PSIRT, RUNNING_CONFIG)
- **PDX-RN**: Generally compliant with network standards

### **Security Observations:**
- **Unauthorized configuration changes** possible (user account made recent changes)
- **No apparent change control** mechanisms in place
- **ACL misconfigurations** causing business-critical service outages

## Immediate Action Required

**URGENT - Fix BGP blocking:**
```cisco
! On PDX-RN device
configure terminal
ip access-list extended WAN
no 10
no 15
exit
```

## Business Impact
- **HIGH** - P1 priority indicates critical business services affected
- **Inter-site connectivity** between autonomous systems is down
- **Potential revenue impact** if these are customer-facing services
- **SLA breach risk** for uptime commitments

**Recommendation**: Implement immediate fix for ACL blocking, followed by comprehensive network resilience and change control improvements.

Your input: 