
## Slide 1

Agentic Identity Security.
Zero Trust for every AI agent and every action it takes.

## Slide 2

Six Parts Take You From the Problem to Proof.
TABLE OF CONTENTS.
01.
The Problem.
Agents act, IAM cannot see.
Slides 3 to 10.
02.
Why Tools Fall Short.
Keys, IAM, point tools.
Slides 11 to 14.
03.
The AccuKnox Solution.
Control plane and flow.
Slides 15 to 19.
04.
Capabilities in Depth.
Ten capabilities, flows, stack.
Slides 20 to 31.
05.
CIEM in the Product.
Cloud identities today.
Slides 32 to 35.
06.
Why AccuKnox.
Proof, outcomes, demo.
Slides 36 to 40.

Agenda. The deck follows one line of argument.
Part 1, the business problem: AI agents act with real credentials, and identity tools were built for people.
Part 2, why today's options fall short: static keys, legacy IAM, and three vendor categories that each cover only part of the problem.
Part 3, the AccuKnox solution: the AgentZ control plane, the reference architecture, and how one request flows.
Part 4, ten capabilities in depth, two per slide.
Part 5, CIEM: the cloud identity inventory AccuKnox ships for human and machine identities.
Part 6, why AccuKnox: differentiators, the category comparison, outcomes and the demo.
Backup slides after the closing slide are hidden. They hold the PRD goals, proposed targets, roadmap and open questions.

## Slide 3

PART 1 · THE BUSINESS PROBLEM.
AI Agents Now Act With Real Credentials.
They call tools, move data and chain to other agents. Identity tools still assume a person is at the keyboard..

Part 1 sets the business context. Agents are now the fastest-growing identity type, and the identity stack cannot tell who an agent acts for.

## Slide 4

Machine Identities Already Outnumber People 82 to 1.
CONTEXT.
82:1.
machine identities for every human identity.
CyberArk 2025.
88%.
of organizations treat only humans as privileged.
CyberArk 2025.
80%.
saw AI agents take unintended actions.
SailPoint 2025.
23%.
saw agents tricked into revealing credentials.
SailPoint 2025.
Agents are the fastest-growing identity type, and the least governed one..

Talk track: agents are the newest and fastest-growing kind of machine identity, and most programs still govern only humans.
Sources.
82 to 1, and 88 percent: CyberArk 2025 Identity Security Landscape, a survey of 2,600 security decision-makers. Machine identities outnumber humans 82 to 1. 88 percent of organizations define only human identities as privileged users. cyberark.com/resources/identity-security/2025-identity-security-landscape
80 percent and 23 percent: SailPoint research on AI agent adoption, 2025. 80 percent of companies say their AI agents took unintended actions, including access to unauthorized systems (39 percent). 23 percent say agents were tricked into revealing access credentials. sailpoint.com/press-releases/sailpoint-ai-agent-adoption-report
These are third-party survey numbers. Quote them with the source on any external version.

## Slide 5

IAM Was Built for People, Not for Agents.
THE PROBLEM.
01.
They act, not only answer.
Agents call tools, move data and trigger workflows, often with no human in the loop..
02.
Their keys are static and too broad.
Long-lived API keys and shared accounts give far more access than a task needs..
03.
Accountability breaks in the chain.
When an agent calls a sub-agent, logs cannot say who authorized the action..
Identity tools check who signed in. Nobody checks what the agent does next..

From the PRD, The Problem.
1. They act, not just answer. Agents call tools, move data and trigger workflows on their own. They often chain to other agents with no human in the loop.
2. Their credentials are static and over-scoped. Long-lived API keys and shared service accounts give agents far more access than any single task needs. Those keys leak into prompts and code.
3. Accountability disappears in the chain. A human asks an agent, that agent asks a sub-agent, and the sub-agent calls an API. Today's logs cannot say who authorized what, or stop it mid-flight.

## Slide 6

The Security Gap Sits Between the Agent and Its Credentials.
THE HIDDEN SECURITY BOUNDARY.
Secure the identity behind the agent, not only the model inside it..

The chain runs Human identity, Agent identity, Workload credentials, MCP tools. The gap sits between the agent and the workload credentials it uses.
Key principle from the PRD: never let the agent say it is acting for User A become the authorization decision.
Always verify the identity-to-agent mapping on your own before you allow access to sensitive data or high-impact actions. Secure the identity behind the agent, not only the model inside it.

## Slide 7

Identity-to-Agent Mapping Is the Missing Layer.
WHAT HAS TO EXIST.
Verified identity plus scoped delegation plus least privilege equals trusted AI actions..

The identity-to-agent mapping layer binds a verified identity to an agent, with explicit delegation, credentials and policy context.
Identity sources: human identity (end user, employee, customer), agent identity (AI agent or service identity), service account (application or workload identity), delegated identity (on behalf of, temporary, external).
The layer does identity binding, delegation, policy context and an audit trail.
Authorization and policy: a policy engine checks if the mapped identity and agent can perform an action on a resource. RBAC, ABAC, least privilege, per-action checks.
Tools, APIs and resources: external tools, APIs, databases, applications and services. Tool allowlists, resource ACLs, tenant isolation.
Delegation and credentials: short-lived tokens, workload credentials and explicit delegation. OAuth and OIDC, scoped credentials, no implicit inheritance.
Security outcomes: correct identity binding, minimal permissions, controlled delegation, full auditability, tenant isolation.

## Slide 8

