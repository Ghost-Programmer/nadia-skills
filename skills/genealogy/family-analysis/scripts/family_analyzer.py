#!/usr/bin/env python3
"""
Family Kinship, Relationship Calculator & Lineage Analysis Tool for Nadia.
Calculates exact genealogical relationships, MRCA, shared DNA cM, and generates tree charts.
Pure Python standard library implementation.
"""

import argparse
import json
import os
import sys
from collections import deque
from typing import Any, Dict, List, Optional, Set, Tuple

# Import the GedcomDatabase from the sibling module if present, or self-contained loader
try:
    from gedcom_tool import GedcomDatabase
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "gedcom", "scripts")))
    from gedcom_tool import GedcomDatabase


# Shared DNA cM Reference Table (Average and 95% Expected Range)
SHARED_CM_TABLE = {
    "Self / Identical Twin": {"avg_cm": 3485, "min_cm": 3400, "max_cm": 3550, "pct": 100.0},
    "Parent / Child": {"avg_cm": 3485, "min_cm": 3330, "max_cm": 3720, "pct": 50.0},
    "Full Sibling": {"avg_cm": 2613, "min_cm": 2209, "max_cm": 3384, "pct": 37.5},
    "Grandparent / Grandchild": {"avg_cm": 1754, "min_cm": 1156, "max_cm": 2311, "pct": 25.0},
    "Aunt / Uncle / Niece / Nephew": {"avg_cm": 1741, "min_cm": 1201, "max_cm": 2282, "pct": 25.0},
    "Half-Sibling": {"avg_cm": 1759, "min_cm": 1160, "max_cm": 2436, "pct": 25.0},
    "1st Cousin": {"avg_cm": 866, "min_cm": 396, "max_cm": 1397, "pct": 12.5},
    "Great-Grandparent / Great-Grandchild": {"avg_cm": 877, "min_cm": 464, "max_cm": 1486, "pct": 12.5},
    "Great-Aunt / Great-Uncle / Grandniece / Grandnephew": {"avg_cm": 850, "min_cm": 430, "max_cm": 1470, "pct": 12.5},
    "Half-Aunt / Half-Uncle / Half-Niece / Half-Nephew": {"avg_cm": 870, "min_cm": 492, "max_cm": 1315, "pct": 12.5},
    "1st Cousin Once Removed": {"avg_cm": 433, "min_cm": 102, "max_cm": 850, "pct": 6.25},
    "Half 1st Cousin": {"avg_cm": 449, "min_cm": 156, "max_cm": 979, "pct": 6.25},
    "2nd Cousin": {"avg_cm": 229, "min_cm": 41, "max_cm": 538, "pct": 3.125},
    "1st Cousin Twice Removed": {"avg_cm": 225, "min_cm": 0, "max_cm": 460, "pct": 3.125},
    "2nd Cousin Once Removed": {"avg_cm": 122, "min_cm": 0, "max_cm": 325, "pct": 1.56},
    "Half 2nd Cousin": {"avg_cm": 117, "min_cm": 0, "max_cm": 325, "pct": 1.56},
    "3rd Cousin": {"avg_cm": 73, "min_cm": 0, "max_cm": 217, "pct": 0.78},
    "2nd Cousin Twice Removed": {"avg_cm": 61, "min_cm": 0, "max_cm": 190, "pct": 0.78},
    "3rd Cousin Once Removed": {"avg_cm": 48, "min_cm": 0, "max_cm": 173, "pct": 0.39},
    "4th Cousin": {"avg_cm": 35, "min_cm": 0, "max_cm": 127, "pct": 0.20},
    "Distant Cousin (5th-8th)": {"avg_cm": 15, "min_cm": 0, "max_cm": 50, "pct": 0.05}
}


