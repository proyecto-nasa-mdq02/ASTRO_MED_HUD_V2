# ==========================================================================
#  CASOS DE USO: GESTIÓN DE TRIPULACIÓN Y ACCESO RBAC (CAPA 2 - APLICACIÓN)
# ==========================================================================

from typing import List, Dict, Any
from src.dominio.entidades import Tripulante
from src.dominio.excepciones import ErrorCredencialesInvalidas, ErrorEntidadNoEncontrada
from src.dominio.politicas_rbac import obtener_estrategia_rbac
from src.dominio.puertos import PuertoSeguridadHash
from src.infraestructura.persistencia.gestor_sqlite import GestorSQLite


class ServicioTripulacion:
    def __init__(self, uow: GestorSQLite, seguridad_hash: PuertoSeguridadHash):
        self.uow = uow
        self.seguridad = seguridad_hash

    def autenticar(self, usuario: str, password_plano: str) -> Tripulante:
        with self.uow:
            tripulante = self.uow.tripulantes.obtener_por_usuario(usuario)
            if not tripulante or not tripulante.password_hash:
                raise ErrorCredencialesInvalidas("Credenciales de misión inválidas o tripulante inactivo.")
            if not self.seguridad.verificar_hash(password_plano, tripulante.password_hash):
                raise ErrorCredencialesInvalidas("Credenciales de misión inválidas o tripulante inactivo.")
            return tripulante

    def registrar_tripulante(self, id_operador: int, datos: Dict[str, Any]) -> Tripulante:
        with self.uow:
            operador = self.uow.tripulantes.obtener_por_id(id_operador)
            if not operador:
                raise ErrorEntidadNoEncontrada("Operador autenticador no encontrado.")

            estrategia = obtener_estrategia_rbac(operador.rol)
            rol_destino = datos.get("rol", "Especialista de Mision")
            estrategia.validar_creacion(rol_destino)

            clave_plana = datos.get("password") or "artemis2026"
            nuevo = Tripulante(
                usuario=datos["usuario"],
                password_hash=self.seguridad.generar_hash(clave_plana),
                nombres=datos["nombres"],
                apellidos=datos["apellidos"],
                codigo_astronauta=datos["codigo_astronauta"],
                rol=rol_destino,
                especialidad=datos.get("especialidad", "General"),
                racha_autocuidado=datos.get("racha_autocuidado", 0),
            )
            return self.uow.tripulantes.guardar(nuevo)

    def modificar_tripulante(self, id_operador: int, id_destino: int, datos: Dict[str, Any]) -> Tripulante:
        with self.uow:
            operador = self.uow.tripulantes.obtener_por_id(id_operador)
            objetivo = self.uow.tripulantes.obtener_por_id(id_destino)
            if not operador or not objetivo:
                raise ErrorEntidadNoEncontrada("Tripulante u operador no encontrado.")

            estrategia = obtener_estrategia_rbac(operador.rol)
            estrategia.validar_modificacion(objetivo.rol, id_destino, id_operador)

            objetivo.nombres = datos.get("nombres", objetivo.nombres)
            objetivo.apellidos = datos.get("apellidos", objetivo.apellidos)
            objetivo.codigo_astronauta = datos.get("codigo_astronauta", objetivo.codigo_astronauta)
            objetivo.rol = datos.get("rol", objetivo.rol)
            objetivo.especialidad = datos.get("especialidad", objetivo.especialidad)

            if datos.get("password"):
                objetivo.password_hash = self.seguridad.generar_hash(datos["password"])
            else:
                objetivo.password_hash = None

            return self.uow.tripulantes.guardar(objetivo)

    def dar_baja_tripulante(self, id_operador: int, id_destino: int) -> None:
        with self.uow:
            operador = self.uow.tripulantes.obtener_por_id(id_operador)
            objetivo = self.uow.tripulantes.obtener_por_id(id_destino)
            if not operador or not objetivo:
                raise ErrorEntidadNoEncontrada("Tripulante no encontrado.")

            estrategia = obtener_estrategia_rbac(operador.rol)
            estrategia.validar_baja(objetivo.rol, id_destino, id_operador)
            self.uow.tripulantes.eliminar_logico(id_destino)

    def listar_tripulacion(self) -> List[Tripulante]:
        with self.uow:
            return self.uow.tripulantes.listar_todos()