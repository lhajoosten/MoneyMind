import re

# Read the file
with open("tests/unit/test_user_repository.py", "r") as f:
    content = f.read()

# Replace all instances of scalar_one_or_none.return_value with scalar_one_or_none = MagicMock(return_value=
content = re.sub(
    r"mock_result\.scalar_one_or_none\.return_value = ([^;]+)",
    r"mock_result.scalar_one_or_none = MagicMock(return_value=\1)",
    content,
)

# Write back
with open("tests/unit/test_user_repository.py", "w") as f:
    f.write(content)

print("Updated all scalar_one_or_none mocks")