Five Attack Surfaces Open Up in the Mapping Gap.
ATTACK SURFACES.
Attack surface | What happens | Business impact
Identity confusion | The agent is tied to the wrong user | Spoofed identity, unauthorized actions
Privilege inheritance | Broad service accounts hand out too much access | Super NHIs with admin rights
Delegation abuse | Valid delegated credentials get misused | Compromise spreads across trust links
Cross-tenant leakage | One user's context reaches another user's agent | Data exposed across tenants
Stale authorization | Revoked permissions still work | Backdoors through forgotten API keys
Each surface turns one compromised agent into access across the business..

From the PRD, the 5 core attack surfaces of the mapping gap.
Identity confusion: the agent becomes associated with the wrong user. Impact: identity spoofing and unauthorized actions.
Privilege inheritance: the agent receives excessive permissions through broad service accounts. Impact: super NHIs with admin privileges.
Delegation abuse: legitimate delegated credentials are misused. Impact: cascading compromise across trusted relationships.
Cross-tenant leakage: one user's context bleeds into another user's agent. Impact: data exposure across isolated tenants.
Stale authorization: revoked permissions remain usable, the digital fossils. Impact: persistent backdoors through unmanaged API keys.

## Slide 9

Six Threats Target AI Agents Today.
THREAT MODEL.
Prompt injection.
Hostile text in inputs or tool output steers the agent.
Confused deputy.
The agent uses its broad rights for a user who lacks them.
Credential theft.
Keys leak into context, logs, repos or memory.
Shadow agents.
Unregistered agents, or agents that outlive their owner.
Tool and MCP poisoning.
Malicious or silently changed tools and servers.
Sandbox escape.
Agents break out to reach hosts, networks and data.
Mapped to OWASP Top 10 for LLM Applications and NIST AI RMF..

From the PRD threat model. What we defend against.
Prompt and indirect injection: hostile instructions in inputs, documents or tool output steer the agent.
Confused deputy: an agent uses its own broad privileges for a user who lacks them.
Credential theft and leakage: keys exposed in context windows, logs, repos or memory.
Shadow and orphaned agents: unregistered agents, or agents that outlive their owner or purpose.
Tool and MCP poisoning: malicious or silently changed tool descriptions and servers.
Sandbox escape and lateral movement: agents break out of their runtime to reach hosts, networks and data.
Reference frameworks: OWASP Top 10 for LLM Applications, OWASP agentic AI threat guidance, NIST AI RMF.

## Slide 10

Five Teams Need Answers About Every Agent.
WHO ASKS.
CISO.
Proof that every agent is known and stoppable.
IAM architect.
One Zero Trust policy for people and agents.
AI platform engineer.
Identity handled by default, not bolted on.
SOC analyst.
Full agent incident story, kill a chain fast.
GRC and compliance.
Controls mapped to EU AI Act, ISO 42001.
One platform answers all five, from the same identity record..

From the PRD personas.
CISO: needs proof that every agent is known, least-privileged and stoppable, in board and regulator language.
IAM or security architect: extends Zero Trust policy from humans and workloads to agents without a parallel stack.
AI platform engineer: ships agents fast and wants identity and credentials handled by default, not bolted on.
SOC analyst: investigates agent incidents end to end and kills a rogue chain in seconds.
GRC and compliance: maps agent controls to the EU AI Act, NIST AI RMF, ISO 42001 and SOC 2.

## Slide 11

PART 2 · CURRENT ALTERNATIVES.
Today's Tools Each Cover Part of the Problem.
Static keys, legacy IAM and point products leave the gap between the agent and its actions open..

Part 2 explains why the options teams use today do not close the identity-to-agent gap.

## Slide 12

A Credential's Lifetime Sets Its Blast Radius.
STATIC KEYS.
Identity must come from what a workload is, proven by attestation..

From the technical deck, the blast radius concept.
A long-lived API key gives months or years of exposure, no identity context, and no way to trace a specific actor.
A single-hop JWT or a SPIFFE SVID lives for minutes, uses eager connect-time authentication and rotates on its own.
Identity must come from what a workload is, proven by attestation. A static secret proves only that someone handed it over.
The circle areas show the contrast, not an exact ratio.

## Slide 13

Legacy IAM Fails on Credentials, Authorization and Visibility.
THE EXECUTIVE DECISION.
 | Legacy static IAM | AccuKnox agentic identity
Credentials | Long-lived API keys and static service accounts | Short-lived SPIFFE SVIDs, proven by workload attestation
Authorization | Assumes the user's rights, coarse access | Checks the caller chain with OpenFGA, narrows scope per hop
Visibility | Logs show only the final service account | RFC 8693 lineage from first prompt to final write
Static and blind.
Short-lived and traced.
Keep your IdP. Add the agent layer it was never built to cover..

From the PRD, the executive decision table.
Credentials. Legacy static IAM: long-lived API keys and static service accounts that turn into digital fossils. AccuKnox: ephemeral SPIFFE SVIDs anchored by continuous cryptographic workload attestation.
Authorization. Legacy: blind assumption of user privileges, coarse-grained access. AccuKnox: caller-chain evaluation with OpenFGA, enforcing scope attenuation at every delegation hop.
Visibility. Legacy: boundary blind spots, logs show only the final service account. AccuKnox: immutable RFC 8693 nested lineage, full forensic audit for fast AI-SOC response.

## Slide 14

