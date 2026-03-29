"""
Mapping from MEDDOCAN-specific labels to generic PHI categories
for privacy evaluation purposes.
"""

# MEDDOCAN label to generic PHI category mapping
MEDDOCAN_TO_PHI_MAPPING = {
    # Person names
    'NOMBRE_SUJETO_ASISTENCIA': 'person',
    'NOMBRE_PERSONAL_SANITARIO': 'person',
    'FAMILIARES_SUJETO_ASISTENCIA': 'person',
    
    # Dates
    'FECHAS': 'date',
    
    # Locations
    'TERRITORIO': 'location',
    'PAIS': 'location',
    'CALLE': 'location',
    'HOSPITAL': 'location',
    'CENTRO_SALUD': 'location',
    'INSTITUCION': 'location',
    
    # IDs
    'ID_SUJETO_ASISTENCIA': 'id',
    'ID_CONTACTO_ASISTENCIAL': 'id',
    'ID_TITULACION_PERSONAL_SANITARIO': 'id',
    'ID_ASEGURAMIENTO': 'id',
    'ID_EMPLEO_PERSONAL_SANITARIO': 'id',
    'IDENTIF_DISPOSITIVOS_NRSERIE': 'id',
    'IDENTIF_BIOMETRICOS': 'id',
    'IDENTIF_VEHICULOS_NRSERIE_PLACAS': 'id',
    'NUMERO_BENEF_PLAN_SALUD': 'id',
    'OTRO_NUMERO_IDENTIF': 'id',
    
    # Age
    'EDAD_SUJETO_ASISTENCIA': 'age',
    
    # Contact information
    'NUMERO_TELEFONO': 'phone',
    'NUMERO_FAX': 'phone',
    'CORREO_ELECTRONICO': 'email',
    
    # Other
    'SEXO_SUJETO_ASISTENCIA': 'other',
    'PROFESION': 'other',
    'URL_WEB': 'other',
    'DIREC_PROT_INTERNET': 'other',
    'OTROS_SUJETO_ASISTENCIA': 'other',
}

def map_meddocan_to_phi(meddocan_label: str) -> str:
    """
    Map MEDDOCAN-specific label to generic PHI category.
    
    Args:
        meddocan_label: MEDDOCAN label (e.g., 'NOMBRE_SUJETO_ASISTENCIA')
    
    Returns:
        Generic PHI category (e.g., 'person', 'date', 'location', 'id', 'age', 'phone', 'email', 'other')
    """
    label_upper = meddocan_label.upper().strip()
    return MEDDOCAN_TO_PHI_MAPPING.get(label_upper, 'other')

def get_all_meddocan_labels() -> list:
    """Get all MEDDOCAN labels."""
    return list(MEDDOCAN_TO_PHI_MAPPING.keys())

def get_phi_categories() -> list:
    """Get all generic PHI categories."""
    return ['person', 'date', 'location', 'id', 'age', 'phone', 'email', 'other']


