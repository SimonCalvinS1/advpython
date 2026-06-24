from abc import ABC, abstractmethod

class AllergyClass(ABC):
    def __init__(self, rule_name):
        self.rule_name = rule_name
    @abstractmethod
    def evaluate(self, ingredients_text, user_allergies):
        pass



class StrictAllergy(AllergyClass):
    def evaluate(self, ingredients_text, user_allergies):
        unsafe_found = []
        for allergen in user_allergies:
            if allergen.strip().lower() in ingredients_text.lower():
                unsafe_found.append(allergen.strip())
        if unsafe_found:
            return f"Critical Danger because it contains: {', '.join(unsafe_found)}"
        return "Safe"


class FoodLimitation(AllergyClass):
    def evaluate(self, ingredients_text, user_allergies):
        warnings_found = []
        for allergen in user_allergies:
            if allergen.strip().lower() in ingredients_text.lower():
                warnings_found.append(allergen.strip())
                
        if warnings_found:
            return f"Warning because it contains: {', '.join(warnings_found)}"
        return "Safe"


class UserProfile:
    def __init__(self, name, allergies, severity_level):
        self.name = name
        if not isinstance(allergies, list) or len(allergies) == 0 or allergies == [""]:
            raise ValueError("Profile creation failed because no list of at least one allergen")
        self.allergies = allergies
        self.severity_level = severity_level
    def display_profile(self):
        return f"\nProfile is created\nUser: {self.name}\nAllergies: {', '.join(self.allergies)}\nSeverity: {self.severity_level}\n\n"


class EmptyMenuError(Exception):
    pass


def main():
    print("\t\tSafeBite is your allergy companion")
    try:
        name = input("Enter user name: ").strip()
        if not name:
            raise ValueError("Name cannot be left blank.")
        raw_allergies = input("Enter allergies (separated by commas, e.g., peanut, milk, soy): ")
        allergies_list = [a.strip() for a in raw_allergies.split(",") if a.strip()]
        print("\nSelect Allergy Severity Level:")
        print("1. Severe")
        print("2. Mild")
        choice = input("Enter choice (1 or 2): ").strip()
        if choice == "1":
            severity = "Severe"
            chosen_rule = StrictAllergy("More allergy")
        elif choice == "2":
            severity = "Mild"
            chosen_rule = FoodLimitation("Little allergy")
        else:
            print("Wrong choice, choosing severe")
            severity = "Severe"
            chosen_rule = StrictAllergy("More allergy")
        user = UserProfile(name, allergies_list, severity)
        print(user.display_profile())
    except ValueError as ve:
        print(f"\nProfile registration error: {ve}")
        return

    print("\nFood Item Check")
    meal_name = input("Mention what you are planning to eat (like Biriyani, Curd Rice): ").strip()
    ingredients = input(f"Tell me the ingredients for {meal_name}: ").strip()
    try:
        if not ingredients:
            raise EmptyMenuError("Exception: ingredients are empty")
        print(f"\nDoing analysis for {user.name}: {chosen_rule.rule_name} now")
        verdict = chosen_rule.evaluate(ingredients, user.allergies)
        print("\nResult is here:-")
        print(f"Meal Analysed: {meal_name}")
        print(f"Result for {user.name}: {verdict}")
    except EmptyMenuError as eme:
        print(f"\n[Application Error]: {eme}")
    except Exception as e:
        print(f"\n[Unexpected Error Occurring]: {e}")

main()