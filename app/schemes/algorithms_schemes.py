from pydantic import BaseModel, validator
from uuid import UUID
import ast

def _validate_algorithm_script(script_code: str):
    """
    A robust, multi-step validator for the algorithm script.
    Raises ValueError for any validation failures.
    """
    if not script_code:
        raise ValueError("Script cannot be empty.")

    # Step 1: Check for Python syntax errors.
    try:
        tree = ast.parse(script_code)
    except SyntaxError as e:
        # This is the most critical check for errors like the user reported.
        raise ValueError(f"Script has a syntax error: {e}")

    # Step 2: Ensure a 'simulate' function is defined.
    simulate_function_found = False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == 'simulate':
            simulate_function_found = True
            # Step 3: Check the function signature (number of arguments).
            args = [arg.arg for arg in node.args.args]
            required_args = ['current_time', 'base_consumption', 'peak_consumption',
                               'cycle_duration', 'on_duration', 'extra_params']
            if len(args) != len(required_args):
                raise ValueError(f"The 'simulate' function must have exactly {len(required_args)} arguments: {', '.join(required_args)}")
            
            # Optional: Check argument names, though signature length is often enough.
            for i, arg_name in enumerate(args):
                if arg_name != required_args[i]:
                     raise ValueError(f"Argument {i+1} should be '{required_args[i]}', but is named '{arg_name}'")
            break
    
    if not simulate_function_found:
        raise ValueError("Script must contain a function named 'simulate'.")

    # Step 4: Execute the function with test data to check for runtime errors and return type.
    try:
        exec_env = {}
        exec(script_code, {}, exec_env)
        simulate_func = exec_env["simulate"]

        test_result = simulate_func(
            current_time=1000, base_consumption=10.0, peak_consumption=20.0,
            cycle_duration=60, on_duration=30, extra_params={}
        )

        if not isinstance(test_result, (int, float)):
            raise ValueError(f"The 'simulate' function must return a number (int or float), but it returned a {type(test_result).__name__}.")
        
        # Check for NaN or infinity
        import math
        if math.isnan(test_result) or math.isinf(test_result):
            raise ValueError("The 'simulate' function returned a non-finite number (NaN or infinity).")

    except ValueError:
        raise # Re-raise our own validation errors.
    except Exception as e:
        # Catch errors from the script's execution.
        raise ValueError(f"The 'simulate' function failed during test execution: {e}")


class AlgorithmCreate(BaseModel):
    name: str
    description: str | None = None
    algorithm_type: str
    script: str
    
    @validator('script')
    def validate_script(cls, v):
        _validate_algorithm_script(v)
        return v

class AlgorithmUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    algorithm_type: str | None = None
    script: str | None = None
    
    @validator('script')
    def validate_script(cls, v):
        if v is not None:
            _validate_algorithm_script(v)
        return v

class AlgorithmResponse(BaseModel):
    id: UUID
    name: str
    description: str | None = None
    algorithm_type: str
    script: str
