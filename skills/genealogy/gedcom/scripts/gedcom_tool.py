#!/usr/bin/env python3
"""
GEDCOM Parser and Diagnostic Tool for Nadia Genealogy Suite.
Supports GEDCOM 5.5, 5.5.1, and 7.0 standard formats.
Pure Python standard library implementation.
"""

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


class GedcomRecord:
    def __init__(self, level: int, xref: Optional[str], tag: str, value: str):
        self.level = level
        self.xref = xref
        self.tag = tag
        self.value = value
        self.children: List['GedcomRecord'] = []

    def get_child_value(self, tag: str) -> Optional[str]:
        for child in self.children:
            if child.tag == tag:
                val = child.value
                for sub in child.children:
                    if sub.tag == 'CONC':
                        val = (val or "") + (sub.value or "")
                    elif sub.tag == 'CONT':
                        val = (val or "") + "\n" + (sub.value or "")
                return val
        return None

    def get_child(self, tag: str) -> Optional['GedcomRecord']:
        for child in self.children:
            if child.tag == tag:
                return child
        return None

    def get_children(self, tag: str) -> List['GedcomRecord']:
        return [child for child in self.children if child.tag == tag]


class GedcomDatabase:
    def __init__(self):
        self.header: Dict[str, Any] = {}
        self.individuals: Dict[str, Dict[str, Any]] = {}
        self.families: Dict[str, Dict[str, Any]] = {}
        self.sources: Dict[str, Dict[str, Any]] = {}
        self.repositories: Dict[str, Dict[str, Any]] = {}
        self.notes: Dict[str, str] = {}
        self.raw_records: List[GedcomRecord] = []

    @staticmethod
    def _read_file_with_encoding(file_path: str) -> str:
        encodings = ['utf-8-sig', 'utf-8', 'latin-1', 'cp1252', 'ascii']
        for enc in encodings:
            try:
                with open(file_path, 'r', encoding=enc, errors='replace') as f:
                    return f.read()
            except Exception:
                continue
        raise ValueError(f"Unable to read file: {file_path}")

    @classmethod
    def parse_file(cls, file_path: str) -> 'GedcomDatabase':
        content = cls._read_file_with_encoding(file_path)
        db = cls()
        db._parse_content(content)
        return db

    def _parse_content(self, content: str):
        lines = content.splitlines()
        root_records: List[GedcomRecord] = []
        stack: List[GedcomRecord] = []

        line_regex = re.compile(r'^\s*(\d+)\s+(?:(@[^@]+@)\s+)?([A-Za-z0-9_]+)(?:\s+(.*))?$')

        for line in lines:
            line_str = line.strip()
            if not line_str:
                continue
            match = line_regex.match(line_str)
            if not match:
                continue

            level = int(match.group(1))
            xref = match.group(2)
            tag = match.group(3).upper()
            value = (match.group(4) or "").strip()

            record = GedcomRecord(level, xref, tag, value)

            if level == 0:
                root_records.append(record)
                stack = [record]
            else:
                while len(stack) > level:
                    stack.pop()
                if stack:
                    stack[-1].children.append(record)
                    stack.append(record)

        self.raw_records = root_records
        self._process_records()

    def _process_records(self):
        for rec in self.raw_records:
            if rec.tag == 'HEAD':
                self._process_head(rec)
            elif rec.tag == 'INDI' and rec.xref:
                self.individuals[rec.xref] = self._process_individual(rec)
            elif rec.tag == 'FAM' and rec.xref:
                self.families[rec.xref] = self._process_family(rec)
            elif rec.tag == 'SOUR' and rec.xref:
                self.sources[rec.xref] = self._process_source(rec)
            elif rec.tag == 'REPO' and rec.xref:
                self.repositories[rec.xref] = self._process_repository(rec)
            elif rec.tag == 'NOTE' and rec.xref:
                self.notes[rec.xref] = rec.value

    def _process_head(self, rec: GedcomRecord):
        self.header = {
            "gedcom_version": "5.5",
            "source": rec.get_child_value('SOUR') or "Unknown",
            "charset": rec.get_child_value('CHAR') or "UTF-8"
        }
        gedc = rec.get_child('GEDC')
        if gedc:
            vers = gedc.get_child_value('VERS')
            if vers:
                self.header["gedcom_version"] = vers

    def _extract_event(self, rec: Optional[GedcomRecord]) -> Optional[Dict[str, Any]]:
        if not rec:
            return None
        date_val = rec.get_child_value('DATE')
        place_val = rec.get_child_value('PLAC')
        year = self._extract_year(date_val)
        return {
            "date": date_val,
            "year": year,
            "place": place_val
        }

    @staticmethod
    def _extract_year(date_str: Optional[str]) -> Optional[int]:
        if not date_str:
            return None
        match = re.search(r'\b(1[0-9]{3}|20[0-9]{2}|0?[1-9][0-9]{2})\b', date_str)
        if match:
            try:
                return int(match.group(1))
            except ValueError:
                pass
        return None

    def _process_individual(self, rec: GedcomRecord) -> Dict[str, Any]:
        indi_id = rec.xref
        name_rec = rec.get_child('NAME')
        raw_name = name_rec.value if name_rec else "Unknown"
        
        given_name = ""
        surname = ""
        if name_rec:
            given_name = name_rec.get_child_value('GIVN') or ""
            surname = name_rec.get_child_value('SURN') or ""
            if not given_name and not surname and '/' in raw_name:
                parts = raw_name.split('/')
                given_name = parts[0].strip()
                surname = parts[1].strip() if len(parts) > 1 else ""

        sex = rec.get_child_value('SEX') or "U"
        birth = self._extract_event(rec.get_child('BIRT'))
        death = self._extract_event(rec.get_child('DEAT'))
        burial = self._extract_event(rec.get_child('BURI'))
        christening = self._extract_event(rec.get_child('CHR')) or self._extract_event(rec.get_child('BAPM'))

        famc_links = [child.value for child in rec.get_children('FAMC') if child.value]
        fams_links = [child.value for child in rec.get_children('FAMS') if child.value]

        occupations = [child.value for child in rec.get_children('OCCU') if child.value]
        residences = []
        for resi in rec.get_children('RESI'):
            res_event = self._extract_event(resi)
            if res_event and (res_event["date"] or res_event["place"]):
                residences.append(res_event)

        clean_name = raw_name.replace('/', '').strip()
        if not clean_name:
            clean_name = f"{given_name} {surname}".strip() or "Unnamed Individual"

        # Calculate estimated lifespan
        lifespan = None
        if birth and birth.get("year") and death and death.get("year"):
            lifespan = death["year"] - birth["year"]

        return {
            "id": indi_id,
            "name": clean_name,
            "given_name": given_name,
            "surname": surname,
            "sex": sex.upper(),
            "birth": birth,
            "death": death,
            "burial": burial,
            "christening": christening,
            "lifespan_years": lifespan,
            "family_child_of": famc_links,
            "family_spouse_in": fams_links,
            "occupations": occupations,
            "residences": residences
        }

    def _process_family(self, rec: GedcomRecord) -> Dict[str, Any]:
        fam_id = rec.xref
        husb = rec.get_child_value('HUSB')
        wife = rec.get_child_value('WIFE')
        children = [child.value for child in rec.get_children('CHIL') if child.value]
        marriage = self._extract_event(rec.get_child('MARR'))
        divorce = self._extract_event(rec.get_child('DIV'))

        return {
            "id": fam_id,
            "husband_id": husb,
            "wife_id": wife,
            "children_ids": children,
            "marriage": marriage,
            "divorce": divorce
        }

    def _process_source(self, rec: GedcomRecord) -> Dict[str, Any]:
        return {
            "id": rec.xref,
            "title": rec.get_child_value('TITL') or rec.value,
            "author": rec.get_child_value('AUTH'),
            "publication": rec.get_child_value('PUBL'),
            "repository_id": rec.get_child_value('REPO')
        }

    def _process_repository(self, rec: GedcomRecord) -> Dict[str, Any]:
        return {
            "id": rec.xref,
            "name": rec.get_child_value('NAME') or rec.value,
            "address": rec.get_child_value('ADDR')
        }

    def get_individual(self, indi_id: str) -> Optional[Dict[str, Any]]:
        return self.individuals.get(indi_id)

    def get_family(self, fam_id: str) -> Optional[Dict[str, Any]]:
        return self.families.get(fam_id)

    def get_parents(self, indi_id: str) -> List[Dict[str, Any]]:
        indi = self.get_individual(indi_id)
        if not indi:
            return []
        parents = []
        for famc_id in indi["family_child_of"]:
            fam = self.get_family(famc_id)
            if fam:
                if fam.get("husband_id"):
                    h = self.get_individual(fam["husband_id"])
                    if h:
                        parents.append(h)
                if fam.get("wife_id"):
                    w = self.get_individual(fam["wife_id"])
                    if w:
                        parents.append(w)
        return parents

    def get_spouses(self, indi_id: str) -> List[Dict[str, Any]]:
        indi = self.get_individual(indi_id)
        if not indi:
            return []
        spouses = []
        for fams_id in indi["family_spouse_in"]:
            fam = self.get_family(fams_id)
            if fam:
                if fam.get("husband_id") and fam["husband_id"] != indi_id:
                    s = self.get_individual(fam["husband_id"])
                    if s:
                        spouses.append(s)
                elif fam.get("wife_id") and fam["wife_id"] != indi_id:
                    s = self.get_individual(fam["wife_id"])
                    if s:
                        spouses.append(s)
        return spouses

    def get_children_of_individual(self, indi_id: str) -> List[Dict[str, Any]]:
        indi = self.get_individual(indi_id)
        if not indi:
            return []
        children = []
        seen = set()
        for fams_id in indi["family_spouse_in"]:
            fam = self.get_family(fams_id)
            if fam:
                for c_id in fam.get("children_ids", []):
                    if c_id not in seen:
                        seen.add(c_id)
                        c = self.get_individual(c_id)
                        if c:
                            children.append(c)
        return children

    def get_siblings(self, indi_id: str) -> List[Dict[str, Any]]:
        indi = self.get_individual(indi_id)
        if not indi:
            return []
        siblings = []
        seen = {indi_id}
        for famc_id in indi["family_child_of"]:
            fam = self.get_family(famc_id)
            if fam:
                for c_id in fam.get("children_ids", []):
                    if c_id not in seen:
                        seen.add(c_id)
                        c = self.get_individual(c_id)
                        if c:
                            siblings.append(c)
        return siblings

    def get_summary(self) -> Dict[str, Any]:
        total_indi = len(self.individuals)
        total_fam = len(self.families)
        total_sour = len(self.sources)

        males = sum(1 for indi in self.individuals.values() if indi["sex"] == 'M')
        females = sum(1 for indi in self.individuals.values() if indi["sex"] == 'F')
        unknown_sex = total_indi - (males + females)

        birth_years = [indi["birth"]["year"] for indi in self.individuals.values() if indi.get("birth") and indi["birth"].get("year")]
        death_years = [indi["death"]["year"] for indi in self.individuals.values() if indi.get("death") and indi["death"].get("year")]
        lifespans = [indi["lifespan_years"] for indi in self.individuals.values() if indi.get("lifespan_years") is not None and 0 <= indi["lifespan_years"] <= 120]

        surnames = [indi["surname"] for indi in self.individuals.values() if indi.get("surname")]
        top_surnames = Counter(surnames).most_common(10)

        earliest_birth = min(birth_years) if birth_years else None
        latest_death = max(death_years) if death_years else None
        avg_lifespan = round(sum(lifespans) / len(lifespans), 1) if lifespans else None

        return {
            "gedcom_version": self.header.get("gedcom_version", "5.5"),
            "total_individuals": total_indi,
            "total_families": total_fam,
            "total_sources": total_sour,
            "gender_breakdown": {
                "males": males,
                "females": females,
                "unknown": unknown_sex
            },
            "timeline": {
                "earliest_birth_year": earliest_birth,
                "latest_death_year": latest_death,
                "average_lifespan_years": avg_lifespan
            },
            "top_surnames": [{"surname": s, "count": c} for s, c in top_surnames]
        }

    def search_individuals(self, name: Optional[str] = None,
                           birth_from: Optional[int] = None, birth_to: Optional[int] = None,
                           death_from: Optional[int] = None, death_to: Optional[int] = None,
                           place: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        results = []
        name_lower = name.lower() if name else None
        place_lower = place.lower() if place else None

        for indi in self.individuals.values():
            if name_lower and name_lower not in indi["name"].lower():
                continue

            b_year = indi.get("birth", {}).get("year") if indi.get("birth") else None
            if birth_from is not None and (b_year is None or b_year < birth_from):
                continue
            if birth_to is not None and (b_year is None or b_year > birth_to):
                continue

            d_year = indi.get("death", {}).get("year") if indi.get("death") else None
            if death_from is not None and (d_year is None or d_year < death_from):
                continue
            if death_to is not None and (d_year is None or d_year > death_to):
                continue

            if place_lower:
                places = []
                if indi.get("birth") and indi["birth"].get("place"):
                    places.append(indi["birth"]["place"].lower())
                if indi.get("death") and indi["death"].get("place"):
                    places.append(indi["death"]["place"].lower())
                if not any(place_lower in p for p in places):
                    continue

            results.append(indi)
            if len(results) >= limit:
                break

        return results

    def get_ancestors_tree(self, indi_id: str, max_generations: int = 4) -> Optional[Dict[str, Any]]:
        indi = self.get_individual(indi_id)
        if not indi:
            return None

        def _recurse(current_id: str, gen: int) -> Dict[str, Any]:
            person = self.get_individual(current_id)
            if not person or gen > max_generations:
                return {}

            node = {
                "id": person["id"],
                "name": person["name"],
                "birth": person.get("birth"),
                "death": person.get("death"),
                "generation": gen,
                "father": None,
                "mother": None
            }

            if gen < max_generations:
                parents = self.get_parents(current_id)
                for p in parents:
                    if p.get("sex") == 'M' and not node["father"]:
                        node["father"] = _recurse(p["id"], gen + 1)
                    elif p.get("sex") == 'F' and not node["mother"]:
                        node["mother"] = _recurse(p["id"], gen + 1)
            return node

        return _recurse(indi_id, 1)

    def get_descendants_tree(self, indi_id: str, max_generations: int = 4) -> Optional[Dict[str, Any]]:
        indi = self.get_individual(indi_id)
        if not indi:
            return None

        def _recurse(current_id: str, gen: int) -> Dict[str, Any]:
            person = self.get_individual(current_id)
            if not person or gen > max_generations:
                return {}

            children_nodes = []
            if gen < max_generations:
                children = self.get_children_of_individual(current_id)
                for child in children:
                    c_node = _recurse(child["id"], gen + 1)
                    if c_node:
                        children_nodes.append(c_node)

            return {
                "id": person["id"],
                "name": person["name"],
                "birth": person.get("birth"),
                "death": person.get("death"),
                "generation": gen,
                "children": children_nodes
            }

        return _recurse(indi_id, 1)

    def validate_tree(self) -> Dict[str, Any]:
        anomalies = []

        for indi_id, indi in self.individuals.items():
            name = indi["name"]
            b_year = indi.get("birth", {}).get("year") if indi.get("birth") else None
            d_year = indi.get("death", {}).get("year") if indi.get("death") else None

            # 1. Death before birth
            if b_year and d_year and d_year < b_year:
                anomalies.append({
                    "type": "CHRONOLOGY_ERROR",
                    "severity": "HIGH",
                    "individual_id": indi_id,
                    "name": name,
                    "description": f"Death year ({d_year}) is prior to birth year ({b_year})."
                })

            # 2. Impossible lifespan (> 120 years)
            if b_year and d_year and (d_year - b_year) > 120:
                anomalies.append({
                    "type": "IMPOSSIBLE_LIFESPAN",
                    "severity": "HIGH",
                    "individual_id": indi_id,
                    "name": name,
                    "description": f"Calculated lifespan of {d_year - b_year} years exceeds standard threshold (120 years)."
                })

            # 3. Parent-child chronology
            parents = self.get_parents(indi_id)
            for parent in parents:
                pb_year = parent.get("birth", {}).get("year") if parent.get("birth") else None
                pd_year = parent.get("death", {}).get("year") if parent.get("death") else None

                if b_year and pb_year:
                    age_at_birth = b_year - pb_year
                    if age_at_birth < 0:
                        anomalies.append({
                            "type": "PARENT_BORN_AFTER_CHILD",
                            "severity": "CRITICAL",
                            "individual_id": indi_id,
                            "name": name,
                            "parent_id": parent["id"],
                            "parent_name": parent["name"],
                            "description": f"Child born in {b_year} before parent was born ({pb_year})."
                        })
                    elif age_at_birth < 12:
                        anomalies.append({
                            "type": "IMPROBABLE_PARENT_AGE",
                            "severity": "MEDIUM",
                            "individual_id": indi_id,
                            "name": name,
                            "parent_id": parent["id"],
                            "parent_name": parent["name"],
                            "description": f"Parent was only {age_at_birth} years old when child was born in {b_year}."
                        })
                    elif parent.get("sex") == 'F' and age_at_birth > 60:
                        anomalies.append({
                            "type": "IMPROBABLE_MOTHER_AGE",
                            "severity": "MEDIUM",
                            "individual_id": indi_id,
                            "name": name,
                            "parent_id": parent["id"],
                            "parent_name": parent["name"],
                            "description": f"Mother was {age_at_birth} years old at child birth in {b_year}."
                        })

                if b_year and pd_year:
                    if parent.get("sex") == 'F' and b_year > pd_year:
                        anomalies.append({
                            "type": "BORN_AFTER_MOTHER_DEATH",
                            "severity": "CRITICAL",
                            "individual_id": indi_id,
                            "name": name,
                            "parent_id": parent["id"],
                            "parent_name": parent["name"],
                            "description": f"Child born in {b_year} after mother's death in {pd_year}."
                        })
                    elif parent.get("sex") == 'M' and b_year > (pd_year + 1):
                        anomalies.append({
                            "type": "BORN_AFTER_FATHER_DEATH",
                            "severity": "HIGH",
                            "individual_id": indi_id,
                            "name": name,
                            "parent_id": parent["id"],
                            "parent_name": parent["name"],
                            "description": f"Child born in {b_year}, more than 1 year after father's death in {pd_year}."
                        })

        # 4. Check for potential duplicates in tree
        duplicates = self._find_potential_tree_duplicates()

        return {
            "total_anomalies": len(anomalies),
            "anomalies": anomalies,
            "potential_duplicates": duplicates
        }

    def _find_potential_tree_duplicates(self) -> List[Dict[str, Any]]:
        potential_dups = []
        name_map = defaultdict(list)
        for indi in self.individuals.values():
            if indi["name"] and indi["name"] != "Unnamed Individual":
                key = (indi["given_name"].lower(), indi["surname"].lower())
                if key[0] and key[1]:
                    name_map[key].append(indi)

        for (given, surname), group in name_map.items():
            if len(group) > 1:
                for i in range(len(group)):
                    for j in range(i + 1, len(group)):
                        p1 = group[i]
                        p2 = group[j]
                        b1 = p1.get("birth", {}).get("year") if p1.get("birth") else None
                        b2 = p2.get("birth", {}).get("year") if p2.get("birth") else None
                        if b1 and b2 and abs(b1 - b2) <= 2:
                            potential_dups.append({
                                "individual_1": {"id": p1["id"], "name": p1["name"], "birth_year": b1},
                                "individual_2": {"id": p2["id"], "name": p2["name"], "birth_year": b2},
                                "confidence": "HIGH" if b1 == b2 else "MODERATE",
                                "rationale": f"Matching name '{p1['name']}' with close birth years ({b1} vs {b2})."
                            })

        return potential_dups


def main():
    parser = argparse.ArgumentParser(description="Nadia GEDCOM Parser & Genealogy Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # parse
    p_parse = subparsers.add_parser("parse", help="Parse a GEDCOM file and output raw JSON structure")
    p_parse.add_argument("--file", required=True, help="Path to .ged file")
    p_parse.add_argument("--output", help="Optional output JSON file path")

    # summary
    p_sum = subparsers.add_parser("summary", help="Generate statistical summary of GEDCOM dataset")
    p_sum.add_argument("--file", required=True, help="Path to .ged file")

    # individual
    p_indi = subparsers.add_parser("individual", help="Inspect individual details, vitals, and immediate family")
    p_indi.add_argument("--file", required=True, help="Path to .ged file")
    p_indi.add_argument("--id", help="Individual XREF ID (e.g. @I1@)")
    p_indi.add_argument("--name", help="Search name if ID is unknown")

    # family
    p_fam = subparsers.add_parser("family", help="Inspect family record details (parents & children)")
    p_fam.add_argument("--file", required=True, help="Path to .ged file")
    p_fam.add_argument("--id", required=True, help="Family XREF ID (e.g. @F1@)")

    # ancestors
    p_anc = subparsers.add_parser("ancestors", help="Generate recursive ancestor pedigree tree")
    p_anc.add_argument("--file", required=True, help="Path to .ged file")
    p_anc.add_argument("--id", required=True, help="Individual XREF ID")
    p_anc.add_argument("--generations", type=int, default=4, help="Number of ancestral generations (default: 4)")

    # descendants
    p_desc = subparsers.add_parser("descendants", help="Generate recursive descendant tree")
    p_desc.add_argument("--file", required=True, help="Path to .ged file")
    p_desc.add_argument("--id", required=True, help="Individual XREF ID")
    p_desc.add_argument("--generations", type=int, default=4, help="Number of descendant generations (default: 4)")

    # search
    p_search = subparsers.add_parser("search", help="Search individuals by criteria")
    p_search.add_argument("--file", required=True, help="Path to .ged file")
    p_search.add_argument("--name", help="Name query")
    p_search.add_argument("--birth-from", type=int, help="Earliest birth year")
    p_search.add_argument("--birth-to", type=int, help="Latest birth year")
    p_search.add_argument("--death-from", type=int, help="Earliest death year")
    p_search.add_argument("--death-to", type=int, help="Latest death year")
    p_search.add_argument("--place", help="Birth/Death place keyword")
    p_search.add_argument("--limit", type=int, default=20, help="Max results")

    # validate
    p_val = subparsers.add_parser("validate", help="Run logical validation checks and find anomalies")
    p_val.add_argument("--file", required=True, help="Path to .ged file")

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(json.dumps({"error": f"File not found: {args.file}"}), file=sys.stderr)
        sys.exit(1)

    try:
        db = GedcomDatabase.parse_file(args.file)
    except Exception as e:
        print(json.dumps({"error": f"Failed to parse GEDCOM file: {str(e)}"}), file=sys.stderr)
        sys.exit(1)

    result: Any = {}

    if args.command == "parse":
        result = {
            "header": db.header,
            "total_individuals": len(db.individuals),
            "total_families": len(db.families),
            "individuals": db.individuals,
            "families": db.families
        }
        if args.output:
            with open(args.output, "w", encoding="utf-8") as out:
                json.dump(result, out, indent=2)
            print(json.dumps({"status": "SUCCESS", "saved_to": args.output, "total_individuals": len(db.individuals)}))
            return

    elif args.command == "summary":
        result = db.get_summary()

    elif args.command == "individual":
        target_id = args.id
        if not target_id and args.name:
            matches = db.search_individuals(name=args.name, limit=1)
            if matches:
                target_id = matches[0]["id"]
            else:
                result = {"error": f"No individual matching name: {args.name}"}
                print(json.dumps(result, indent=2))
                return

        if not target_id:
            result = {"error": "Must specify --id or --name"}
        else:
            indi = db.get_individual(target_id)
            if not indi:
                result = {"error": f"Individual {target_id} not found"}
            else:
                parents = db.get_parents(target_id)
                spouses = db.get_spouses(target_id)
                children = db.get_children_of_individual(target_id)
                siblings = db.get_siblings(target_id)
                result = {
                    "individual": indi,
                    "parents": [{"id": p["id"], "name": p["name"], "sex": p["sex"], "birth": p.get("birth")} for p in parents],
                    "spouses": [{"id": s["id"], "name": s["name"], "birth": s.get("birth")} for s in spouses],
                    "children": [{"id": c["id"], "name": c["name"], "birth": c.get("birth")} for c in children],
                    "siblings": [{"id": b["id"], "name": b["name"], "birth": b.get("birth")} for b in siblings]
                }

    elif args.command == "family":
        fam = db.get_family(args.id)
        if not fam:
            result = {"error": f"Family {args.id} not found"}
        else:
            husb = db.get_individual(fam["husband_id"]) if fam.get("husband_id") else None
            wife = db.get_individual(fam["wife_id"]) if fam.get("wife_id") else None
            children = [db.get_individual(cid) for cid in fam.get("children_ids", []) if db.get_individual(cid)]
            result = {
                "family": fam,
                "husband": husb,
                "wife": wife,
                "children": children
            }

    elif args.command == "ancestors":
        tree = db.get_ancestors_tree(args.id, max_generations=args.generations)
        result = tree if tree else {"error": f"Individual {args.id} not found"}

    elif args.command == "descendants":
        tree = db.get_descendants_tree(args.id, max_generations=args.generations)
        result = tree if tree else {"error": f"Individual {args.id} not found"}

    elif args.command == "search":
        result = {
            "results": db.search_individuals(
                name=args.name,
                birth_from=args.birth_from,
                birth_to=args.birth_to,
                death_from=args.death_from,
                death_to=args.death_to,
                place=args.place,
                limit=args.limit
            )
        }

    elif args.command == "validate":
        result = db.validate_tree()

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