Three Vendor Categories Each Leave a Gap Open.
COMPETITIVE LANDSCAPE.
IAM incumbents.
Okta, Microsoft Entra.
Strong identity.
Little runtime or prompt control.
NHI vendors.
Secrets and service accounts.
Good discovery.
Weak on delegation and behavior.
AI security platforms.
Posture and guardrails.
Strong AI context.
Often SaaS-only, gateway-bound.
No category ties identity, runtime enforcement and prompt defense together..

From the PRD competitive landscape.
IAM incumbents, for example Okta and Microsoft Entra, extend human and workload identity to agents. Strong identity. Limited runtime and prompt-layer enforcement.
Non-human identity (NHI) vendors focus on secrets and service-account hygiene. Good discovery. Weak on delegation chains and agent behavior.
AI security platforms, for example Zenity, cover agent posture, guardrails and prompt defenses. Strong AI context. Often SaaS-only and bound to a gateway.
The AccuKnox edge is on the next slide and in Part 6.

## Slide 15

PART 3 · THE ACCUKNOX SOLUTION.
Verify Every Agent and Every Action.
One control plane binds each agent to a verified identity, a scoped task and a full audit trail..

Part 3 shows the AccuKnox answer: the CISO mandate, the AgentZ control plane, the reference architecture and the request flow.

## Slide 16

Zero Trust for Agents Is One Unbroken Chain.
THE CISO MANDATE.
Verified human.
The person who starts the chain, tied to your IdP.
Attested agent.
Proof of what the workload is, not a secret it holds.
Scoped delegation.
Short-lived credentials that expire in minutes.
Least privilege.
Per-action rights on named MCP tools and APIs.
The mandate: an unbroken chain from the first prompt to the final write..

From the PRD, the CISO mandate for Zero Trust agentic identity.
Verified human identity: the human principal who starts the chain, tied to the enterprise IdP.
Attested agent identity: cryptographic proof of what the workload is, not only a static secret it holds.
Scoped delegation: short-lived, audience-bound credentials with strict TTLs under 15 minutes.
Least-privilege actions: granular, per-action authorization on specific MCP tools and APIs.
The mandate: an unbroken chain from the first prompt to the final write.

## Slide 17

AgentZ Puts Four Controls Around Every Agent.
THE ACCUKNOX ANSWER.
Agents never hold secrets. A prompt injection cannot leak what the agent never got..

From the PRD, the AccuKnox answer: the AgentZ control plane.
Identity and attestation: SPIFFE workload identity, with ModelKnox for model attestation.
Delegation and policy: OpenFGA relationship-based decisions and RFC 8693 delegation chains.
Execution guardrails: KubeArmor runtime enforcement and the stateful Prompt Firewall.
Credential broker: ephemeral access, scoped per task.
Positioning: evolutionary consolidation, not disruption. It sits as a control-plane layer directly above the existing infrastructure.
From accuknox.com/platform/agentz: agents never hold secrets. AgentZ injects scoped credentials at runtime and never stores them in the agent context, so a prompt injection cannot leak what the agent never receives.

## Slide 18

One Gateway Stands Between Every Agent and Every Tool.
REFERENCE ARCHITECTURE.
Your IdP stays the source of truth. AccuKnox adds the agent layer on top..

From the PRD reference architecture.
Humans and apps (users, services, schedulers) drive AI agents (agents, sub-agents, copilots).
Every agent call passes the AccuKnox Agent Identity Gateway: identity and attestation, credential broker, delegation, policy decision, prompt firewall, MCP gateway.
The gateway reaches tools and data: MCP servers, APIs, SaaS and databases.
Supporting services: the enterprise IdP (Okta, Entra) stays the system of record. Policy as code and the risk engine hold task scopes, risk tiers and simulation. The runtime sensor (KubeArmor eBPF) enforces at process, file and network level. Audit, lineage and AI-SOC write tamper-evident logs to SIEM and SOAR.

## Slide 19

Ten Capabilities Cover the Agent From Discovery to Kill Switch.
CAPABILITIES AT A GLANCE.
01.
Discovery and inventory.
02.
Verifiable identity.
03.
Secretless credentials.
04.
Delegation chains.
05.
Task-scoped access.
06.
Runtime authorization.
07.
Tool and MCP control.
08.
Prompt and memory.
09.
Human approval.
10.
Audit and kill switch.
Phase 1 sees and stops agents. Later phases scope and govern them at scale..

The top 10 capabilities from the PRD, in order. Part 4 covers each one.
01 Agent discovery and inventory: find and register every agent, sanctioned or shadow.
02 Verifiable agent identity: a unique, attested cryptographic identity per agent instance.
03 Secretless, short-lived credentials: remove static keys, broker short-lived tokens.
04 Delegation and on-behalf-of chains: carry the human principal through every hop.
05 Least-privilege, task-scoped authorization: just-in-time permissions that expire with the task.
06 Continuous runtime authorization: check every tool call, not only the login.
07 Tool and MCP governance: allowlist, pin and scope every tool and server.
08 Prompt, context and memory integrity: stop injected instructions from becoming actions.
09 Human-in-the-loop step-up: risk-tiered approvals for high-impact actions.
10 Audit, forensics and kill switch: full lineage, and revoke a rogue chain in seconds.
PRD priority: all P0 except 08 and 09, which are P1.

## Slide 20

PART 4 · TEN CAPABILITIES IN DEPTH.
Each Capability Closes One Gap.
Two capabilities per slide: why it matters, what it does, and the AccuKnox building blocks behind it..

Part 4 walks the ten capabilities in pairs. User stories and acceptance criteria from the PRD sit in each slide's notes.

## Slide 21

