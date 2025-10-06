import re
from typing import Optional

class FilterModule:

	def filters(self):
		return {
			"to_snake": self.to_snake_case
		}

	def to_snake_case(self, input: str, casing: Optional[str] = None):
		split = re.split(r"""
			(?<=[A-Z])(?=[A-Z][a-z])
			|(?<=[^A-Z])(?=[A-Z])
			|(?<=[A-Za-z])(?=[^A-Za-z])
			""",
			input,
			flags=re.VERBOSE
		)
		joined = "_".join((s.strip().strip("_") for s in split))
		scrubed = re.sub(r"^a-zA-Z0-9 _-","", joined)
		snaked = scrubed.translate(str.translate(" -","__"))

		if casing:
			if casing.upper().startswith("UP"):
				return snaked.upper()
			if casing.upper().startswith("LOW"):
				return snaked.lower()
			
		return snaked
			