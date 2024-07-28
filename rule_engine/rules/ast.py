import re
import operator as op
import json

class ASTNode:
    def __init__(self, type, value, left=None, right=None):
        self.type = type
        self.value = value
        self.left = left
        self.right = right

    def to_dict(self):
        """Convert ASTNode to a dictionary."""
        return {
            'type': self.type,
            'value': self.value,
            'left': self.left.to_dict() if self.left else None,
            'right': self.right.to_dict() if self.right else None
        }

def create_rule(rule_string):
    """
    Create an AST from a rule string.
    This function parses the rule string and converts it into an AST.
    """
    def parse_expression(expression):
        # Base case: if the expression is simple (e.g., "age > 30")
        if ' ' not in expression:
            return ASTNode(type='operand', value=expression).to_dict()

        # Split the expression by the operator
        parts = split_expression(expression, 'AND')
        if not parts:
            parts = split_expression(expression, 'OR')

        if len(parts) == 2:
            left_expr = parse_expression(parts[0])
            right_expr = parse_expression(parts[1])
            operator = 'AND' if 'AND' in expression else 'OR'
            return ASTNode(type='operator', value=operator, left=left_expr, right=right_expr).to_dict()

        return ASTNode(type='operand', value=expression).to_dict()

    def split_expression(expression, operator):
        # Simple split; assumes operator is not within sub-expressions
        level = 0
        parts = []
        current = ''
        for char in expression:
            if char == '(':
                level += 1
            elif char == ')':
                level -= 1
            elif char == ' ' and level == 0 and expression.startswith(operator, len(current)):
                parts.append(current.strip())
                current = ''
                continue
            current += char
        parts.append(current.strip())
        return parts

    rule_string = rule_string.strip()
    if not rule_string:
        raise ValueError("Empty rule string")

    return parse_expression(rule_string)

def combine_rules(rules, ast_json=None):
    """
    Combine multiple rules into a single AST.
    This function creates a combined AST from a list of rule strings and/or an existing AST JSON.
    """
    def merge_asts(ast1, ast2):
        # Simplistic merging strategy; assumes AND combination
        return ASTNode(type='operator', value='AND', left=ast1, right=ast2)

    asts = [create_rule(rule) for rule in rules]
    if ast_json:
        root = dict_to_ast(ast_json)
        asts.append(root)
    
    if not asts:
        return None
    
    combined_ast = asts[0]
    for ast in asts[1:]:
        combined_ast = merge_asts(combined_ast, ast)
    
    # Convert combined AST to dictionary before returning
    return ast_to_dict(combined_ast)

def evaluate_ast(node, user_data):
    """
    Evaluate an ASTNode against user data.
    """
    if isinstance(node, dict):  # Convert dict to ASTNode if necessary
        node = dict_to_ast(node)
    
    if node.type == 'operand':
        # Directly evaluate the operand
        return evaluate_operand(node.value, user_data)
    
    elif node.type == 'operator':
        left_result = evaluate_ast(node.left, user_data)
        right_result = evaluate_ast(node.right, user_data)
        
        if node.value == 'AND':
            return left_result and right_result
        elif node.value == 'OR':
            return left_result or right_result
        else:
            raise ValueError(f"Unknown operator: {node.value}")
    
    else:
        raise ValueError(f"Unknown node type: {node.type}")

def evaluate_operand(operand, user_data):
    import operator

    # Define possible operators and their corresponding functions
    operators = {
        '==': operator.eq,
        '!=': operator.ne,
        '>': operator.gt,
        '<': operator.lt,
        '>=': operator.ge,
        '<=': operator.le,
        '=': operator.eq  # Add '=' as an alias for '=='
    }

    # Split operand into attribute, operator, and value
    for op in operators:
        if op in operand:
            attribute, value = operand.split(op, 1)
            attribute = attribute.strip()
            value = value.strip()
            value = eval(value)  # Convert to integer or other types as necessary
            # Check if attribute exists in user_data
            if attribute in user_data:
                # Evaluate the condition
                return operators[op](user_data[attribute], value)
            else:
                raise ValueError(f"Attribute '{attribute}' not found in user data")

    raise ValueError(f"Unknown operator in operand: {operand}")

def dict_to_ast(data):
    """
    Convert a dictionary representation of an AST to an ASTNode object.
    """
    if not data:
        return None
    return ASTNode(
        type=data.get('type'),
        value=data.get('value'),
        left=dict_to_ast(data.get('left')),
        right=dict_to_ast(data.get('right'))
    )

def ast_to_dict(node):
    """
    Convert an ASTNode object to a dictionary representation.
    """
    if isinstance(node, dict):
        # If node is already a dictionary, return it as is
        return node
    elif isinstance(node, ASTNode):
        # If node is an ASTNode object, convert it to a dictionary
        return {
            'type': node.type,
            'value': node.value,
            'left': ast_to_dict(node.left),
            'right': ast_to_dict(node.right)
        }
    else:
        # If node is neither a dict nor ASTNode, return None
        return None


# Example of converting an AST to JSON
def ast_to_json(node):
    """Convert ASTNode object to a JSON string."""
    return json.dumps(ast_to_dict(node))

# Example of converting JSON to AST
def json_to_ast(json_str):
    """Convert a JSON string to an ASTNode object."""
    return dict_to_ast(json.loads(json_str))