class FamilyAnalyzer:
    def __init__(self, db: GedcomDatabase):
        self.db = db

    def find_ancestors_with_paths(self, indi_id: str) -> Dict[str, List[List[str]]]:
        """
        Returns a dictionary mapping ancestor_id -> list of paths from indi_id to ancestor_id.
        Each path is [indi_id, parent_id, grandparent_id, ...]
        """
        ancestor_paths = {}
        queue = deque([[indi_id]])

        while queue:
            path = queue.popleft()
            current = path[-1]
            if current not in ancestor_paths:
                ancestor_paths[current] = []
            ancestor_paths[current].append(path)

            parents = self.db.get_parents(current)
            for p in parents:
                p_id = p["id"]
                if p_id not in path:  # Avoid cyclic loops
                    queue.append(path + [p_id])

        return ancestor_paths

    def find_mrca(self, indi1_id: str, indi2_id: str) -> List[Dict[str, Any]]:
        """
        Find Most Recent Common Ancestors (MRCA) between two individuals.
        """
        if indi1_id == indi2_id:
            p = self.db.get_individual(indi1_id)
            return [{
                "ancestor_id": indi1_id,
                "name": p["name"] if p else indi1_id,
                "distance_1": 0,
                "distance_2": 0,
                "path_1": [indi1_id],
                "path_2": [indi1_id]
            }]

        anc1 = self.find_ancestors_with_paths(indi1_id)
        anc2 = self.find_ancestors_with_paths(indi2_id)

        common_ids = set(anc1.keys()) & set(anc2.keys())
        if not common_ids:
            return []

        # Calculate minimum distance pairs
        candidates = []
        for c_id in common_ids:
            paths1 = anc1[c_id]
            paths2 = anc2[c_id]
            min_d1 = min(len(p) - 1 for p in paths1)
            min_d2 = min(len(p) - 1 for p in paths2)
            p1 = [p for p in paths1 if len(p) - 1 == min_d1][0]
            p2 = [p for p in paths2 if len(p) - 1 == min_d2][0]

            ancestor = self.db.get_individual(c_id)
            candidates.append({
                "ancestor_id": c_id,
                "name": ancestor["name"] if ancestor else c_id,
                "distance_1": min_d1,
                "distance_2": min_d2,
                "sum_distance": min_d1 + min_d2,
                "path_1": p1,
                "path_2": p2
            })

        # Filter to only the most recent common ancestors (smallest sum_distance)
        min_sum = min(c["sum_distance"] for c in candidates)
        mrcas = [c for c in candidates if c["sum_distance"] == min_sum]
        return mrcas

    def calculate_blood_relationship(self, indi1_id: str, indi2_id: str) -> Optional[Dict[str, Any]]:
        p1 = self.db.get_individual(indi1_id)
        p2 = self.db.get_individual(indi2_id)
        if not p1 or not p2:
            return None

        if indi1_id == indi2_id:
            return {
                "relationship": "Self",
                "category": "DIRECT",
                "formal_title": "Self",
                "mrca": [{"ancestor_id": indi1_id, "name": p1["name"]}],
                "dna_estimate": SHARED_CM_TABLE["Self / Identical Twin"]
            }

        mrcas = self.find_mrca(indi1_id, indi2_id)
        if not mrcas:
            return None

        # Take first MRCA profile for distance calculation
        m = mrcas[0]
        d1 = m["distance_1"]  # Generations from indi1 to MRCA
        d2 = m["distance_2"]  # Generations from indi2 to MRCA
        num_mrcas = len(mrcas)
        sex2 = p2.get("sex", "U")

        # Determine relationship name from d1 and d2
        rel_title, base_cat, dna_key = self._format_kinship(d1, d2, num_mrcas, sex2)

        dna_info = SHARED_CM_TABLE.get(dna_key, SHARED_CM_TABLE.get("Distant Cousin (5th-8th)"))

        return {
            "individual_1": {"id": p1["id"], "name": p1["name"]},
            "individual_2": {"id": p2["id"], "name": p2["name"]},
            "relationship_to_individual_1": rel_title,
            "generations_from_mrca_1": d1,
            "generations_from_mrca_2": d2,
            "common_ancestors": [{"id": mrca["ancestor_id"], "name": mrca["name"]} for mrca in mrcas],
            "dna_shared_estimate": dna_info
        }

    def _format_kinship(self, d1: int, d2: int, num_mrcas: int, sex2: str) -> Tuple[str, str, str]:
        # Direct Ancestor (d1 > 0, d2 == 0) -> p2 is ancestor of p1
        if d2 == 0:
            if d1 == 1:
                title = "Father" if sex2 == 'M' else ("Mother" if sex2 == 'F' else "Parent")
                return title, "DIRECT", "Parent / Child"
            elif d1 == 2:
                title = "Grandfather" if sex2 == 'M' else ("Grandmother" if sex2 == 'F' else "Grandparent")
                return title, "DIRECT", "Grandparent / Grandchild"
            elif d1 == 3:
                title = "Great-Grandfather" if sex2 == 'M' else ("Great-Grandmother" if sex2 == 'F' else "Great-Grandparent")
                return title, "DIRECT", "Great-Grandparent / Great-Grandchild"
            else:
                prefix = "Great-" * (d1 - 2)
                title = f"{prefix}Grandfather" if sex2 == 'M' else (f"{prefix}Grandmother" if sex2 == 'F' else f"{prefix}Grandparent")
                return title, "DIRECT", "Distant Cousin (5th-8th)"

        # Direct Descendant (d1 == 0, d2 > 0) -> p2 is descendant of p1
        if d1 == 0:
            if d2 == 1:
                title = "Son" if sex2 == 'M' else ("Daughter" if sex2 == 'F' else "Child")
                return title, "DIRECT", "Parent / Child"
            elif d2 == 2:
                title = "Grandson" if sex2 == 'M' else ("Granddaughter" if sex2 == 'F' else "Grandchild")
                return title, "DIRECT", "Grandparent / Grandchild"
            elif d2 == 3:
                title = "Great-Grandson" if sex2 == 'M' else ("Great-Granddaughter" if sex2 == 'F' else "Great-Grandchild")
                return title, "DIRECT", "Great-Grandparent / Great-Grandchild"
            else:
                prefix = "Great-" * (d2 - 2)
                title = f"{prefix}Grandson" if sex2 == 'M' else (f"{prefix}Granddaughter" if sex2 == 'F' else f"{prefix}Grandchild")
                return title, "DIRECT", "Distant Cousin (5th-8th)"

        # Siblings (d1 == 1, d2 == 1)
        if d1 == 1 and d2 == 1:
            is_half = (num_mrcas == 1)
            if is_half:
                title = "Half-Brother" if sex2 == 'M' else ("Half-Sister" if sex2 == 'F' else "Half-Sibling")
                return title, "COLLATERAL", "Half-Sibling"
            else:
                title = "Brother" if sex2 == 'M' else ("Sister" if sex2 == 'F' else "Sibling")
                return title, "COLLATERAL", "Full Sibling"

        # Aunts / Uncles (d1 > 1, d2 == 1) -> p2 is sibling to ancestor of p1
        if d2 == 1:
            gen_diff = d1 - 1
            if gen_diff == 1:
                title = "Uncle" if sex2 == 'M' else ("Aunt" if sex2 == 'F' else "Aunt/Uncle")
                return title, "COLLATERAL", "Aunt / Uncle / Niece / Nephew"
            elif gen_diff == 2:
                title = "Great-Uncle" if sex2 == 'M' else ("Great-Aunt" if sex2 == 'F' else "Great-Aunt/Uncle")
                return title, "COLLATERAL", "Great-Aunt / Great-Uncle / Grandniece / Grandnephew"
            else:
                prefix = "Great-" * (gen_diff - 1)
                title = f"{prefix}Uncle" if sex2 == 'M' else (f"{prefix}Aunt" if sex2 == 'F' else f"{prefix}Aunt/Uncle")
                return title, "COLLATERAL", "Distant Cousin (5th-8th)"

        # Nieces / Nephews (d1 == 1, d2 > 1) -> p2 is child of sibling of p1
        if d1 == 1:
            gen_diff = d2 - 1
            if gen_diff == 1:
                title = "Nephew" if sex2 == 'M' else ("Niece" if sex2 == 'F' else "Niece/Nephew")
                return title, "COLLATERAL", "Aunt / Uncle / Niece / Nephew"
            elif gen_diff == 2:
                title = "Grandnephew" if sex2 == 'M' else ("Grandniece" if sex2 == 'F' else "Grandniece/Grandnephew")
                return title, "COLLATERAL", "Great-Aunt / Great-Uncle / Grandniece / Grandnephew"
            else:
                prefix = "Great-" * (gen_diff - 1)
                title = f"{prefix}Nephew" if sex2 == 'M' else (f"{prefix}Niece" if sex2 == 'F' else f"{prefix}Niece/Nephew")
                return title, "COLLATERAL", "Distant Cousin (5th-8th)"

        # Cousins (d1 >= 2, d2 >= 2)
        cousin_degree = min(d1, d2) - 1
        removed = abs(d1 - d2)

        ordinals = {1: "1st", 2: "2nd", 3: "3rd", 4: "4th", 5: "5th", 6: "6th", 7: "7th", 8: "8th"}
        degree_str = ordinals.get(cousin_degree, f"{cousin_degree}th")

        removed_str = ""
        if removed == 1:
            removed_str = " Once Removed"
        elif removed == 2:
            removed_str = " Twice Removed"
        elif removed == 3:
            removed_str = " Three Times Removed"
        elif removed > 3:
            removed_str = f" {removed} Times Removed"

        title = f"{degree_str} Cousin{removed_str}"

        # Match table key
        key = f"{degree_str} Cousin{removed_str}"
        if key not in SHARED_CM_TABLE:
            key = "Distant Cousin (5th-8th)"

        return title, "COUSIN", key

    def render_pedigree_ascii(self, indi_id: str, generations: int = 3) -> str:
        tree = self.db.get_ancestors_tree(indi_id, max_generations=generations)
        if not tree:
            return f"Individual {indi_id} not found."

        lines = []

        def _format_node(node: Optional[Dict[str, Any]]) -> str:
            if not node or not node.get("name"):
                return "Unknown"
            birth_yr = node.get("birth", {}).get("year") if node.get("birth") else ""
            death_yr = node.get("death", {}).get("year") if node.get("death") else ""
            dates = f" ({birth_yr}-{death_yr})" if (birth_yr or death_yr) else ""
            return f"{node['name']}{dates}"

        lines.append(f"Pedigree Chart for: {_format_node(tree)}")
        lines.append("=" * 60)

        # Generation 1 (Target)
        lines.append(f"1. [Self] {_format_node(tree)}")

        # Generation 2 (Parents)
        father = tree.get("father")
        mother = tree.get("mother")
        lines.append(f"   ├── 2. [Father] {_format_node(father)}")
        if father and generations >= 3:
            ff = father.get("father")
            fm = father.get("mother")
            lines.append(f"   │   ├── 4. [Paternal Grandfather] {_format_node(ff)}")
            lines.append(f"   │   └── 5. [Paternal Grandmother] {_format_node(fm)}")

        lines.append(f"   └── 3. [Mother] {_format_node(mother)}")
        if mother and generations >= 3:
            mf = mother.get("father")
            mm = mother.get("mother")
            lines.append(f"       ├── 6. [Maternal Grandfather] {_format_node(mf)}")
            lines.append(f"       └── 7. [Maternal Grandmother] {_format_node(mm)}")

        return "\n".join(lines)

    def generate_family_timeline(self, indi_id: str) -> List[Dict[str, Any]]:
        indi = self.db.get_individual(indi_id)
        if not indi:
            return []

        events = []

        # Individual's events
        if indi.get("birth") and indi["birth"].get("year"):
            events.append({
                "year": indi["birth"]["year"],
                "date": indi["birth"].get("date"),
                "event": "Birth",
                "person": indi["name"],
                "place": indi["birth"].get("place"),
                "description": f"{indi['name']} was born."
            })

        if indi.get("christening") and indi["christening"].get("year"):
            events.append({
                "year": indi["christening"]["year"],
                "date": indi["christening"].get("date"),
                "event": "Christening",
                "person": indi["name"],
                "place": indi["christening"].get("place"),
                "description": f"{indi['name']} was christened."
            })

        # Marriages
        for fams_id in indi.get("family_spouse_in", []):
            fam = self.db.get_family(fams_id)
            if fam and fam.get("marriage") and fam["marriage"].get("year"):
                spouse_id = fam["wife_id"] if fam.get("husband_id") == indi_id else fam.get("husband_id")
                spouse = self.db.get_individual(spouse_id) if spouse_id else None
                s_name = spouse["name"] if spouse else "Unknown Spouse"
                events.append({
                    "year": fam["marriage"]["year"],
                    "date": fam["marriage"].get("date"),
                    "event": "Marriage",
                    "person": indi["name"],
                    "place": fam["marriage"].get("place"),
                    "description": f"Marriage to {s_name}."
                })

        # Children Births
        for child in self.db.get_children_of_individual(indi_id):
            if child.get("birth") and child["birth"].get("year"):
                events.append({
                    "year": child["birth"]["year"],
                    "date": child["birth"].get("date"),
                    "event": "Child Birth",
                    "person": child["name"],
                    "place": child["birth"].get("place"),
                    "description": f"Birth of child: {child['name']}."
                })

        # Parent Deaths
        for parent in self.db.get_parents(indi_id):
            if parent.get("death") and parent["death"].get("year"):
                events.append({
                    "year": parent["death"]["year"],
                    "date": parent["death"].get("date"),
                    "event": "Parent Death",
                    "person": parent["name"],
                    "place": parent["death"].get("place"),
                    "description": f"Death of parent: {parent['name']}."
                })

        # Individual Death
        if indi.get("death") and indi["death"].get("year"):
            events.append({
                "year": indi["death"]["year"],
                "date": indi["death"].get("date"),
                "event": "Death",
                "person": indi["name"],
                "place": indi["death"].get("place"),
                "description": f"{indi['name']} passed away."
            })

        # Sort chronologically
        events.sort(key=lambda e: (e["year"], e.get("date") or ""))
        return events


