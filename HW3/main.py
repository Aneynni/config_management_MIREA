#!/bin/python3
import yaml
import argparse
import sys
import re

def parse_yaml_file(file_path):
    with open(file_path, 'r') as file:
        try:
            lines = file.readlines()
            data = yaml.safe_load(''.join(lines))
            return data, lines
        except yaml.YAMLError as exc:
            print(f"Error parsing YAML file: {exc}")
            sys.exit(1)

def extract_comments(lines):
    comments = []
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith('#'):
            comments.append(stripped_line[1:].strip())
    return comments
def evaluate_expression(expression, context):
    match_pow = re.match(r'^\{pow (\w+) (\w+)\}$', expression)
    if match_pow:
        base_var, exp_var = match_pow.groups()
        if base_var in context and exp_var in context:
            return context[base_var] ** context[exp_var]
        else:
            raise ValueError(f"One of the variables {base_var} or {exp_var} not found in context")

    match = re.match(r'^\{\+ (\w+) (\d+)\}$', expression)
    if match:
        print("HERE")
        var_name, number = match.groups()
        number = int(number)
        if var_name in context:
            return context[var_name] + number
        else:
            raise ValueError(f"Variable {var_name} not found in context")
    else:
        raise ValueError(f"Invalid expression format: {expression}")
 
    raise ValueError(f"Invalid expression format: {expression}")

def transform_data(data, context=None):
    if context is None:
        context = data
    
    if isinstance(data, dict):
        return transform_dict(data, context)
    elif isinstance(data, int) or isinstance(data, float):
        return str(data)
    elif isinstance(data, str) and data.startswith('{') and data.endswith('}'):
        return str(evaluate_expression(data, context))
    else:
        raise ValueError("Unsupported data type")

def transform_dict(data_dict, context):
    transformed = "$[\n"
    for key, value in data_dict.items():
        if not is_valid_name(key):
            raise ValueError(f"Invalid identifier name: {key}")
        transformed += f" {key} : {transform_data(value, context)},\n"
    transformed += "]"
    return transformed

def transform_dict(data_dict, context):
    transformed = "$[\n"
    for key, value in data_dict.items():
        if not is_valid_name(key):
            raise ValueError(f"Invalid identifier name: {key}")
        transformed += f" {key} : {transform_data(value, context)},\n"
    transformed += "]"
    return transformed

def is_valid_name(name):
    return re.match(r'^[_A-Z][_a-zA-Z0-9]*$', name) is not None

def main():
    parser = argparse.ArgumentParser(description='YAML to Custom Config Language Converter')
    parser.add_argument('file_path', help='Path to the YAML file')
    args = parser.parse_args()

    data, lines = parse_yaml_file(args.file_path)
    transformed_data = transform_data(data)
    
    comments = extract_comments(lines)
    comment_text = '\n'.join([f"|| {comment}" for comment in comments])

    output = f"{comment_text}\n{transformed_data}"
    
    print(output)

if __name__ == "__main__":
    main()

