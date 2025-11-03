import pulp

def resoudre_prog_lineaire(direction: str, 
                         fonction_obj: dict[str, float], 
                         contraintes: list[dict]) -> tuple[str, float, dict[str, float]]:
    """
    Résout un problème de programmation linéaire avec PuLP. [cite: 17, 27]

    Args:
        direction: "Maximiser" ou "Minimiser".
        fonction_obj: Dictionnaire des coefficients. Ex: {'x': 3, 'y': 2}
        contraintes: Liste de dictionnaires de contraintes.
                     Ex: [{'coeffs': {'x': 1, 'y': 1}, 'type': '<=', 'rhs': 10},
                          {'coeffs': {'x': 2, 'y': 1}, 'type': '>=', 'rhs': 5}]

    Returns:
        Un tuple (statut, valeur_objectif, valeurs_variables).
    """
    
    # 1. Définir la direction du problème
    if direction == "Maximiser":
        prob = pulp.LpProblem("Mon_Probleme_PL", pulp.LpMaximize)
    else:
        prob = pulp.LpProblem("Mon_Probleme_PL", pulp.LpMinimize)

    # 2. Définir les variables (nous les "devinons" à partir des entrées)
    noms_variables = set(fonction_obj.keys())
    for c in contraintes:
        noms_variables.update(c['coeffs'].keys())
    
    variables = pulp.LpVariable.dicts("Var", noms_variables, lowBound=0) # On suppose les variables >= 0

    # 3. Ajouter la fonction objectif
    prob += pulp.lpSum([fonction_obj.get(v, 0) * variables[v] for v in noms_variables]), "Fonction_Objectif"

    # 4. Ajouter les contraintes
    for i, c in enumerate(contraintes):
        expression = pulp.lpSum([c['coeffs'].get(v, 0) * variables[v] for v in noms_variables])
        
        if c['type'] == '<=':
            prob += expression <= c['rhs'], f"Contrainte_{i}"
        elif c['type'] == '>=':
            prob += expression >= c['rhs'], f"Contrainte_{i}"
        elif c['type'] == '==':
            prob += expression == c['rhs'], f"Contrainte_{i}"

    # 5. Résoudre le problème
    try:
        prob.solve(pulp.PULP_CBC_CMD(msg=0)) # msg=0 pour cacher les logs de Cbc
    except Exception as e:
        return f"Erreur lors de la résolution: {e}", 0, {}

    # 6. Formater et retourner les résultats
    statut = pulp.LpStatus[prob.status]
    valeur_obj = pulp.value(prob.objective)
    valeurs_vars = {v.name: v.varValue for v in prob.variables()}
    
    return statut, valeur_obj, valeurs_vars