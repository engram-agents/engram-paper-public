"""Orchestrates the full pipeline (pre-reg §5 sampling -> §4/§4.1 packet
extraction -> §8.0 K* computation -> self-contained output for judge
fairies).

Usage:
    python -m compression_fidelity --db /path/to/knowledge.db --out ./out

Output layout (self-contained — no DB, no MCP, no network needed to read it):
    out/
      manifest.json                        sample composition, natural-frame
                                            counts, K* + tier assignments,
                                            redaction summary, exclusions,
                                            without-interpretation membership,
                                            AND the packet_id <-> node_id map
                                            (researcher-side only — see below)
      redaction_log.jsonl                  one line per redaction hit
                                            (keyed by real node_id — researcher
                                            debugging surface, not served)
      exclusions.json                      excluded items, by real node_id +
                                            packet_id + reason (researcher-side)
      packets/primary/<packet_id>.json     all sampled items (with interpretation)
      packets/without_interpretation/<packet_id>.json
                                            the ~50% stratified subsample,
                                            interpretation stripped

**Packet IDs are opaque (reviewer-fairy catch #1, fixed).** `packets/*/*.json`
filenames AND each packet's own `packet_id` field use an opaque
`pkt_NNNNN` serial (`sampling.assign_packet_ids`), never the real ENGRAM
node ID — a raw node ID inside a served packet would let a
partially-unisolated judge fairy call `engram_inspect(<id>)` directly,
defeating the pre-reg's §3 harness-isolation defense-in-depth. The
`packet_id <-> node_id` mapping lives ONLY in `manifest.json` (which is a
researcher-side output, not something handed to judge fairies) — never in
a packet file itself.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from . import binning, db, depth as depthmod, kstar, packet as packetmod, sampling
from .constants import DERIVATION_TYPES, OBSERVATION_TYPES


def run(
    db_path: str,
    out_dir: str,
    seed: int = sampling.DEFAULT_SEED,
    per_cell_target: int = sampling.PER_CELL_TARGET,
    deep_tier_cap: int = sampling.DEEP_TIER_CAP,
) -> dict:
    out = Path(out_dir)
    (out / "packets" / "primary").mkdir(parents=True, exist_ok=True)
    (out / "packets" / "without_interpretation").mkdir(parents=True, exist_ok=True)

    conn = db.connect(db_path)
    frame_nodes = db.fetch_frame(conn)
    node_types = db.fetch_all_node_types(conn)
    premises = db.fetch_all_derives_from(conn)
    depth_map = depthmod.compute_depth_map(node_types, premises)
    node_by_id = {n.id: n for n in frame_nodes}

    sample_result = sampling.draw_stratified_sample(
        frame_nodes, depth_map, seed=seed,
        per_cell_target=per_cell_target, deep_tier_cap=deep_tier_cap,
    )

    # Opaque packet-ID assignment (reviewer-fairy catch #1) — this mapping
    # is the ONLY place the real node_id and the served packet_id are ever
    # linked; it goes into manifest.json (researcher-side), never into a
    # packets/*/*.json file.
    packet_id_map = sampling.assign_packet_ids(sample_result.sampled_ids, seed)

    cache = packetmod.tree.GraphCache(conn)

    all_hits = []
    exclusions = []
    primary_packets = {}
    stripped_packets = {}

    without_interp_set = set(sample_result.without_interpretation_ids)

    for node_id in sample_result.sampled_ids:
        node = node_by_id[node_id]
        packet_id = packet_id_map[node_id]

        primary_result = packetmod.build_packet(cache, node, packet_id, include_interpretation=True)
        all_hits.extend(primary_result.redaction_hits)
        if primary_result.excluded:
            exclusions.append({
                "node_id": node_id, "packet_id": packet_id, "arm": "primary",
                "reason": primary_result.exclusion_reason,
                "token_count": primary_result.token_count,
                "chain_redaction_fraction": round(primary_result.chain_redaction_fraction, 4),
            })
        else:
            primary_packets[node_id] = primary_result.packet
            (out / "packets" / "primary" / f"{packet_id}.json").write_text(
                json.dumps(primary_result.packet, indent=2, ensure_ascii=False)
            )

        if node_id in without_interp_set:
            stripped_result = packetmod.build_packet(
                cache, node, packet_id, include_interpretation=False
            )
            all_hits.extend(stripped_result.redaction_hits)
            if stripped_result.excluded:
                exclusions.append({
                    "node_id": node_id, "packet_id": packet_id, "arm": "without_interpretation",
                    "reason": stripped_result.exclusion_reason,
                    "token_count": stripped_result.token_count,
                    "chain_redaction_fraction": round(stripped_result.chain_redaction_fraction, 4),
                })
            else:
                stripped_packets[node_id] = stripped_result.packet
                (out / "packets" / "without_interpretation" / f"{packet_id}.json").write_text(
                    json.dumps(stripped_result.packet, indent=2, ensure_ascii=False)
                )

    # K* computed on the FROZEN SAMPLE's computed confidence (pre-reg §8.0:
    # "Pool the FROZEN SAMPLE's ... confidence values"). Judgment call
    # (flagged in handoff): "frozen sample" is read here as the sample AFTER
    # packet-extraction exclusions (§12 step 4, "item set frozen (counts
    # recorded)", comes right after step 3's extraction+validation) — i.e.
    # the set actually served to judges, not the initial stratified draw
    # before exclusions were known. Nodes excluded from the PRIMARY arm
    # (redaction-gutted or over-size) are dropped from the K* pool; a node
    # excluded only from the without-interpretation arm still counts (it's
    # still served, just not in that sensitivity arm).
    excluded_from_primary = {
        e["node_id"] for e in exclusions if e["arm"] == "primary"
    }
    scored_ids = [
        nid for nid in sample_result.sampled_ids
        if node_by_id[nid].confidence is not None and nid not in excluded_from_primary
    ]
    scores = [node_by_id[nid].confidence for nid in scored_ids]
    k_result = kstar.compute_k_star(scored_ids, scores)

    redaction_by_category: dict[str, int] = {}
    for h in all_hits:
        redaction_by_category[h.category] = redaction_by_category.get(h.category, 0) + 1

    frame_totals = {
        "observation": len([n for n in frame_nodes if n.type in OBSERVATION_TYPES]),
        "derivation": len([n for n in frame_nodes if n.type in DERIVATION_TYPES]),
    }
    frame_totals["total"] = frame_totals["observation"] + frame_totals["derivation"]

    sample_totals = {
        "observation": len([nid for nid in sample_result.sampled_ids if node_by_id[nid].type in OBSERVATION_TYPES]),
        "derivation": len([nid for nid in sample_result.sampled_ids if node_by_id[nid].type in DERIVATION_TYPES]),
    }
    sample_totals["total"] = sample_totals["observation"] + sample_totals["derivation"]

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_db": str(Path(db_path).resolve()),
        "seed": seed,
        "per_cell_target": per_cell_target,
        "deep_tier_cap": deep_tier_cap,
        "frame_totals": frame_totals,
        "sample_totals": sample_totals,
        "cell_counts": {
            "frame": sample_result.frame_cell_counts,
            "sampled": sample_result.sampled_cell_counts,
        },
        "deep_tier": {
            "frame_count": sample_result.deep_tier_frame_count,
            "sampled_count": sample_result.deep_tier_sampled_count,
            "cap": deep_tier_cap,
            "reduced_by_sampling": sample_result.deep_tier_reduced,
        },
        "k_star": {
            "k_star": k_result.k_star,
            "k_requested_max": k_result.k_requested_max,
            "degenerate_reduced": k_result.degenerate_reduced,
            "n_distinct_values": k_result.n_distinct_values,
            "n_samples": k_result.n_samples,
            "centroids": k_result.centroids,
            "bic": k_result.bic,
            "algorithm": "ckwrap.ckmeans (wraps R Ckmeans.1d.dp) -- exact 1-D k-means DP, BIC-selected K",
            "tier_assignments": k_result.tier_assignments,
        },
        "redaction_summary": {
            "total_hits": len(all_hits),
            "by_category": redaction_by_category,
        },
        "exclusions": exclusions,
        "without_interpretation_subsample": {
            "count": len(sample_result.without_interpretation_ids),
            "ids": sample_result.without_interpretation_ids,
        },
        "primary_packet_count": len(primary_packets),
        "stripped_packet_count": len(stripped_packets),
        # Researcher-side ONLY — the real node_id <-> served packet_id map.
        # Never duplicate this into a packets/*/*.json file (see cli.py /
        # packet.py / sampling.py docstrings — reviewer-fairy catch #1).
        "packet_id_map": packet_id_map,
    }

    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False, default=str))
    (out / "exclusions.json").write_text(json.dumps(exclusions, indent=2, ensure_ascii=False))
    with (out / "redaction_log.jsonl").open("w") as f:
        for h in all_hits:
            f.write(json.dumps({
                "node_id": h.node_id, "packet_id": packet_id_map.get(h.node_id),
                "field": h.field, "category": h.category,
                "matched_text": h.matched_text, "start": h.start, "end": h.end,
            }) + "\n")

    return manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", required=True, help="path to knowledge.db")
    parser.add_argument("--out", required=True, help="output directory")
    parser.add_argument("--seed", type=int, default=sampling.DEFAULT_SEED)
    parser.add_argument("--per-cell-target", type=int, default=sampling.PER_CELL_TARGET)
    parser.add_argument("--deep-tier-cap", type=int, default=sampling.DEEP_TIER_CAP)
    args = parser.parse_args(argv)

    manifest = run(
        args.db, args.out, seed=args.seed,
        per_cell_target=args.per_cell_target, deep_tier_cap=args.deep_tier_cap,
    )
    print(json.dumps({
        "frame_totals": manifest["frame_totals"],
        "sample_totals": manifest["sample_totals"],
        "k_star": manifest["k_star"]["k_star"],
        "primary_packet_count": manifest["primary_packet_count"],
        "stripped_packet_count": manifest["stripped_packet_count"],
        "exclusion_count": len(manifest["exclusions"]),
        "redaction_total_hits": manifest["redaction_summary"]["total_hits"],
    }, indent=2))


if __name__ == "__main__":
    main()
