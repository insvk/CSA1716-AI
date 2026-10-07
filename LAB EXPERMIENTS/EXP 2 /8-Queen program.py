def solve_8_queens():
    def solve(row, cols, diag1, diag2, path):
        if row == 8:
            result.append(path)
            return
        for col in range(8):
            if col not in cols and row - col not in diag1 and row + col not in diag2:
                solve(row + 1, cols | {col}, diag1 | {row - col}, diag2 | {row + col}, path + [col])
    
    result = []
    solve(0, set(), set(), set(), [])
    return result

if __name__ == "__main__":
    solutions = solve_8_queens()
    print(f"Total solutions found: {len(solutions)}\nFirst solution:")
    for r in solutions[0]:
        print(". " * r + "Q " + ". " * (7 - r))
