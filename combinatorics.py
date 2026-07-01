from itertools import combinations

def load_recipes(file_path):
    """Reads the fusion database from a text file and returns a recipe dict and a set of all valid card names."""
    recipes = {}
    all_known_cards = set()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if "=" not in line:
                    continue
                
                materials_part, result = line.split("=")
                card1, card2 = materials_part.split("+")
                
                c1, c2 = card1.strip(), card2.strip()
                all_known_cards.add(c1)
                all_known_cards.add(c2)
                
                key = tuple(sorted([c1, c2]))
                recipes[key] = result.strip()
                
    except FileNotFoundError:
        print(f"Error: The recipe file '{file_path}' was not found.")
        
    return recipes, all_known_cards

def load_hand_with_fuzzy_search(file_path, all_known_cards):
    """Reads your hand from a text file and resolves partial names to full card names."""
    hand = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                search_term = line.strip().lower()
                
                if not search_term:
                    continue
                
                # Try to find any cards in the database that match the partial string
                # matches = [card for card in all_known_cards if search_term in card.lower()]
                matches = []
                for card in all_known_cards:
                    # print(card)
                    if search_term in card.lower():
                        matches.append(card)


                if len(matches) == 1:
                    # Perfect! Found exactly one match
                    hand.append(matches[0])
                elif len(matches) > 1:
                    # Ambigous search: matches multiple cards
                    print(f"⚠️ Warning: '{line.strip()}' is ambiguous. It matches: {matches}. (Skipping)")
                else:
                    # No card found
                    print(f"❌ Error: Could not find any card matching '{line.strip()}' in the database.")
    except FileNotFoundError:
        print(f"Error: The hand file '{file_path}' was not found.")
    return hand

def find_possible_fusions(card_list, recipe_db):
    """Finds matching fusions based on the resolved card list."""
    valid_fusions = []
    pairs = combinations(card_list, 2)
    
    for card1, card2 in pairs:
        lookup_key = tuple(sorted([card1, card2]))
        if lookup_key in recipe_db:
            valid_fusions.append({
                "materials": (card1, card2),
                "result": recipe_db[lookup_key]
            })
            
    return valid_fusions

# --- Main Execution ---
if __name__ == "__main__":
    # 1. Load the master recipe rules and extract every unique card name
    fusion_database, known_cards = load_recipes(r"yugioh fusions.txt")
    
    # 2. Load your hand (now allowing partial names)
    my_cards = load_hand_with_fuzzy_search(r"cards.txt", known_cards)
    
    if my_cards and fusion_database:
        print(f"\nSuccessfully resolved hand to: {my_cards}\n")
        
        # 3. Find matches
        fusions = find_possible_fusions(my_cards, fusion_database)
        
        if fusions:
            print("Possible Fusions Found:")
            for f in fusions:
                m1, m2 = f["materials"]
                print(f" * {m1} + {m2} -> {f['result']}")
        else:
            print("No possible fusions found with your current hand.")
