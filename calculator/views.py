from django.shortcuts import render
from django.http import JsonResponse
import math
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Calculation  # Import the model
from django.utils import timezone
from django.views.decorators.http import require_GET

def calculator_view(request):
    return render(request, 'calculator/index.html')

@csrf_exempt
def calculate(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            expression = data.get('expression', '')
            operation = data.get('operation', '')
            
            result = None
            error = None
            
            try:
                if operation == 'sqrt':
                    num = float(expression)
                    if num < 0:
                        error = "Cannot calculate square root of negative number"
                    else:
                        result = math.sqrt(num)
                
                elif operation == 'factorial':
                    num = int(float(expression))
                    if num < 0:
                        error = "Factorial cannot be negative"
                    else:
                        result = math.factorial(num)
                
                elif operation == 'log':
                    num = float(expression)
                    if num <= 0:
                        error = "Logarithm undefined for non-positive numbers"
                    else:
                        result = math.log10(num)
                
                elif operation == 'power':
                    parts = expression.split('^')
                    if len(parts) == 2:
                        base = float(parts[0])
                        exponent = float(parts[1])
                        result = base ** exponent
                    else:
                        error = "Invalid power expression"
                
                elif operation == 'equals':
                    # Replace ^ with ** for Python evaluation
                    expression = expression.replace('^', '**')
                    result = eval(expression)
                
                else:
                    error = "Unknown operation"
            
            except ZeroDivisionError:
                error = "Cannot divide by zero"
            except ValueError as e:
                error = "Invalid input"
            except Exception as e:
                error = str(e)
            
            # Save calculation to DB
            Calculation.objects.create(
                expression=expression,
                operation=operation,
                result=str(result) if result is not None else None,
                error=error
            )

            return JsonResponse({
                'result': result,
                'error': error
            })
        except Exception as e:
            return JsonResponse({
                'result': None,
                'error': str(e)
            })
    
    return JsonResponse({'error': 'Invalid request'})

@require_GET
def history(request):
    calculations = Calculation.objects.order_by('-timestamp')[:20]  # latest 20
    data = [
        {
            'expression': c.expression,
            'operation': c.operation,
            'result': c.result,
            'error': c.error,
            'timestamp': c.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
        for c in calculations
    ]
    return JsonResponse({'history': data})