Know Every Agent and Prove Who It Is.
CAPABILITIES 01 AND 02.
01.
Discovery and inventory.
You cannot secure an agent you cannot see..
Finds agents in Kubernetes, cloud AI, SaaS and laptops.
Records owner, purpose, model, tools and data.
Flags orphaned agents and unused rights.
ACCUKNOX BUILDING BLOCKS.
AI-SPM.
CNAPP asset graph.
02.
Verifiable identity.
Shared accounts make every agent look the same..
One cryptographic ID per agent instance.
Bound to image, model, config and runtime.
Federates with Okta or Entra ID.
ACCUKNOX BUILDING BLOCKS.
AgentZ.
KubeArmor.
ModelKnox.

01 Agent discovery and inventory, P0.
Why it matters: agents are spun up by developers, embedded in SaaS copilots and run on laptops. Most never pass a security review.
User story: as a CISO, I want a live inventory of every agent, its owner and what it can reach, so shadow agents cannot operate unnoticed.
Core requirements: auto-discover agents across Kubernetes, cloud AI services, SaaS copilots and developer endpoints. Register each agent with owner, purpose, model, tools and data access. Flag orphaned agents (owner left, project ended) and unused privileges. Risk-score each agent from its access, exposure and behavior.
Acceptance criteria: every agent maps to a named human owner. Orphans alerted within 24 hours. Inventory exports to CMDB or SIEM.
02 Verifiable agent identity, P0.
Why it matters: Zero Trust starts with knowing exactly which agent, and which version, is asking.
User story: as an IAM architect, I want each agent instance to prove who it is and what code it runs before it gets anything.
Core requirements: issue a unique cryptographic identity per agent instance, SPIFFE and SVID-style workload identity. Bind identity to attestation: container image, model, prompt or config, and runtime hashes. Distinguish agent type, version and instance for policy and audit. Federate with the enterprise IdP rather than replacing it.
Acceptance criteria: no two agents share an identity. Every call carries a signed identity. A tampered image or config fails attestation.

## Slide 22

Give Agents No Standing Secrets and a Traceable Chain.
CAPABILITIES 03 AND 04.
03.
Secretless credentials.
Static API keys are the top cause of over-privilege..
Short-lived, audience-bound tokens only.
Rotates and revokes through your vaults.
Keeps secrets out of prompts and memory.
ACCUKNOX BUILDING BLOCKS.
AgentZ.
Secrets scanning.
04.
Delegation chains.
Agents act for people, and agents call agents..
Carries the human through every hop.
Scope can only shrink at each hop.
Covers agent-to-agent and MCP calls.
ACCUKNOX BUILDING BLOCKS.
AgentZ.

03 Secretless, short-lived credentials, P0.
Why it matters: static API keys are the single most common way agents get over-privileged and compromised. They leak into prompts, logs and memory.
User story: as a platform engineer, I want my agents to get credentials on their own and only for as long as they need them.
Core requirements: broker short-lived, audience-bound tokens, with no long-lived keys in agent code or context. Automatic rotation and revocation with existing vaults and cloud IAM. Detect hard-coded or pasted secrets in prompts, code and agent memory. Keep secrets out of the model's context window entirely.
Acceptance criteria: default token TTL 15 minutes or less, configurable. Static-key use flagged on first sight. Zero secrets present in agent context.
04 Delegation and on-behalf-of chains, P0.
Why it matters: without an unbroken chain you get confused-deputy attacks and no accountability.
User story: as a SOC analyst, I want every agent action tied to the human who started it, through every hop.
Core requirements: carry user to agent to sub-agent delegation with OAuth 2.0 Token Exchange (RFC 8693) actor claims. Attenuate scope at every hop, so a delegate never exceeds its delegator. Record consent and delegation grants with expiry. Support agent-to-agent (A2A) and MCP call paths.
Acceptance criteria: 100 percent of actions attributable to a human principal. Downstream scopes are a subset of upstream scopes, enforced. Delegation revocable mid-chain.

## Slide 23

Authorize Each Action, Not Only the Login.
CAPABILITIES 05 AND 06.
05.
Task-scoped access.
Agents get standing access just in case..
Just-in-time grants that expire with the task.
Policy as code with data, time and risk.
Right-sizing from usage, dry run first.
ACCUKNOX BUILDING BLOCKS.
AgentZ.
AI-SPM.
06.
Runtime authorization.
A trusted agent can be hijacked one prompt later..
A decision on every tool and API call.
Per-agent baseline blocks odd behavior.
Enforced at process, file and network level.
ACCUKNOX BUILDING BLOCKS.
KubeArmor.
AgentZ.

05 Least-privilege, task-scoped authorization, P0.
Why it matters: least privilege has to be per task, just-in-time and self-expiring.
User story: as an IAM architect, I want permissions granted for a task and gone when it ends, without writing policy by hand for every agent.
Core requirements: just-in-time, task-scoped grants that expire on completion or timeout. Policy as code (for example OPA or Cedar) with attribute and relationship context: data sensitivity, time, risk. Right-sizing recommendations from observed usage. Simulation or dry-run mode before enforcement.
Acceptance criteria: grants auto-expire at task end. Unused privileges surfaced weekly. Policies testable in simulation.
06 Continuous runtime authorization, P0.
Why it matters: authorization must happen on every action, all the time.
User story: as a CISO, I want every tool and API call checked in real time, with enforcement at the runtime and not only at the gateway.
Core requirements: real-time policy decision on every tool call, API request and data access. Behavioral baselining per agent, with anomalies that trigger step-down or block. Runtime enforcement at process, file and network level (eBPF and LSM). Block, alert and audit-only modes per policy.
Acceptance criteria: p99 decision latency target to be confirmed, under 25 ms proposed. Out-of-baseline actions blocked in enforce mode. Works in air-gapped clusters.