def main():
    parser = argparse.ArgumentParser(description="Nadia Family Analyzer & Kinship Calculator")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # relationship
    p_rel = subparsers.add_parser("relationship", help="Calculate exact genealogical relationship between two individuals")
    p_rel.add_argument("--file", required=True, help="Path to .ged file")
    p_rel.add_argument("--id1", required=True, help="First individual XREF ID")
    p_rel.add_argument("--id2", required=True, help="Second individual XREF ID")

    # mrca
    p_mrca = subparsers.add_parser("mrca", help="Find Most Recent Common Ancestor(s)")
    p_mrca.add_argument("--file", required=True, help="Path to .ged file")
    p_mrca.add_argument("--id1", required=True, help="First individual XREF ID")
    p_mrca.add_argument("--id2", required=True, help="Second individual XREF ID")

    # chart
    p_chart = subparsers.add_parser("chart", help="Render ASCII pedigree chart")
    p_chart.add_argument("--file", required=True, help="Path to .ged file")
    p_chart.add_argument("--id", required=True, help="Individual XREF ID")
    p_chart.add_argument("--generations", type=int, default=3, help="Generations to render (default: 3)")

    # timeline
    p_time = subparsers.add_parser("timeline", help="Generate combined life timeline for an individual and family")
    p_time.add_argument("--file", required=True, help="Path to .ged file")
    p_time.add_argument("--id", required=True, help="Individual XREF ID")

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(json.dumps({"error": f"File not found: {args.file}"}), file=sys.stderr)
        sys.exit(1)

    try:
        db = GedcomDatabase.parse_file(args.file)
    except Exception as e:
        print(json.dumps({"error": f"Failed to parse GEDCOM file: {str(e)}"}), file=sys.stderr)
        sys.exit(1)

    analyzer = FamilyAnalyzer(db)

    if args.command == "relationship":
        res = analyzer.calculate_blood_relationship(args.id1, args.id2)
        if not res:
            res = {"result": "NO_DIRECT_BLOOD_RELATION_FOUND", "description": f"No common ancestor found between {args.id1} and {args.id2}."}
        print(json.dumps(res, indent=2))

    elif args.command == "mrca":
        mrcas = analyzer.find_mrca(args.id1, args.id2)
        print(json.dumps({"mrcas": mrcas}, indent=2))

    elif args.command == "chart":
        chart_str = analyzer.render_pedigree_ascii(args.id, generations=args.generations)
        print(json.dumps({"chart": chart_str, "individual_id": args.id}, indent=2))

    elif args.command == "timeline":
        events = analyzer.generate_family_timeline(args.id)
        print(json.dumps({"individual_id": args.id, "timeline": events}, indent=2))


if __name__ == "__main__":
    main()
