from datetime import date

class ScoringConfig:
    def __init__(self, w_importance=0.5, w_urgency=0.3, w_effort=0.1, w_dependencies=0.1):
        self.w_importance = w_importance
        self.w_urgency = w_urgency
        self.w_effort = w_effort
        self.w_dependencies = w_dependencies

def days_until(due_date):
    if due_date is None:
        return None
    today = date.today()
    delta = (due_date - today).days
    return delta

def urgency_score(due_date):
    d = days_until(due_date)
    if d is None:
        return 0.3
    if d < 0: return 1.0
    if d == 0: return 0.9
    if d <= 3: return 0.7
    if d <= 7: return 0.5
    if d <= 14: return 0.3
    return 0.1

def effort_score(estimated_hours):
    if estimated_hours is None or estimated_hours <= 0:
        return 0.5
    if estimated_hours <= 1: return 1.0
    if estimated_hours <= 3: return 0.8
    if estimated_hours <= 5: return 0.6
    if estimated_hours <= 8: return 0.4
    return 0.2

def dependency_score(num_dependents):
    if num_dependents == 0: return 0.2
    if num_dependents == 1: return 0.5
    if num_dependents <= 3: return 0.8
    return 1.0

# NEW: Multiple scoring strategies
def fastest_wins_score(task, num_dependents):
    """Prioritize quick tasks (low effort)"""
    return effort_score(task.get('estimated_hours')) * 100

def high_impact_score(task, num_dependents):
    """Prioritize important tasks only"""
    return (task['importance'] / 10.0) * 100

def deadline_driven_score(task, num_dependents):
    """Prioritize urgent/overdue tasks"""
    return urgency_score(task.get('due_date')) * 100

def smart_balance_score(task, num_dependents, config=None):
    """Balanced approach (your original)"""
    if config is None:
        config = ScoringConfig()
    imp_norm = task['importance'] / 10.0
    u = urgency_score(task.get('due_date'))
    e = effort_score(task.get('estimated_hours'))
    dep = dependency_score(num_dependents)
    score = (config.w_importance * imp_norm + config.w_urgency * u + 
             config.w_effort * e + config.w_dependencies * dep) * 100.0
    return round(score, 2)

# Strategy selector
STRATEGIES = {'fastest_wins': fastest_wins_score,
    'high_impact': high_impact_score,
    'deadline_driven': deadline_driven_score,
    'smart_balance': smart_balance_score
} 