## Slide 24

Control the Tools Agents Use and the Text They Read.
CAPABILITIES 07 AND 08.
07.
Tool and MCP control.
A poisoned tool turns a helper into an attacker..
Registry and allowlist for MCP servers.
Signed, pinned manifests catch rug pulls.
Per-tool scopes and argument limits.
ACCUKNOX BUILDING BLOCKS.
AgentZ.
AI-SPM.
08.
Prompt and memory.
Injected text hijacks agents without stealing keys..
Stateful firewall tracks intent across turns.
Inspects retrieved content and tool output.
Catches memory poisoning, redacts data.
ACCUKNOX BUILDING BLOCKS.
Prompt Firewall.
DSPM.

07 Tool and MCP governance, P0.
Why it matters: tools are how agents touch the world. A poisoned tool description or rogue MCP server turns a helpful agent into an attacker.
User story: as a platform engineer, I want agents to use only approved tools, and to know when a tool changes underneath them.
Core requirements: registry and allowlist for MCP servers and tools, block unapproved ones. Sign and pin tool manifests, detect description changes (rug pulls). Per-tool scopes and argument-level constraints. An MCP gateway that enforces authorization on every call.
Acceptance criteria: unapproved MCP servers blocked. Tool definition changes require re-approval. Per-tool usage visible per agent.
08 Prompt, context and memory integrity, P1.
Why it matters: injected instructions in documents, web pages and tool output are how attackers hijack agents without touching credentials.
User story: as a security architect, I want injected instructions caught before they turn into tool calls or data exfiltration.
Core requirements: stateful prompt firewall that tracks intent across multi-turn sessions. Inspect retrieved content and tool outputs for indirect injection. Detect memory poisoning in long-term agent memory. Classify and redact sensitive data in prompts and responses.
Acceptance criteria: injection blocked before tool execution. Sensitive data redacted per policy. Session context retained across turns.

## Slide 25

Keep People in the Loop and Stop a Rogue Chain Fast.
CAPABILITIES 09 AND 10.
09.
Human approval.
Some actions are too big for autonomy alone..
Risk tiers by action, data and blast radius.
Approve in Slack, Teams, email or mobile.
Unanswered requests deny by default.
ACCUKNOX BUILDING BLOCKS.
AgentZ.
AI-SOC.
10.
Audit and kill switch.
When it goes wrong, you need the story and a stop..
Tamper-evident lineage to the data touched.
Exports to SIEM and SOAR, AI-SOC views.
Revokes an agent, a version or a chain.
ACCUKNOX BUILDING BLOCKS.
AI-SOC.
AgentZ.
KubeArmor.

09 Human-in-the-loop step-up, P1.
Why it matters: some actions are too consequential for autonomy alone, such as moving money, deleting data, changing privileges or contacting customers.
User story: as a CISO, I want high-risk agent actions to pause for a human, without slowing down routine work.
Core requirements: risk tiers per action type, data class and blast radius. Asynchronous approval through Slack, Teams, email or mobile (CIBA-style). Timeouts default to deny, with break-glass and full audit. Tune thresholds from approval history to cut noise.
Acceptance criteria: tiers configurable per agent and action. Unanswered approvals deny by default. Approval decisions logged with the approver.
10 Audit, forensics and kill switch, P0.
Why it matters: when something goes wrong, you need to rebuild exactly what happened and stop it at once across every agent in the chain.
User story: as a SOC analyst, I want a full lineage of an incident and a single control to quarantine a rogue agent chain.
Core requirements: tamper-evident lineage from request to delegation to tool call to data touched. Export to SIEM and SOAR, with native AI-SOC investigation views. Kill switch: revoke or quarantine an agent, a version or an entire chain. Compliance mapping to the EU AI Act, NIST AI RMF, ISO 42001 and SOC 2.
Acceptance criteria: full chain rebuildable per action. Revocation propagates in a time to be confirmed, under 60 seconds proposed. Evidence packs export for auditors.

## Slide 26

Every Request Passes Five Checkpoints.
HOW ONE REQUEST FLOWS.
The agent never carries the user's token to the tool. It gets a scoped one per call..

From the PRD, the complete agentic Zero Trust blueprint: eager auth, token exchange and CEL RBAC.
1. Connect: the enterprise client registers and authenticates once at connect time (eager auth).
2. Invoke: the autonomous agent tries to call a tool.
3. Exchange: the security token service handles impersonation, delegation and on-behalf-of exchange.
4. Authorize: a CEL RBAC policy filters the call. Example rule: request.auth.claims.act.sub contains 'finance-agent'.
5. Execute: a scoped, audited token reaches the SaaS MCP server.
Steps 2 to 5 run inside the trust domain and security perimeter.

## Slide 27

On-Behalf-Of Exchange Keeps the User on Every Hop.
EXAMPLE WITH ENTRA ID.
The tool sees the original user and a narrow scope, never the broker token..

