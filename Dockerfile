[project]
name = "nomad-training-navigator"
version = "0.1.0"
description = "Streamlit app to manage and explore NOMAD training materials"
authors = [
  { name = "Siamak", email = "hidemyemail@physik.hu-berlin.de"  }
]
requires-python = ">=3.9"

dependencies = [
  "streamlit",
  "pandas"
]

[tool.black]
line-length = 100

[tool.ruff]
line-length = 100
select = ["E", "F", "I"]