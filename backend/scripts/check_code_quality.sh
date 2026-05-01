#!/bin/bash
# Code Quality Check Script for AUREXIS AI Backend

echo "🔍 Running Code Quality Checks..."
echo "================================"

# 1. Format with Black
echo "📝 Running Black formatter..."
black --check --diff . || {
    echo "❌ Black formatting issues found. Run 'black .' to auto-fix."
    exit 1
}
echo "✅ Black formatting OK"

# 2. Sort imports with isort
echo "📦 Running isort..."
isort --check-only --diff . || {
    echo "❌ Import sorting issues found. Run 'isort .' to auto-fix."
    exit 1
}
echo "✅ Import sorting OK"

# 3. Lint with flake8
echo "🔎 Running flake8..."
flake8 . || {
    echo "❌ Flake8 linting issues found."
    exit 1
}
echo "✅ Flake8 linting OK"

# 4. Type check with mypy
echo "🔬 Running mypy type checker..."
mypy . || {
    echo "❌ Type checking issues found."
    exit 1
}
echo "✅ Type checking OK"

# 5. Run tests
echo "🧪 Running tests..."
pytest --cov=. --cov-report=term-missing --cov-report=html || {
    echo "❌ Tests failed."
    exit 1
}
echo "✅ Tests passed"

echo ""
echo "🎉 All code quality checks passed!"
