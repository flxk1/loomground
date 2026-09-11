# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2026 flxk1
"""documents in -> grounded claims -> policy -> verdict -> human decision -> signed proof, verified offline."""
import base64, csv, hashlib, json, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
import five_d_nd
from governance_certification import verify as gv
from oversight_certificate import Aid, Assistance, Disposition, Human, OversightCertificate, issue, verify as ov_verify

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
BIN = Path(sys.executable).parent
canon = lambda d: json.dumps(d, separators=(",", ":"), sort_keys=True).encode()
sk = Ed25519PrivateKey.generate(); pk = sk.public_key()
def verify_sig(m, s):
    try: pk.verify(s, m); return True
    except InvalidSignature: return False

# 1 ground: index the documents folder with the law-eu profile; every claim carries its span
subprocess.run([BIN / "versum", "index", HERE / "docs", "--profile", "law-eu", "--out", OUT / ".versum"], check=True, capture_output=True)
claims = list(csv.DictReader(open(OUT / ".versum/claims.csv")))
p = next(c for c in claims if c["marker"] == "must not")
ref = f'{p["source_urn"]}#{p["unit_id"]}:{p["span_start"]}-{p["span_end"]}'
print(f"1 grounded   {len(claims)} claims, markers {sorted(c['marker'] for c in claims)}; cited span {ref[:24]}...{ref[-20:]}")
print(f"             {p['text']}")

# 2 policy: high-risk transfers are reserved to a human of role legal
policy_fp = hashlib.sha256((HERE / "policy.lg").read_bytes()).hexdigest()[:16]
print(f"2 policy     policy.lg fingerprint {policy_fp}")

# 3 verdict: the agent proposes a high-risk transfer, citing the span
token = {"id": "t1", "kind": "data_transfer", "risk": "high", "party": "customer-42", "provenance": [ref]}
(OUT / "transport.json").write_text(json.dumps({"activations": [{"actor": "agent", "source": "transfer", "token": token}], "expected": {}, "log": []}))
subprocess.run([BIN / "loomground-solver", "loomground", "policy.lg", "--transport", "out/transport.json", "-o", "out/verdict.json"], cwd=HERE, check=True, capture_output=True)
v = json.loads((OUT / "verdict.json").read_text()); gate = v["trace"]["evaluation"]["transfer"]
print(f"3 verdict    status={v['status']} gate=transfer verdict={gate['verdict']} master={gate['master']} undecided={v['undecided']}")

# 4 decision: the dpo decides the reserved action; the certificate is signed, then re-checked offline
now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
cert = OversightCertificate(id="ov-0001", action="data_transfer:t1", disposition=Disposition.DECIDED, at=now, basis=ref, evidence=(ref,),
                            human=Human(id="dpo", qualification="data-protection-officer", credential_not_after="2027-01-01T00:00:00Z"),
                            assistance=Assistance(Aid.UNAIDED))
ov = issue(cert, canonicalize=canon, sign=sk.sign, keyid="k1").to_dict()
(OUT / "oversight.dsse.json").write_text(json.dumps(ov, indent=1))
rep = ov_verify(ov, canonicalize=canon, verify_sig=verify_sig, now=now)
print(f"4 oversight  ov-0001 decided by dpo; verify ok={rep.ok} findings={[f.code for f in rep.findings]} independence={rep.independence.value}")

# 5 proof: five pillars in one in-toto statement, DSSE-signed, verified by the reference verifier from the public key alone
gref = {"dimensions": ["temporal", "relational"], "anchor": ref}
assert five_d_nd.validate(gref)
grounded = {"scheme": "https://loomground.org/grounding/5d+nd/v1", "ref": gref, "digest": five_d_nd.digest(gref)}
predicate = {"verdict": "hold-approved", "action_class": "data_transfer", "issued_at": now,
             "enforced": {"mechanism": "loomground-solver:gate", "blocked_unless_permitted": True, "decision_ref": "out/verdict.json#transfer"},
             "overseen": {"required": True, "disposition": "DECIDED", "qualifier": "dpo", "oversight_certificate": ov},
             "grounded": grounded,
             "intact": {"type": "native-chain", "log_id": "end-to-end", "entry_ref": "out/verdict.json", "algorithm": "ed25519+sha256"},
             "legitimate": {"policy_id": "policy.lg", "policy_fingerprint": policy_fp, "anchors": [grounded]}}
stmt = {"_type": "https://in-toto.io/Statement/v1", "subject": [{"name": "data_transfer:t1", "digest": {"sha256": hashlib.sha256(canon(token)).hexdigest()}}],
        "predicateType": gv.PREDICATE_TYPE, "predicate": predicate}
body = canon(stmt)
env = {"payloadType": gv._DSSE_PAYLOAD_TYPE, "payload": base64.b64encode(body).decode(),
       "signatures": [{"keyid": "k1", "sig": base64.b64encode(sk.sign(gv._pae(gv._DSSE_PAYLOAD_TYPE, body))).decode()}]}
(OUT / "govcert.dsse.json").write_text(json.dumps(env, indent=1))
(OUT / "pub.pem").write_bytes(pk.public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo))
r = subprocess.run([BIN / "govcert-verify", "--pubkey", "pub.pem", "govcert.dsse.json"], cwd=OUT, capture_output=True, text=True)
print(f"5 proof      govcert-verify exit={r.returncode} {' '.join((r.stdout + r.stderr).split())}")
print("out/         .versum/claims.csv transport.json verdict.json oversight.dsse.json govcert.dsse.json pub.pem")
sys.exit(r.returncode)