From the PRD: set up OAuth 2.0 on-behalf-of token exchange with Entra ID.
1. User and client: the developer signs in from an MCP client with authorization code and PKCE.
2. Entra ID, the IdP and authorization server: OIDC authentication with OAuth 2.1 and PKCE, custom auth server, signing keys and JWKS, scopes and claims, access policies, trusted servers. It issues the broker JWT.
3. AccuKnox Agent Fabric, the agent gateway. Inbound, it validates the JWT: signature, issuer, audience, expiration, scope. Outbound, it runs the on-behalf-of token exchange (RFC 8693) and injects the delegated JWT.
4. The protected MCP resource gets only the delegated JWT.
Planner agent broker JWT: audience api://planning-agent-broker, scope Planner Agent Broker Invoke, subject the user.
MCP server delegated JWT: audience api://MCPServer, scope MCP Server Invoke, subject the original user, client Broker OBO Client.
Rule: never forward the planner agent broker JWT downstream.

## Slide 28

Authorization Follows the Whole Caller Chain.
WORKED EXAMPLE.
Same user, different agent path, different rights. OpenFGA makes that call..

From the technical deck. When a request reaches the AI gateway, it may have passed several agents. The decision depends on which agents were in the path. This is unique to agentic AI.
Do not assume the principal's permission for the AI agent.
Decision inputs: the principal (the user the request acts for), the upstream caller sequence (every agent the request passed), and the target resource (the MCP server or tool).
Example rules from the multi-cloud scenario. The user has read and write rights on the GitHub repository.
Target GitHub MCP server, principal User-1, upstream Coder agent: read on all repos.
Target GitHub MCP server, principal User-1, upstream Remediation agent then Coder agent: read-only repos, read-write PRs.
Target ServiceNow MCP server, principal User-1, upstream Remediation agent then Security agent: read-write tickets.
Lineage is kept as a signed delegation-and-receipt system, not a mutable HTTP header stack. Each hop binds to an authenticated workload identity.

## Slide 29

Four Layers Carry One Identity Proof From the Workload Up.
THE AGENTIC MESH STACK.
An agent proves what it is once, at Layer 1. Every layer above reuses that proof..

From the PRD and the technical deck, the agentic mesh stack. Read it bottom up.
Layer 1, workload identity anchor: the SPIRE server issues the SVID that every layer above trusts.
Layer 2, ambient service mesh: every hop authenticated without a sidecar per pod, with L4 mTLS.
Layer 3, translation and control: the MCP gateway and security token service route MCP auth and mint single-hop JWTs per call.
Layer 4, enterprise identity: dual IdP setup with Keycloak for internal OIDC and Microsoft Entra ID for the cloud domain.
An agent proves what it is at Layer 1, and every layer above reuses that proof.

## Slide 30

Deploy Anywhere and Keep the Identity Stack You Have.
PLATFORM.
SaaS.
Customer VPC.
Private cloud.
Air-gapped.
OPEN STANDARDS.
SPIFFE and SVID.
OAuth 2.1.
RFC 8693.
OpenID Connect.
MCP authorization.
WORKS WITH YOUR STACK.
Okta.
Entra ID.
Vault.
Splunk.
Sentinel.
Slack.
Teams.
Same features in every deployment, no phone-home. Prompts and data stay with you..

From the PRD non-functional requirements.
Deployment: SaaS, customer VPC, private cloud and fully air-gapped, with the same feature set and no phone-home.
Standards: SPIFFE and SVID, OAuth 2.1, RFC 8693 token exchange, OpenID, MCP authorization spec.
Integrations: Okta, Entra, Ping. HashiCorp Vault and cloud KMS. Splunk and Microsoft Sentinel. Slack and Teams.
Privacy and sovereignty: prompts and data stay in the customer's boundary, with configurable retention and redaction.
Scale target: tens of thousands of agent instances and millions of tool calls per day per tenant. Performance target: p99 policy latency under 25 ms proposed, no single point of failure. Both are PRD targets, not shipped numbers.

## Slide 31

Identity Plugs Into the Full AccuKnox AI Security Platform.
BEYOND IDENTITY.
AI-SPM and AIBOM.
Every model, agent and MCP server.
Prompt Firewall.
Stops injection and data leaks.
KubeArmor sandbox.
Kernel-level limits per agent.
AI-SOC.
Investigates agent incidents.
DSPM.
Knows the data agents touch.
CIEM.
Cloud identities and their risk.
PROMPT FIREWALL COVERS SAAS, CLOUD, DEV AND LOCAL AGENTS.
ChatGPT.
Claude.
Gemini.
Copilot.
AgentCore.
LangGraph.
n8n.

Agent identity is one layer of the AccuKnox AI security platform. The other layers share the same control plane and inventory.
AI-SPM and AIBOM: an AI bill of materials across managed and unmanaged AI assets, native integration with most model providers, CycloneDX v1.7 format. Source: technical deck, AI asset inventory slide.
Prompt Firewall: covers SaaS AI apps (Claude.ai, chatgpt.com, gemini.google.com, Microsoft Copilot, GitHub Copilot), cloud agents (Azure Copilot Studio and Power Apps, AWS Bedrock AgentCore, GCP Agents Platform), dev agents (Claude Code, Codex, Antigravity) and local agents (LangGraph, n8n and others). Five integration modes: browser plugin, gateway proxy, SDK or proxy mode, cloud SDK or API gateway, and Purview for Microsoft Copilot agents.
KubeArmor sandbox: process, filesystem, credential and network isolation for agents and MCP servers, at the kernel with eBPF.
AI-SOC: triage and investigation across cloud, identity and AI workloads.
DSPM: classifies the data agents can reach.
CIEM: cloud IAM users, roles and groups with risk class. Covered next.

## Slide 32

