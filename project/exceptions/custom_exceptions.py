"""Custom exceptin class to manage user level exception.

User level exceptions are reported back to end user for better user experiance. 
All other exceptions are properly managed by exception handlers
"""

class APIError(Exception):
	pass
