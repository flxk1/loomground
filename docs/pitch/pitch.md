# The pitch — card text (edit here; one card per block; [brackets] = the highlighted words)

## 1 · the problem
H: Governance should not fragment on the [demand side.]
Body: Agent capabilities scale on the supply side. Add a second agent from a second provider and your rules are written twice, in two formats. 
Limit: You can run the same agent everywhere. Your rules cannot follow it easily.

## 2 · where the rules live
H: One rule, written [six ways.]
List: policy documents · system prompts · workflow code · access settings · model safeguards · approval steps
Limit: Each can be checked on its own. None can be checked against another.

## 3 · the task travels
H: The task travels. The rule stays where [it was written.]
Mono: you → agent A → agent B → tool
Body: "Negotiate this contract. Never accept unlimited liability. Ask me before you say yes." Agent A hands the negotiation to agent B. B receives the contract, the task, perhaps the authority. Nothing carries the two rules from A to B.
Limit: API, MCP and A2A carry the task and the data. How to carry the rule easily?

## 4 · the test
H: An agent cannot hold more authority [than its principal.]
Boxes: principal: level 2 · agent acting for it: asks level 4 · result: refused
Body: Level: how much an agent may do without asking a person.
Limit: This is why the principal gets to set the rules.

## 5 · the line
H: One line says who decides, [and when.]
Body: Sending data out at high risk is held for human review:
Mono: reserve data_transfer by human_review when risk >= high
Stamp: HELD FOR HUMAN REVIEW
Body: Loomground is the small open language this line is written in. A reviewer reads it as a rule. A program runs it as a decision and keeps a record.
Limit: It says who decides. It does not judge whether the risk is high or whether the rule is wise.

## 6 · bring your own governance
H: Write the rule once. Every agent reads it [the same way.]
Mono: today: provider A → its settings / provider B → its settings / instead: you → your rules → A, B, C
Body: The rules stay when you change the provider. They go with a task when it is handed on.
Limit: A rule between two parties cannot belong to one of them. So the language is open.

## 7 · the call
H: Open source. Install it, test it, get in touch.
Body: A small side project. The specification, the test cases and two implementations are on GitHub, free to use. 
Link: github.com/flxk1/loomground. 
Whitepaper: http://github.com/flxk1/thoughts