PART 5 · CIEM IN THE PRODUCT.
See Every Cloud Identity and the Access It Holds.
AccuKnox CIEM lists human and machine identities across four clouds and traces each one to its policies..

Part 5 shows AccuKnox CIEM screens from help.accuknox.com. CIEM covers cloud IAM identities today, the same machine identities agents run on.

## Slide 33

CIEM Lists Every Cloud Identity With Its Risk.
CIEM · IDENTITY LIST.
Identities > CIEM, list view filtered to AWS.
AWS.
GCP.
Azure.
OCI.
Users, groups and roles in one list.
Each one marked human or machine.
Risk class from attached policies.
Last used and age show stale access.
Next release.
Privilege escalation and data exfiltration risk shows on each identity row..

Source: help.accuknox.com, Cloud Infrastructure Entitlement Management (docs/getting-started/ciem-overview.md).
CIEM lists the users, groups and roles in AWS, GCP, Azure and Oracle Cloud Infrastructure accounts. For each identity it shows the attached policies, the risk classes those policies carry, and the last time the identity was used.
Each identity is classed human or machine. A CI/CD pipeline account is a machine identity.
Risk class examples: privilege escalation, data exfiltration, credentials exposure, infrastructure modification.
Lifecycle columns: age in days, created at, created by, last used, days since last used.
Where to find it: Identities, then CIEM, in the left navigation.
Status: the help page marks CIEM as coming soon in a newer AccuKnox version. Screens come from the current build and can change. CIEM supports standalone cloud accounts today, not organization accounts.
Screenshot: ciem-identity-list.png, account values redacted in the source.

## Slide 34

The Access Graph Shows Where Each Permission Comes From.
CIEM · IDENTITY DETAIL.
Access Graph tab: one user, its groups, and the policies they grant.
Identity to group to policy.
Read each policy as JSON.
Findings by severity.
Related identities in the account.
Trace an excess permission to the exact group or policy that granted it..

Source: help.accuknox.com CIEM overview.
Select an identity in the list. A panel opens with four tabs: Overview, Access Graph, Related Identities and Raw Information.
Access Graph: the identity sits at the top, its groups in the middle, and the policies each group grants at the bottom. A policy attached straight to the identity sits in the same row as the groups. It shows which permissions reach the identity and through which group.
Overview: identity details, total findings by severity (Critical, High, Medium, Low), and the attached policies. Expand a policy row to read the policy document as JSON. Policy types: cloud managed, inline policy, user managed.
Screenshots: ciem-identity-graph.png and ciem-identity-overview.png, cropped to the side panel. Identity names are redacted in the source.

## Slide 35

One Graph Maps Every User, Group, Role and Policy.
CIEM · ORGANIZATION GRAPH.
Organization graph for one AWS account.
77 users.
22 groups.
637 roles.
504 policies.
Sample AWS account. Roles outnumber users 8 to 1..
CIEM covers cloud identities today. Agentic identity extends it to every AI agent..

Source: help.accuknox.com CIEM overview.
Select the graph icon at the top right of Identities, CIEM. Filter by cloud provider and cloud account name.
The cloud account node sits at the top, with one node each for users, groups, roles and policies. The badge on each node is the count. In the sample AWS account on the help page, the badges read 77 users, 22 groups, 637 roles and 504 policies. Select a node to expand its members, then a member to open its access graph.
Bridge to the agentic story: roles far outnumber users in the sample account, the same machine-identity pattern behind the 82 to 1 ratio. Agentic identity security extends the same visibility and control to AI agents.
Screenshot: ciem-org-graph.png.

## Slide 36

PART 6 · WHY ACCUKNOX.
Identity and Runtime Enforcement in One Platform.
Four differentiators, a category comparison, the outcomes you can prove, and the live demo..

Part 6 closes on the key differentiators and the proof.

## Slide 37

Four Differentiators Set AccuKnox Apart.
KEY DIFFERENTIATORS.
Identity plus runtime.
KubeArmor eBPF enforces each decision at process, file and network level.
Stateful prompt firewall.
Patent pending. Tracks intent across multi-turn sessions.
Air-gapped and sovereign.
Same features in SaaS, VPC, private cloud or offline.
Cloud, AI and data context.
CNAPP, AI-SPM and DSPM feed every identity decision.
Built on open standards: SPIFFE for identity and OpenFGA for authorization..

From the PRD, the AccuKnox edge.
1. Identity plus runtime enforcement in one platform, through KubeArmor eBPF. Decisions are enforced at process, file and network level, not only at a gateway.
2. Stateful prompt firewall, patent pending. It tracks intent across multi-turn sessions.
3. Air-gapped and sovereign deployment. SaaS, customer VPC, private cloud or fully air-gapped, with the same feature set and no phone-home.
4. CNAPP, AI-SPM and DSPM context. Agent identity decisions use the cloud, AI asset and data context AccuKnox already collects.
Built on open standards: SPIFFE for identity and OpenFGA for fine-grained authorization (accuknox.com/solutions/agentic-ai-security).

## Slide 38

AccuKnox Covers What Each Category Leaves Out.
CATEGORY COMPARISON.
Capability | IAM incumbents | NHI vendors | AI security | AccuKnox
Verified agent identity | Yes | Partial | Partial | Yes
Agent and NHI discovery | Partial | Yes | Yes | Yes
Delegation chain control | Partial | No | Partial | Yes
Kernel runtime enforcement | No | No | No | Yes
Prompt-layer defense | No | No | Yes | Yes
Air-gapped deployment | Partial | Partial | No | Yes
Only AccuKnox ties identity, kernel enforcement and prompt defense together..

