def even_only(numbers):
    result = []
    for n in numbers:
        if n % 2 == 0:
            result.append(n)
    return result
