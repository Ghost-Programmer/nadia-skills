#!/usr/bin/env python3
"""
Record Matcher and Historical Comparison Engine for Nadia Genealogy Suite.
Performs multi-factor probabilistic record matching, phonetic name matching,
household relational reinforcement, and cross-tree duplicate detection.
Pure Python standard library implementation.
"""

import argparse
import difflib
import json
import os
import re
import sys
from collections import defaultdict
from typing import Any, Dict, List, Optional, Set, Tuple

try:
    from gedcom_tool import GedcomDatabase
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "gedcom", "scripts")))
    from gedcom_tool import GedcomDatabase


# Common Genealogical Nickname / Alias Equivalence Dictionary
NICKNAME_MAP = {
    "william": {"bill", "billy", "will", "willy", "liam"},
    "bill": {"william", "billy", "will", "willy"},
    "robert": {"bob", "bobby", "rob", "robby", "bert"},
    "bob": {"robert", "bobby", "rob"},
    "margaret": {"peggy", "maggie", "meg", "daisy", "marge", "margo"},
    "peggy": {"margaret", "maggie"},
    "mary": {"polly", "molly", "mae", "maria"},
    "polly": {"mary", "molly"},
    "elizabeth": {"beth", "betty", "liz", "lizzie", "eliza", "bess", "elise"},
    "eliza": {"elizabeth", "beth", "lizzie"},
    "john": {"jack", "johnny", "jon"},
    "jack": {"john", "johnny"},
    "james": {"jim", "jimmy", "jamie"},
    "jim": {"james", "jimmy"},
    "richard": {"dick", "rick", "ricky", "rich"},
    "dick": {"richard", "rick"},
    "thomas": {"tom", "tommy"},
    "tom": {"thomas", "tommy"},
    "alexander": {"alex", "alec", "sandy"},
    "alex": {"alexander", "alec"},
    "sarah": {"sally", "sadie", "sara"},
    "sally": {"sarah", "sadie"},
    "charles": {"charlie", "chuck", "chas"},
    "charlie": {"charles", "chuck"},
    "edward": {"ed", "eddie", "ned", "ted"},
    "ed": {"edward", "eddie", "ned"},
    "ann": {"anne", "annie", "nancy", "nan"},
    "nancy": {"ann", "anne", "annie"},
    "henry": {"hank", "harry", "hal"},
    "harry": {"henry", "hank"},
    "catherine": {"katherine", "kate", "katie", "cathy", "kathy", "kay"},
    "catherine": {"katherine", "kate", "katie", "cathy", "kathy", "kay"}
}


def soundex(name: str) -> str:
    """Calculates American Soundex code for a given surname/name."""
    if not name:
        return "0000"
    clean = re.sub(r'[^a-zA-Z]', '', name).upper()
    if not clean:
        return "0000"

    first_letter = clean[0]
    mapping = {
        'B': '1', 'F': '1', 'P': '1', 'V': '1',
        'C': '2', 'G': '2', 'J': '2', 'K': '2', 'Q': '2', 'S': '2', 'X': '2', 'Z': '2',
        'D': '3', 'T': '3',
        'L': '4',
        'M': '5', 'N': '5',
        'R': '6'
    }

    encoded = [first_letter]
    prev = mapping.get(first_letter, '0')

    for char in clean[1:]:
        code = mapping.get(char, '0')
        if code != '0':
            if code != prev:
                encoded.append(code)
            prev = code
        else:
            prev = '0'

    result = "".join(encoded)[:4]
    return result.ljust(4, '0')


def string_similarity(s1: str, s2: str) -> float:
    if not s1 or not s2:
        return 0.0
    return difflib.SequenceMatcher(None, s1.lower().strip(), s2.lower().strip()).ratio()


