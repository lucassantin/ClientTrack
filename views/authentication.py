from models.employee import Employee
from models.specialty import Specialty

class UsersView:
    """View for user-related operations."""

    def create_employee(self, name: str, contact: str, specialty: Specialty):
        """Create a new employee."""
        return Employee(name, contact, specialty)
