from models.service import Service
from models.specialty import Specialty
from DAO.specialty_dao import SpecialtySqliteDAO
from DAO.dao import DAO

class ServiceSqliteDAO(DAO):
    """DAO para objetos Service, herdando funcionalidades genéricas."""

    def __init__(self):
        super().__init__()
        self.specialty_dao = SpecialtySqliteDAO()

    def create(self, service: Service) -> Service:
        """Salva um novo serviço usando o método genérico."""
        
        specialty_id = service.specialty.id if service.specialty else None
        
        data = {
            "id": service.id,
            "name": service.name,
            "description": service.description,
            "price": service.price,
            "specialty_id": specialty_id  
        }
        
        self._insert("services", data)
        return service

    def _map_row_to_service(self, row) -> Service:
        """Converte linha do banco em objeto Service, buscando a Especialidade."""
        specialty = None
        
        if row['specialty_id']:
            specialty = self.specialty_dao.find_by_id(row['specialty_id'])
        
        return Service(
            id=row['id'], 
            name=row['name'], 
            description=row['description'], 
            price=row['price'], 
            specialty=specialty
        )

    def find_all(self) -> list[Service]:
        """Busca todos os serviços."""
        rows = self._fetch_all("services")
        return [self._map_row_to_service(row) for row in rows]

    def find_by_id(self, service_id: str) -> Service | None:
        """Busca um serviço pelo ID."""
        row = self._fetch_by_id("services", service_id)
        if row:
            return self._map_row_to_service(row)
        return None

    def update(self, service: Service) -> Service:
        """Atualiza o serviço."""
        
        specialty_id = service.specialty.id if service.specialty else None
        
        data = {
            "name": service.name,
            "description": service.description,
            "price": service.price,
            "specialty_id": specialty_id
        }
        
        self._update("services", service.id, data)
        return service

    def delete(self, service_id: str) -> bool:
        """Deleta o serviço."""
        return self._delete("services", service_id)