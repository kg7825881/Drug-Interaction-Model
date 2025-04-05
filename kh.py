# drug_interaction_checker.py

from typing import List, Dict

# Sample drug database (should be replaced with real-time API or database)
DRUG_DATABASE = {
    "Combiflam": {"Paracetamol": 500, "Ibuprofen": 400},
    "Crocin": {"Paracetamol": 500},
    "Advil": {"Ibuprofen": 200},
    "Disprin": {"Aspirin": 325},
}

SIDE_EFFECTS_DB = {
    "Paracetamol": ["Liver damage in high doses"],
    "Ibuprofen": ["Stomach pain", "Nausea", "Bleeding risk"],
    "Aspirin": ["Gastric irritation", "Bleeding"],
}

INTERACTIONS = {
    ("Paracetamol", "Ibuprofen"): "Generally safe but monitor for gastrointestinal issues",
    ("Ibuprofen", "Aspirin"): "Increased risk of bleeding",
}

SAFE_LIMITS = {
    "Paracetamol": 4000,
    "Ibuprofen": 1200,
    "Aspirin": 4000
}

def check_drugs(drugs: List[str]):
    drug_data: Dict[str, Dict[str, int]] = {}
    component_totals = {}
    warnings = []
    interactions_found = []
    side_effects_info = {}

    # Extract composition
    for drug in drugs:
        if drug not in DRUG_DATABASE:
            print(f"❌ Drug '{drug}' not found in database.")
            return
        composition = DRUG_DATABASE[drug]
        drug_data[drug] = composition
        for comp, dose in composition.items():
            component_totals[comp] = component_totals.get(comp, 0) + dose

    # Check for overdose
    for comp, total_dose in component_totals.items():
        limit = SAFE_LIMITS.get(comp)
        if limit and total_dose > limit:
            warnings.append({
                "component": comp,
                "total_dosage": total_dose,
                "limit": limit,
                "warning": f"Exceeds safe limit of {limit}mg"
            })

    # Check for interactions
    components = list(component_totals.keys())
    for i in range(len(components)):
        for j in range(i + 1, len(components)):
            pair = (components[i], components[j])
            reverse_pair = (components[j], components[i])
            if pair in INTERACTIONS:
                interactions_found.append({"between": pair, "effect": INTERACTIONS[pair]})
            elif reverse_pair in INTERACTIONS:
                interactions_found.append({"between": reverse_pair, "effect": INTERACTIONS[reverse_pair]})

    # Gather side effects
    for comp in component_totals:
        side_effects_info[comp] = SIDE_EFFECTS_DB.get(comp, ["No data available"])

    # Output results
    print("\n✅ Drug Compositions:")
    for drug, comps in drug_data.items():
        print(f"  {drug}: {comps}")

    print("\n🧪 Total Components:")
    for comp, total in component_totals.items():
        print(f"  {comp}: {total}mg")

    if warnings:
        print("\n⚠️ Overdose Warnings:")
        for warn in warnings:
            print(f"  {warn['component']}: {warn['total_dosage']}mg - {warn['warning']}")
    else:
        print("\n✅ No overdose detected.")

    if interactions_found:
        print("\n🔁 Interactions Found:")
        for inter in interactions_found:
            print(f"  Between {inter['between'][0]} and {inter['between'][1]}: {inter['effect']}")
    else:
        print("\n✅ No interactions found.")

    print("\n📋 Side Effects:")
    for comp, effects in side_effects_info.items():
        print(f"  {comp}: {', '.join(effects)}")

if __name__ == "__main__":
    user_input = input("Enter drug names separated by commas (e.g. Combiflam,Crocin): ")
    drug_list = [d.strip() for d in user_input.split(",")]
    check_drugs(drug_list)