class RecordMatcher:
    def __init__(self, db: GedcomDatabase):
        self.db = db

    def score_name(self, g_given: str, g_surn: str, r_given: str, r_surn: str) -> Tuple[float, Dict[str, Any]]:
        g_g = (g_given or "").lower().strip()
        g_s = (g_surn or "").lower().strip()
        r_g = (r_given or "").lower().strip()
        r_s = (r_surn or "").lower().strip()

        # Surname score
        surn_score = 0.0
        surn_note = ""
        if g_s == r_s and g_s:
            surn_score = 1.0
            surn_note = "Exact surname match"
        elif soundex(g_s) == soundex(r_s) and g_s and r_s:
            surn_score = 0.88
            surn_note = f"Phonetic Soundex match ({soundex(g_s)})"
        else:
            sim = string_similarity(g_s, r_s)
            surn_score = sim * 0.8
            surn_note = f"String similarity ({round(sim, 2)})"

        # Given name score
        given_score = 0.0
        given_note = ""
        if g_g == r_g and g_g:
            given_score = 1.0
            given_note = "Exact given name match"
        elif g_g in NICKNAME_MAP.get(r_g, set()) or r_g in NICKNAME_MAP.get(g_g, set()):
            given_score = 0.95
            given_note = f"Standard nickname/alias match ({g_g} <-> {r_g})"
        elif g_g and r_g and (g_g.startswith(r_g) or r_g.startswith(g_g)) and min(len(g_g), len(r_g)) >= 3:
            given_score = 0.80
            given_note = "Prefix / abbreviation match"
        elif soundex(g_g) == soundex(r_g) and g_g and r_g:
            given_score = 0.80
            given_note = f"Phonetic Soundex match ({soundex(g_g)})"
        else:
            sim = string_similarity(g_g, r_g)
            given_score = sim * 0.7
            given_note = f"String similarity ({round(sim, 2)})"

        combined_name_score = (surn_score * 0.55) + (given_score * 0.45)
        return combined_name_score, {
            "surname_score": round(surn_score, 2),
            "surname_note": surn_note,
            "given_name_score": round(given_score, 2),
            "given_name_note": given_note,
            "overall_name_score": round(combined_name_score, 2)
        }

    def score_dates(self, g_year: Optional[int], r_year: Optional[int], event_name: str = "Birth") -> Tuple[float, str]:
        if g_year is None or r_year is None:
            return 0.5, f"No {event_name} year in one or both records (neutral)"

        diff = abs(g_year - r_year)
        if diff == 0:
            return 1.0, f"Exact {event_name} year match ({g_year})"
        elif diff == 1:
            return 0.90, f"{event_name} year within 1 year ({g_year} vs {r_year}) - typical census variation"
        elif diff == 2:
            return 0.75, f"{event_name} year within 2 years ({g_year} vs {r_year})"
        elif diff <= 5:
            return 0.45, f"{event_name} year within {diff} years ({g_year} vs {r_year})"
        else:
            return 0.0, f"{event_name} year discrepancy ({g_year} vs {r_year}, diff: {diff} yrs)"

    def score_places(self, g_place: Optional[str], r_place: Optional[str]) -> Tuple[float, str]:
        if not g_place or not r_place:
            return 0.5, "Place data missing in one or both records (neutral)"

        g_tokens = set(re.findall(r'\b\w+\b', g_place.lower()))
        r_tokens = set(re.findall(r'\b\w+\b', r_place.lower()))

        intersection = g_tokens & r_tokens
        if not intersection:
            sim = string_similarity(g_place, r_place)
            if sim > 0.6:
                return round(sim, 2), f"Fuzzy place match ({round(sim, 2)})"
            return 0.1, f"Different locations ('{g_place}' vs '{r_place}')"

        jaccard = len(intersection) / len(g_tokens | r_tokens)
        score = min(1.0, 0.5 + (jaccard * 0.8))
        common_words = ", ".join(list(intersection)[:3])
        return round(score, 2), f"Shared geographic tokens ({common_words})"

    def match_individual_against_record(self, indi_id: str, record_data: Dict[str, Any]) -> Dict[str, Any]:
        indi = self.db.get_individual(indi_id)
        if not indi:
            return {"error": f"Individual {indi_id} not found in GEDCOM"}

        # 1. Name scoring
        rec_given = record_data.get("given_name") or record_data.get("first_name", "")
        rec_surn = record_data.get("surname") or record_data.get("last_name", "")
        if not rec_given and not rec_surn and record_data.get("name"):
            parts = record_data["name"].strip().split()
            rec_given = parts[0] if parts else ""
            rec_surn = parts[-1] if len(parts) > 1 else ""

        name_score, name_details = self.score_name(indi.get("given_name", ""), indi.get("surname", ""), rec_given, rec_surn)

        # 2. Birth date scoring
        g_byear = indi.get("birth", {}).get("year") if indi.get("birth") else None
        r_byear = record_data.get("birth_year")
        if r_byear is None and record_data.get("age") and record_data.get("record_year"):
            r_byear = record_data["record_year"] - record_data["age"]

        birth_score, birth_note = self.score_dates(g_byear, r_byear, "Birth")

        # 3. Death date scoring (if applicable)
        g_dyear = indi.get("death", {}).get("year") if indi.get("death") else None
        r_dyear = record_data.get("death_year")
        death_score, death_note = self.score_dates(g_dyear, r_dyear, "Death")

        # 4. Place scoring
        g_place = (indi.get("birth", {}).get("place") or indi.get("death", {}).get("place")) if indi.get("birth") or indi.get("death") else None
        r_place = record_data.get("place") or record_data.get("residence") or record_data.get("birth_place")
        place_score, place_note = self.score_places(g_place, r_place)

        # 5. Relational Reinforcement (Spouse / Family)
        rel_score = 0.5
        rel_note = "No spouse / household info in record"
        rec_spouse = record_data.get("spouse_name")
        if rec_spouse:
            tree_spouses = self.db.get_spouses(indi_id)
            best_sp_sim = 0.0
            best_sp_name = ""
            for sp in tree_spouses:
                sim = string_similarity(sp["name"], rec_spouse)
                if sim > best_sp_sim:
                    best_sp_sim = sim
                    best_sp_name = sp["name"]

            if best_sp_sim >= 0.85:
                rel_score = 1.0
                rel_note = f"Spouse in record '{rec_spouse}' strongly matches tree spouse '{best_sp_name}'"
            elif best_sp_sim >= 0.60:
                rel_score = 0.80
                rel_note = f"Spouse in record '{rec_spouse}' probable match to tree spouse '{best_sp_name}'"
            else:
                rel_score = 0.20
                rel_note = f"Spouse in record '{rec_spouse}' does not match tree spouse(s)"

        # Composite Calculation
        # Weights: Name (35%), Birth (25%), Place (20%), Relational (20%)
        weights = {"name": 0.35, "birth": 0.25, "place": 0.20, "relational": 0.20}
        composite = (
            (name_score * weights["name"]) +
            (birth_score * weights["birth"]) +
            (place_score * weights["place"]) +
            (rel_score * weights["relational"])
        ) * 100

        confidence = "UNLIKELY"
        if composite >= 82.0:
            confidence = "VERY_HIGH"
        elif composite >= 70.0:
            confidence = "HIGH"
        elif composite >= 55.0:
            confidence = "MODERATE"
        elif composite >= 40.0:
            confidence = "LOW"

        return {
            "individual_in_tree": {
                "id": indi["id"],
                "name": indi["name"],
                "birth_year": g_byear,
                "birth_place": indi.get("birth", {}).get("place") if indi.get("birth") else None,
                "death_year": g_dyear
            },
            "historical_record": record_data,
            "match_evaluation": {
                "composite_score_pct": round(composite, 1),
                "confidence_level": confidence,
                "breakdown": {
                    "name": name_details,
                    "birth_date": {"score": birth_score, "note": birth_note},
                    "place": {"score": place_score, "note": place_note},
                    "relational_household": {"score": rel_score, "note": rel_note}
                },
                "genealogical_proof_standard_assessment": self._generate_gps_assessment(confidence, name_details, birth_note, place_note, rel_note)
            }
        }

    def _generate_gps_assessment(self, confidence: str, name_details: Dict, birth_note: str, place_note: str, rel_note: str) -> str:
        if confidence in ("VERY_HIGH", "HIGH"):
            return f"Evidence demonstrates consistent concordance across name ({name_details['overall_name_score'] * 100}%), timeline ({birth_note}), and geography. High probability of identity."
        elif confidence == "MODERATE":
            return "Positive correlation found, but minor discrepancies in dates or lack of household corroboration require additional record verification before formal tree linking."
        else:
            return "Insufficient evidence or conflicting vital data. Identity cannot be established under standard genealogical proof standards."

    def search_tree_for_record_matches(self, record_data: Dict[str, Any], limit: int = 5) -> List[Dict[str, Any]]:
        evaluations = []
        rec_surn = record_data.get("surname") or ""
        rec_given = record_data.get("given_name") or ""
        if not rec_surn and record_data.get("name"):
            parts = record_data["name"].split()
            rec_given = parts[0]
            rec_surn = parts[-1] if len(parts) > 1 else ""

        # Pre-filter candidates by surname or phonetic soundex
        rec_sx = soundex(rec_surn)
        candidates = []
        for indi in self.db.individuals.values():
            surn = indi.get("surname", "")
            if not surn:
                candidates.append(indi["id"])
            elif surn.lower() == rec_surn.lower() or soundex(surn) == rec_sx or string_similarity(surn, rec_surn) >= 0.7:
                candidates.append(indi["id"])

        if len(candidates) < 5:
            candidates = list(self.db.individuals.keys())

        for indi_id in candidates:
            match_res = self.match_individual_against_record(indi_id, record_data)
            if "match_evaluation" in match_res:
                score = match_res["match_evaluation"]["composite_score_pct"]
                if score >= 35.0:
                    evaluations.append(match_res)

        evaluations.sort(key=lambda x: x["match_evaluation"]["composite_score_pct"], reverse=True)
        return evaluations[:limit]

    def compare_two_trees(self, other_db: GedcomDatabase, min_score: float = 65.0) -> List[Dict[str, Any]]:
        matches = []
        for indi1 in self.db.individuals.values():
            rec_data = {
                "given_name": indi1.get("given_name"),
                "surname": indi1.get("surname"),
                "name": indi1.get("name"),
                "birth_year": indi1.get("birth", {}).get("year") if indi1.get("birth") else None,
                "place": indi1.get("birth", {}).get("place") if indi1.get("birth") else None
            }
            # Search other db
            other_matcher = RecordMatcher(other_db)
            other_matches = other_matcher.search_tree_for_record_matches(rec_data, limit=1)
            if other_matches and other_matches[0]["match_evaluation"]["composite_score_pct"] >= min_score:
                top = other_matches[0]
                matches.append({
                    "tree_1_individual": {"id": indi1["id"], "name": indi1["name"], "birth": indi1.get("birth")},
                    "tree_2_individual": top["individual_in_tree"],
                    "match_score": top["match_evaluation"]["composite_score_pct"],
                    "confidence": top["match_evaluation"]["confidence_level"]
                })
        return matches


