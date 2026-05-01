@echo off
REM Code Quality Check Script for AUREXIS AI Backend (Windows)

echo 🔍 Running Code Quality Checks...
echo =================================

REM 1. Format with Black
echo 📝 Running Black formatter...
black --check --diff . || (
    echo ❌ Black formatting issues found. Run 'black .' to auto-fix.
    exit /b 1
)
echo ✅ Black formatting OK

REM 2. Sort imports with isort
echo 📦 Running isort...
isort --check-only --diff . || (
    echo ❌ Import sorting issues found. Run 'isort .' to auto-fix.
    exit /b 1
)
echo ✅ Import sorting OK

REM 3. Lint with flake8
echo 🔎 Running flake8...
flake8 . || (
    echo ❌ Flake8 linting issues found.
    exit /b 1
)
echo ✅ Flake8 linting OK

REM 4. Type check with mypy
echo 🔬 Running mypy type checker...
mypy . || (
    echo ❌ Type checking issues found.
    exit /b 1
)
echo ✅ Type checking OK

REM 5. Run tests
echo 🧪 Running tests...
pytest --cov=. --cov-report=term-missing --cov-report=html || (
    echo ❌ Tests failed.
    exit /b 1
)
echo ✅ Tests passed

echo.
echo 🎉 All code quality checks passed!