Category-level view built from the PRD competitive landscape. It compares vendor categories, not named products.
IAM incumbents: strong identity, limited runtime and prompt-layer enforcement.
NHI vendors: good discovery, weak on delegation chains and agent behavior.
AI security platforms: strong AI context, often SaaS-only and gateway-bound.
Partial means some vendors in the category offer it, or it works only at one layer such as a gateway.
Validate each cell with product marketing before this slide goes to a public page.

## Slide 39

Five Outcomes a CISO Can Prove to the Board.
OUTCOMES.
Every agent known and owned.
No static secrets on agents.
Every action tied to a human.
A rogue chain stopped at once.
Evidence for EU AI Act, ISO 42001.
Trust nothing. Verify every agent..

Outcomes drawn from the PRD goals and acceptance criteria.
Every agent known and owned: every agent maps to a named human owner, and orphans are flagged.
No static secrets on agents: short-lived, task-scoped credentials by default.
Every action tied to a human: delegation chains carry the human principal through every hop.
A rogue chain stopped from one control: revoke or quarantine an agent, a version or an entire chain.
Evidence for auditors: control mapping to the EU AI Act, NIST AI RMF, ISO 42001 and SOC 2, with evidence packs.
The PRD proposes numeric targets for these outcomes. They sit on a hidden backup slide and are not commitments.

## Slide 40

See Multi-Cloud Agent Chains Run Under Policy, Live.
DEMO AND NEXT STEPS.
WHAT THE DEMO SHOWS.
Authorization rules enforced per call.
Agent chains across AWS and Google Cloud.
SPIFFE identity for every agent.
One console view across clouds.
AgentCore.
Google ADK.
On-prem K8s.
Next steps.
1.
Pick the first agent workflows to protect.
2.
Run a design-partner pilot on them.
3.
Map the controls to your frameworks.
Book a demo at accuknox.com/demo.

Demo scope, from the technical deck.
Showcase authorization rules enforcement.
Showcase cascaded multi-cloud agent calls and the authorization rules based on them. The Remediation and Coder agents run on AWS AgentCore, and the Security agent runs on Google ADK. Every call passes the on-prem AI gateway in Kubernetes.
Showcase SPIFFE for identity.
Showcase visibility across AWS, GCP and on-prem agents from the AccuKnox console.
Next steps for the customer: pick the first agent workflows to protect, run a design-partner pilot on them, and map the controls to your frameworks.
Watch: AgentZ launch film youtube.com/watch?v=mAzLWcr59g0 and the Kubernetes live demo with Rahul Jadhav, CTO, youtube.com/watch?v=dX1sO3sOoFI.

## Slide 41

SEE US IN ACTION.
support@accuknox.com.

## Slide 42

Backup: The PRD Sets Five Goals and Four Non-Goals.
BACKUP · SCOPE.
Goals.
▸  Every agent has a verifiable, owned identity ▸  No static secrets by default ▸  Every action authorized and tied to a human ▸  One policy model for people, workloads, agents ▸  Deploy in SaaS, private cloud or air-gapped.
Non-goals for v1.
▸  Replacing Okta or Entra, AccuKnox federates ▸  Building an agent framework ▸  Judging model quality or accuracy ▸  Consumer agent identity.

Hidden backup. From the PRD scope slide, goals and non-goals for v1. Internal planning material, keep it out of customer sessions unless asked.

## Slide 43

Backup: Proposed Targets for Design Partners to Validate.
BACKUP · SUCCESS METRICS.
Coverage.
▸  95% or more of running agents discovered and owned ▸  100% of P0 agents free of static secrets ▸  100% of actions tied to a human.
Speed.
▸  Under 60 s mean time to revoke a rogue chain ▸  Under 25 ms p99 inline policy decision ▸  Under 5% of human approvals judged unnecessary.

Hidden backup. From the PRD success metrics. These targets are proposals for validation with design partners, not commitments. Never present them as shipped performance.

## Slide 44

Backup: Three Phases Deliver the Ten Capabilities.
BACKUP · ROADMAP.
Phase 1, 0 to 90 days.
▸  See it and stop it ▸  01 Discovery and inventory ▸  02 Verifiable identity ▸  03 Secretless credentials ▸  07 Tool and MCP control ▸  10 Audit and kill switch.
Phase 2, 90 to 180 days.
▸  Scope it, verify every action ▸  04 Delegation chains ▸  05 Task-scoped access ▸  06 Runtime authorization ▸  08 Prompt and memory.
Phase 3, 180 to 360 days.
▸  Govern it at scale ▸  09 Human approval ▸  Advanced approval tuning ▸  Cross-tenant agent federation ▸  Compliance evidence packs.

Hidden backup. From the PRD phased roadmap. Internal plan, dates count from project start and are not customer commitments.

## Slide 45

Backup: Open Risks and Questions in the PRD.
BACKUP · TO RESOLVE.
Risks.
▸  Inline latency slows agents and drives bypass ▸  MCP auth, A2A and agent ID specs still move ▸  Approval fatigue erodes human review ▸  IdP vendors bundle good-enough agent identity.
Open questions.
▸  Which 3 to 5 design partners and frameworks first ▸  Gateway first, sidecar first, or both at GA ▸  Pricing unit: per agent, action or workload ▸  How deep to go with Okta and Entra agent ID ▸  Minimum viable air-gapped package.

Hidden backup. From the PRD risks and open questions. Internal only.