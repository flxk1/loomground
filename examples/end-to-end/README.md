<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 flxk1 -->
# end-to-end

Documents in, verified proof out. One script, five steps; every artifact lands in `out/`.

```bash
pip install cryptography jsonschema \
  "loomground-governance @ git+https://github.com/flxk1/loomground-governance" \
  "loomground-deontic @ git+https://github.com/flxk1/loomground-deontic" \
  "loomground-versum @ git+https://github.com/flxk1/loomground-versum" \
  "loomground-solver @ git+https://github.com/flxk1/loomground-solver" \
  "5d-nd @ git+https://github.com/flxk1/5d-nd" \
  "oversight-certificate @ git+https://github.com/flxk1/oversight-certificate" \
  "governance-certification @ git+https://github.com/flxk1/governance-certification"
python run.py
```

`loomground-governance` and `loomground-deontic` are dependencies of versum and solver; neither is on PyPI, so both are installed from git.

| step | package | out |
|---|---|---|
| 1 ground | loomground-versum | `out/.versum/claims.csv`: 3 claims, each with its span |
| 2 policy | loomground | `policy.lg`: high-risk transfers reserved to role legal |
| 3 verdict | loomground-solver | `out/verdict.json`: `reserved`, master withheld |
| 4 decision | oversight-certificate | `out/oversight.dsse.json`: signed human decision, re-checked offline |
| 5 proof | governance-certification, 5d-nd | `out/govcert.dsse.json`: five pillars, schema-checked, `govcert-verify` OK |

Executed 2026-09-11 against the main branches (versum 0.13.0, solver 0.5.0, governance 0.11.0, deontic 0.2.0, 5d-nd 0.1.0, oversight-certificate 0.2.0, governance-certification 0.1.0):

```
in : docs/policy.md — three sentences: must · may · must not
     policy.lg — gate transfer risk high grant agent · reserve data_transfer by legal when risk >= high
out: 1 grounded   3 claims, markers ['may', 'must', 'must not']; cited span urn:dls:sha256:4af9f2edd...a1090#para-1:225-315
                  The operator must not transfer personal data outside the EU without a transfer mechanism.
     2 policy     policy.lg fingerprint 70806e430a242e8f
     3 verdict    status=escalate gate=transfer verdict=reserved master=withhold undecided=['t1']
     4 oversight  ov-0001 decided by dpo; verify ok=True findings=[] independence=unaided
     5 proof      govcert-verify exit=0 OK
     out/         .versum/claims.csv transport.json verdict.json oversight.dsse.json govcert.dsse.json pub.pem
```