def main():
    parser = argparse.ArgumentParser(description="Nadia Historical Record & Tree Matcher")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # match-record
    p_rec = subparsers.add_parser("match-record", help="Evaluate match between a tree individual and a historical record")
    p_rec.add_argument("--file", required=True, help="Path to GEDCOM .ged file")
    p_rec.add_argument("--id", required=True, help="Tree Individual ID to evaluate against")
    p_rec.add_argument("--record-json", help="Raw JSON string containing record data")
    p_rec.add_argument("--name", help="Name in record")
    p_rec.add_argument("--birth-year", type=int, help="Birth year in record")
    p_rec.add_argument("--death-year", type=int, help="Death year in record")
    p_rec.add_argument("--place", help="Location in record")
    p_rec.add_argument("--spouse", help="Spouse name in record")
    p_rec.add_argument("--record-type", default="Historical Record", help="Record source type (Census, SSDI, etc.)")

    # search-matches
    p_search = subparsers.add_parser("search-matches", help="Search the entire tree for best matches to a historical record")
    p_search.add_argument("--file", required=True, help="Path to GEDCOM .ged file")
    p_search.add_argument("--name", required=True, help="Name in record")
    p_search.add_argument("--birth-year", type=int, help="Birth year in record")
    p_search.add_argument("--place", help="Location in record")
    p_search.add_argument("--spouse", help="Spouse name in record")
    p_search.add_argument("--limit", type=int, default=5, help="Max matches to return")

    # compare-trees
    p_trees = subparsers.add_parser("compare-trees", help="Compare two GEDCOM trees and identify common individuals")
    p_trees.add_argument("--file1", required=True, help="Path to first GEDCOM file")
    p_trees.add_argument("--file2", required=True, help="Path to second GEDCOM file")
    p_trees.add_argument("--min-score", type=float, default=65.0, help="Minimum match score percentage")

    args = parser.parse_args()

    if not os.path.exists(args.file if hasattr(args, 'file') else args.file1):
        print(json.dumps({"error": "Primary GEDCOM file not found"}), file=sys.stderr)
        sys.exit(1)

    db = GedcomDatabase.parse_file(args.file if hasattr(args, 'file') else args.file1)
    matcher = RecordMatcher(db)

    if args.command == "match-record":
        rec_data = {}
        if args.record_json:
            try:
                rec_data = json.loads(args.record_json)
            except Exception as e:
                print(json.dumps({"error": f"Invalid record-json: {str(e)}"}), file=sys.stderr)
                sys.exit(1)
        else:
            rec_data = {
                "name": args.name,
                "birth_year": args.birth_year,
                "death_year": args.death_year,
                "place": args.place,
                "spouse_name": args.spouse,
                "record_type": args.record_type
            }

        res = matcher.match_individual_against_record(args.id, rec_data)
        print(json.dumps(res, indent=2))

    elif args.command == "search-matches":
        rec_data = {
            "name": args.name,
            "birth_year": args.birth_year,
            "place": args.place,
            "spouse_name": args.spouse
        }
        res = matcher.search_tree_for_record_matches(rec_data, limit=args.limit)
        print(json.dumps({"matches_found": len(res), "top_matches": res}, indent=2))

    elif args.command == "compare-trees":
        if not os.path.exists(args.file2):
            print(json.dumps({"error": f"Second file not found: {args.file2}"}), file=sys.stderr)
            sys.exit(1)
        db2 = GedcomDatabase.parse_file(args.file2)
        matches = matcher.compare_two_trees(db2, min_score=args.min_score)
        print(json.dumps({"total_matches": len(matches), "cross_tree_matches": matches}, indent=2))


if __name__ == "__main__":
    main()
