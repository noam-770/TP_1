import subprocess
import sys
from pathlib import Path

def test_multiple_inputs():
    """Test pour un programme qui demande alphabet et nombre de lettres"""
    test_cases = [
        {
            'name': 'alphabet et nombre de lettres inférieur à la taille de l\'alphabet',
            'input': 'abcde\n4\n',
            'expected_in_output': ['abcd']
        },
        {
            'name': 'alphabet avec caractères spéciaux et nombre de lettres inférieur à la taille de l\'alphabet',
            'input': 'aA1@!2\n4\n',
            'expected_in_output': ['aA1@']
        },
        {
            'name': 'alphabet et nombre de lettres supérieur à la taille de l\'alphabet',
            'input': 'azerty\n9\n',
            'expected_in_output': ['azertyaze']
        },
        {
            'name': 'alphabet et nombre de lettres négatif',
            'input': 'azerty\n-9\n',
            'expected_in_output': ['']
        },
        {
            'name': 'alphabet et nombre de lettres non numérique',
            'input': 'azerty\na\n',
            'expected_in_output': ['']
        }
    ]
    return test_cases

def run_cpp_tests(executable, test_cases, timeout_duration=10):
    """Exécute une série de tests sur un programme C++"""
    
    print(f"Test du programme: {executable}")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test {i}/{len(test_cases)}: {test_case['name']} ---")
        
        try:
            # Affichage de l'entrée envoyée
            print(f"Entrée envoyée: {repr(test_case['input'])}")
            
            # Exécution du programme
            result = subprocess.run(
                [executable],
                input=test_case['input'],
                text=True,
                capture_output=True,
                timeout=timeout_duration
            )
            
            print(f"Code de retour: {result.returncode}")
            print(f"Sortie complète:")
            print(f"STDOUT: {repr(result.stdout)}")
            if result.stderr:
                print(f"STDERR: {repr(result.stderr)}")
            
            # Vérification des résultats attendus
            success = True
            
            if 'expected_in_output' in test_case:
                expected = test_case['expected_in_output']
                
                if isinstance(expected, list):
                    # Vérifier que tous les éléments sont présents
                    for item in expected:
                        if str(item).lower() not in result.stdout.lower():
                            print(f"⚠ Élément manquant: '{item}'")
                            success = False
                else:
                    # Vérifier qu'un seul élément est présent
                    if str(expected).lower() not in result.stdout.lower():
                        print(f"⚠ Sortie attendue non trouvée: '{expected}'")
                        success = False
            
            if 'expected_returncode' in test_case:
                if result.returncode != test_case['expected_returncode']:
                    print(f"⚠ Code de retour incorrect. Attendu: {test_case['expected_returncode']}, Reçu: {result.returncode}")
                    success = False
            
            if success:
                print("✓ Test réussi!")
            else:
                print("✗ Test échoué!")
                return 1
                
        except subprocess.TimeoutExpired:
            print("✗ Timeout - le programme ne répond pas")
        except Exception as e:
            print(f"✗ Erreur lors du test: {e}")

def main():
    """Fonction principale pour tester votre programme C++"""
    
    # Compilation
    try:
        print("Compilation du programme C++...")
        subprocess.run(["g++", "genemdp.cpp", "-o", "genemdp"], check=True, timeout=30)
        print("✓ Compilation réussie!")
    except subprocess.CalledProcessError as e:
        print(f"✗ Erreur de compilation: {e}")
        return
    
    # Déterminer l'exécutable
    executable = "./genemdp.exe" if sys.platform == "win32" else "./genemdp"
    if not Path(executable).exists():
        executable = "./genemdp" if sys.platform == "win32" else "./genemdp.exe"
    
    if not Path(executable).exists():
        print("✗ Exécutable non trouvé après compilation")
        return
    
    test_cases = test_multiple_inputs()
    
    return run_cpp_tests(executable, test_cases)

if __name__ == "__main__":
    sys.exit(main())